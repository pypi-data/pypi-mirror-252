#!/usr/bin/env python
#
# WebActogram
# Copyright (C) 2020-2022 Barrett F. Davis
# Copyright (C) 2021-2024 Stephen Karl Larroque
#
# Licensed under the MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#=================================
#          WebActogram
#      by Barrett F. Davis
#      and other contributors
#      maintained by Stephen Karl Larroque
#         License: MIT
#  Creation date: 2023-08-04
#=================================

## Imports

# Native IO
import argparse
import configparser
import glob
import os
import random
import shlex
import sys
import sqlite3
from shutil import copy, rmtree
# Native maths
import datetime
from datetime import timedelta
from datetime import datetime as dt
from itertools import groupby
# Typing
from collections.abc import Sequence
# Path
from pathlib import Path 
# Browser history
from browser_history import get_history

# Scientific stack
import numpy as np
import pandas as pd
from scipy.ndimage import median_filter

# Plot
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter

# GUI
import matplotlib.image as mpimg

## Plots config
plt.close('all'); plt.style.use('default')  # close all plots and use default style
for tick in ['xtick.minor.visible', 'ytick.minor.visible']:
    plt.rcParams[tick] = False  # disable minor ticks

## Main class
class Actography:
    def __init__(self, args):
        self.show = args.show  # show the plot
        self.png = args.png  # save as png
        self.save_csv = args.csv  # save as csv

        self.freq = args.freq
        self.norm = args.normalize
        self.dblur = args.daily_blur
        self.hblur = args.hourly_blur

        self.landscape = args.landscape  # horizontal or vertical printing mode
        self.printer_friendly = args.printer_friendly  # printer friendly mode (black and white)

        self.legacy = args.legacy  # use legacy (internal) browsers histories import method, otherwise if false we will use browser-history external module (more browsers supported and all profiles are imported)

        self.zz = None # wakefulness
        self.dd = None # day range
        self.h1 = None # 24 hour range
        self.h2 = None # 48 hour range

        self.act = None  # actogram
        self.pdf = None  # probability density function
        self.timeshare = None  # timeshare

        self.sleeps = []  # sleep times

        self.df = pd.DataFrame() # activity dataframe (each row === site visit time)
        self.binned_df = pd.DataFrame() # df binned by interval (e.g. 15 min)

        self.freq_intv = float(self.freq[:-1])/60  # frequency interval in hours
        self.freq_no = int(24*60/float(self.freq[:-1]))  # frequency number

        self.h1 = np.linspace(0, 24, self.freq_no, endpoint=False)  # 24 hour range
        self.h2 = np.linspace(0, 48, 2*self.freq_no, endpoint=False)  # 48 hour range

        self.end = dt.combine(dt.today() - timedelta(days=1), dt.max.time())  # end date

        # TODO fix this to query intelligently (i.e., ignore 5% of early days
        # if they are isolated from rest, use a cutoff like 90% of data

        # start date
        if args.start == 'available':
            self.start = dt.fromisoformat('2000-01-01 00:00:00')  # if start date is available, set to 2000-01-01 00:00:00
        elif args.start is not None:
            self.start = dt.fromisoformat(args.start)  # if start date is not None, set to the start date
        else:
            self.start = dt.fromisoformat('2000-01-01 00:00:00')  # otherwise, set to 2000-01-01 00:00:00

    def __call__(self):
        self.__main__()

    def __main__(self):
        os.makedirs('actograms/', exist_ok=True)

        # import the data
        if self.legacy:
            # Old internal method to import browsers histories
            self.ImportData(self)
        else:
            # New method to import browsers histories using an external module
            self.import_data_ext()
        self.ProcessData(self)  # process the data

        plot = self.PlotData(self)  # plot the data
        self.ExportData(self, plot)  # export the data (to png or csv)

    def import_data_ext(self):
        """ Import histories data using browser-history package """
        outputs = get_history()
        # his is a list of (datetime.datetime, url) tuples
        histories = outputs.histories
        # convert to a dataframe with the same structure as before, to stay compatible
        df = pd.DataFrame((x[0] for x in histories), columns=['visit_time'])
        df['visit_time'] = pd.to_datetime(df['visit_time'].dt.tz_localize(None), errors='coerce').dropna()  # drop NaT values (and keep it as a DataFrame, because it will always return a Series since we are manipulating a single column)
            # TODO: browser-history.get_history() returns timezone-awake datetime objects, but the rest of the code compares against timezone-naive datetime objects, so for now we strip away the timezone-aware info using df['visit_time'].dt.tz_localize(None)
        self.df = df
        return df

    class ImportData:
        def __init__(self, act):
            super().__init__()
            self.act = act  # actogram class
            self.history_loc_dict_temp = []  # temporary dictionary to store the filepaths of the temporary history files and which browser they relate to (for SQLite queries) -- we copy history files to a temporary folder to avoid modifying the original ones

            self.__main__()

        def __main__(self):
            self.lookup_history_filepaths()  # lookup the history filepaths
            self.copy_history_to_temp_folder()  # copy the history files to a temporary folder
            self.import_history_to_working_memory()  # import the history files to working memory
            self.delete_temporary_history_folder()  # delete the temporary folder

        def find_firefox_profile(self, home):
            """ Find the default Firefox profile on the user's computer. """
            if sys.platform == "darwin":
                profile_dir = os.path.join(home, 'Library/Application Support/Firefox')
            elif sys.platform == "win32":
                profile_dir = os.path.join(home, 'AppData/Roaming/Mozilla/Firefox')
            elif sys.platform == "linux":
                profile_dir = os.path.join(home, '.mozilla/firefox')
            ff_config = configparser.ConfigParser()
            ff_config.read(os.path.join(profile_dir, "profiles.ini"))
            for section in ff_config.sections():
                if section.startswith("Install"):
                    p = ff_config[section]["Default"]
                    if "default-release" in p:
                        profile = p
            profile_path = os.path.join(profile_dir, profile)
            return profile_path

        def lookup_history_filepaths(self):
            """ check which OS user is running script from, then
            check typical file paths for popular browser history files """

            #home = os.path.expanduser("~")
            home = str(Path.home())
            history_filepaths = {}  # dictionary to store filepaths for each browser. Structure is: {browser: [filepath1, filepath2, ...]} because there can be multiple filpaths for the browser history, multiple profiles per browser, and sometimes the default profile is not named Default (eg for Chrome).

            if sys.platform == "darwin":  # Darwin == OSX
                history_filepaths['safari'] = [os.path.join(home, 'Library/Safari/History.db')]
                history_filepaths['chrome'] = [os.path.join(home, 'Library/Application Support/Google/Chrome/Default/History'),
                                               os.path.join(home, 'Library/Application Support/Google/Chrome/Profile 1/History'),
                                               os.path.join(home, 'Library/Application Support/Google/Chrome/Guest/History')
                                               ]
                history_filepaths['firefox'] = [os.path.join(self.find_firefox_profile(home), 'places.sqlite')]
                history_filepaths['edge'] = [os.path.join(home, 'Library/Application Support/Microsoft Edge/Default/History'),
                                             os.path.join(home, 'Library/Application Support/Microsoft Edge/Profile 1/History'),
                                             os.path.join(home, 'Library/Application Support/Microsoft Edge/Guest/History')
                                            ]

            elif sys.platform == "win32":
                # Note: when using os.path.join(), make sure there is no leading '/', otherwise it will treat it as an absolute path and forget the home directory
                history_filepaths['safari'] = [os.path.join(home, 'AppData/Local/Safari/History.db')]
                history_filepaths['chrome'] = [os.path.join(home, 'AppData/Local/Google/Chrome/User Data/Default/History'),
                                               os.path.join(home, 'AppData/Local/Google/Chrome/User Data/Profile 1/History'),
                                               os.path.join(home, 'AppData/Local/Google/Chrome/User Data/Guest/History')
                                               ]
                history_filepaths['firefox'] = [os.path.join(self.find_firefox_profile(home), 'places.sqlite')]
                history_filepaths['edge'] = [os.path.join(home, 'AppData/Local/Microsoft/Edge/User Data/Default/History'),
                                            os.path.join(home, 'AppData/Local/Microsoft/Edge/User Data/Profile 1/History'),
                                            os.path.join(home, 'AppData/Local/Microsoft/Edge/User Data/Guest/History')
                                            ]
                
            elif sys.platform == "linux":
                history_filepaths['safari'] = [os.path.join(home, '.config/safari/History.db')]
                history_filepaths['chrome'] = [os.path.join(home, '.config/google-chrome/Default/History'),
                                               os.path.join(home, '.config/google-chrome/Profile 1/History'),
                                               os.path.join(home, '.config/google-chrome/Guest/History')
                                               ]
                history_filepaths['firefox'] = [os.path.join(self.find_firefox_profile(home), 'places.sqlite')]
                history_filepaths['edge'] = [os.path.join(home, '.config/microsoft-edge/Default/History'),
                                            os.path.join(home, '.config/microsoft-edge/Profile 1/History'),
                                            os.path.join(home, '.config/microsoft-edge/Guest/History')
                                            ]

            else:
                print('Sorry, having trouble with your operating system.')
                sys.exit()

            self.history_loc_dict = history_filepaths

        def copy_history_to_temp_folder(self):
            """ Iterate through each file referenced in the history_loc_dict 
            and copy to some temporary folder. This avoids direclty operating 
            on the user's browsers' history files. """
            for browser, pathslist in self.history_loc_dict.items():
                for path in pathslist:
                    if path is not None and os.path.exists(path) and os.path.isfile(path):
                        # If the file exists, copy it to a temporary folder
                        self.copy_history_func(browser, path)

        def copy_history_func(self, browser, src, dst_folder='temp_history'):
            """ function to copy file at given file location to temporary folder"""
            os.makedirs(dst_folder, exist_ok=True)
            fname = Path(src).name  # get the filename from the path
            dst = os.path.join(dst_folder, fname)
            # Test if destination file already exists
            if os.path.exists(dst):
                # If it already exists (eg, multiple profiles for one browser), change destination folder dst to append a random number to the filename to avoid collision
                dst = os.path.join(dst_folder, fname + str(hex(random.getrandbits(65))[2:-1]))

            # Since the output can be different from input, we need to create a new dict to map and remember what are the browsers (to know which SQLite commands to send)
            self.history_loc_dict_temp.append([browser, dst])

            try:
                copy(src, dst)
                return dst

            except IOError as e:
                print("Unable to copy file. %s" % e)

            except FileNotFoundError:
                print('The file \'' + fname + '\' could not be found.')

            except Exception:
                print('Something went wrong, the file \'' +
                      fname + '\' was not loaded.')

        def import_history_to_working_memory(self):
            """ Imports all the files in the temporary folder into working
                memory. Each browser's particular history file format is 
                standardized before concatenating to an overarching df.
                This effectively merges all histories from various browsers and profiles."""
            
            # All the sql commands to extract the history data from the different browsers SQLite databases
            sql_commands = {
                'safari':
                    'SELECT datetime(visit_time+978307200, "unixepoch",\
                    "localtime") FROM history_visits ORDER BY visit_time DESC;',
                'chrome':
                    "SELECT datetime(last_visit_time/1000000-11644473600,\
                    'unixepoch','localtime') FROM urls ORDER BY last_visit_time DESC;",
                'firefox':
                    'SELECT datetime(visit_date/1000000,\
                    "unixepoch", "localtime") FROM moz_historyvisits ORDER BY visit_date ASC;',
                'edge':
                    "SELECT datetime(last_visit_time/1000000-11644473600,\
                    'unixepoch','localtime') FROM urls ORDER BY last_visit_time DESC;"
            }

            df_list = []  # list of dataframes to concatenate outside of the loop (faster than concatenating inside the loop, otherwise memory is reallocated at each iteration so complexity is O(N^2) quadratic)

            # For each browsers' history file, import the data into a pandas dataframe and add into a list
            for (browser, path) in self.history_loc_dict_temp:
                    if path is not None and os.path.exists(path) and os.path.isfile(path):
                        # If the file doesn't exist, skip it
                        df = self._import_history_func(path, sql_commands[browser])
                        df_list.append(df) # add the dataframe to the list of dataframes, complexity O(1)
            # Concatenate all dataframes at once, complexity is then O(N)
            self.act.df = pd.concat(df_list)

        def delete_temporary_history_folder(self):
            """ Delete the temporary folder after files are copied into working 
            memory. No need to cache this temporary folder, unless looking to back up
            browser history data (in which case there are better alternatives) """
            if os.path.isdir('temp_history'):
                rmtree('temp_history')

        def _import_history_func(self, file_name, command_str):
            """ Function to open SQL styled history files and convert to a pandas
            DataFrame type. SQL objects are closed after copying to Pandas DF. """
            cnx = sqlite3.connect(file_name)  # connect to the SQLite database
            df = pd.read_sql_query(command_str, cnx)  # read the SQL query into a pandas dataframe
            cnx.commit()  # commit changes (this is necessary to close the connection, and is why we copy the history files to a temporary folder beforehand to avoid tampering the originals)
            cnx.close()  # close the connection

            df.rename(inplace=True, columns={df.columns[0]: 'visit_time'})  # rename the column to 'visit_time' for consistency
            df['visit_time'] = pd.to_datetime(df['visit_time'], errors='coerce').dropna()  # drop NaT values (and keep it as a DataFrame, because it will always return a Series since we are manipulating a single column)

            return df

    class ProcessData:
        """ Process the imported data into a format that can be plotted """
        def __init__(self, act):
            super().__init__()
            self.act = act  # actogram class

            self.pcm = None  # pcolormesh data
            self.pdf = None  # probability density function
            self.tshare = None  # timeshare

            self.df = self.act.df  # activity dataframe
            self.binned_df = self.act.df  # binned dataframe

            self.__main__()

        def __main__(self):
            self.aggregate_visits_by_freq()  # aggregate the visits by frequency
            self.pre_allocate_binned_df()  # pre-allocate the binned dataframe
            self.clip_date_range()  # clip the date range to the first visit # TODO make timezone aware, add option for visualizing in either current tz or selected tz

            self.init_pcolormesh_args()  # initialize the pcolormesh arguments
            self.apply_median_blurring()  # apply median blurring
            self.define_pcolormesh_args()  # define the pcolormesh arguments

            self.check_continuous_sleep_times()  # check the continuous sleep times
            self.define_subplot_args()  # define the subplot arguments

            self.pass_processed_data()  # pass the processed data to the plotting class

        def aggregate_visits_by_freq(self):
            """
            INPUT: pandas dataframe from private class variables

            OUTPUT: Nx1 pandas dataframe (not series) of binned visit histories

            DESCRIPTION: 
            Aggregate the M rows for each unique visit from self.df into some N 
            rows corresponding to all the time intervals (e.g. 5 min)
            in the input dataframe's date range. Output row values are the 
            number of visits within each time interval. """
            visits = pd.to_datetime(self.df.loc[:, 'visit_time'])  # convert the visit_time column to datetime objects
            self.df = pd.DataFrame({'visits': np.ones(len(visits))}, index=visits)  # create a dataframe with the visits column and the visits as the index
            self.df = self.df.resample(self.act.freq).agg({'visits': 'sum'})  # resample the dataframe to the specified frequency and aggregate the visits column by summing
            self.df = self.df.fillna(0)  # fill the NaN values with 0

        def pre_allocate_binned_df(self):
            """
            INPUT: binned visit histories from previous step (private class variable)

            OUTPUT: M x  binned dataframe of appropriate shape 

            DESCRIPTION: 
            Aggregate the M rows for each unique visit from self.df into some N 
            rows corresponding to all the time intervals (e.g. 5 min)
            in the input dataframe's date range. Output row values are the 
            number of visits within each time interval. 
            """
            bdf = pd.DataFrame(data=self.df, index=self.df.index)  # create a dataframe with the same index as self.df

            d1 = self.df.index.min().floor(freq='D') - timedelta(days=1)  # get the first date in the index and subtract one day
            d2 = self.df.index.max().ceil(freq='D') - timedelta(days=1, seconds=1)  # get the last date in the index and subtract one day and one second
            days = pd.date_range(d1, d2, freq=self.act.freq)  # create a date range from the first date to the last date with the specified frequency

            bdf = bdf.reindex(days, fill_value=0)  # reindex the dataframe with the date range and fill the NaN values with 0
            bdf['x'], bdf['y'] = (lambda x: (x.date, x.time))(bdf.index)  # create columns for the date and time
            bdf.rename(columns={'visits': 'z'}, inplace=True)  # rename the visits column to z

            self.binned_df = bdf  # update the binned dataframe

        def clip_date_range(self):
            """ clip the date range to the first visit """
            first_visit = self.df.ne(0)  # creates a boolean mask where each element is True if the corresponding element in self.df is not equal to 0, and False otherwise.
            first_visit = first_visit.idxmax()  # returns the index of the first occurrence of the maximum value in the Series. If the Series is all True/False values, then this will be the index of the first True value.
            first_visit = first_visit.iloc[0]  # indexing the Series returned by idxmax().
            dt_first_visit = dt.combine(first_visit, dt.min.time())  # combine the date of the first visit with the minimum time of the datetime object
            if self.act.start <= dt_first_visit: self.act_start = dt_first_visit  # if the start date is before the first visit, then set the start date to the first visit

            bdf = self.binned_df  # binned dataframe
            bdf = bdf.fillna(0)  # fill the NaN values with 0
            bdf = bdf[bdf.index >= self.act.start]  # clip the date range to the start date
            bdf = bdf[bdf.index <= self.act.end]  # clip the date range to the end date

            self.act.dd = pd.unique(bdf.index.date)  # unique dates

            self.binned_df = bdf  # update the binned dataframe

        def init_pcolormesh_args(self):
            """ define the x, y and z (color) data structure for plotting later on"""
            z = self.binned_df['z'].T.values
            act_z = np.asarray(z.reshape(len(self.act.h1), -1, order='F'))  # reshape the z array to be 2D

            self.pcm = {'x': None,  # x and y are None because they will be defined later
                        'y': None,
                        'z': act_z.astype(int)}  # z is the reshaped z array

        def apply_median_blurring(self):
            """ apply blurring process to smooth out time away from the internet 
            at the daily level or one-off periods at the day-to-day level"""
            zz = self.pcm['z']

            if self.act.hblur: zz = median_filter(zz, size=(self.act.hblur, 1))  # apply median filter to the z array
            if self.act.dblur: zz = median_filter(zz, size=(1, self.act.dblur))  # apply median filter to the z array
            if self.act.norm:  zz = (zz>=1)  # normalize the z array

            self.pcm['z'] = zz.astype(float)  # update the pcm dictionary

        def define_pcolormesh_args(self):
            """ define the x, y and z (color) data structure for plotting later on """
            xx, yy, zz = self.act.dd, self.act.h2, np.tile(self.pcm['z'], (2, 1))  # tile the z array to create a 2D array

            if not self.act.landscape:  # if vertical
                xx, yy = yy, xx  # swap the x and y arrays
                zz = zz.T  # transpose the z array

            self.pcm = {'x': xx, 'y': yy, 'z': zz}  # update the pcm dictionary
            self.act.act = self.pcm  # update the act dictionary

        def define_subplot_args(self):
            """ define the x, y and z (color) data structure for plotting later on """
            dt = self.act.freq_intv  # time interval

            ax_pdf = 0^self.act.landscape  # axis for pdf
            ax_ts = 1^self.act.landscape  # axis for timeshare

            zz = self.pcm['z']

            _ = lambda x: pd.Series(x).rolling(window=7, min_periods=0).mean()  # rolling average function
            offline_avg = _(24 - np.nansum(zz * dt/2, axis=ax_ts))  # average offline time
            sleeps_avg = _(self.act.sleeps)  # average sleep time

            #days = pd.date_range(self.act.dd[0], self.act.dd[-1])  # days
            #pdf = np.pad(pdf, (2,1), mode='edge')  # pad the pdf with zeros on either side
            #offline_avg = np.pad(offline_avg, (1,2), mode='edge')  # pad the offline average with zeros on either side
            #sleeps_avg = np.pad(sleeps_avg, (1,2), mode='edge')  # pad the sleep average with zeros on either side

            self.act.timeshare = [offline_avg, sleeps_avg]  # timeshare
            self.act.pdf = (lambda x: x/x.max())(np.nansum(zz, axis=ax_pdf))  # pdf

        def pass_processed_data(self):
            """ pass processed data to the plotting class """
            self.act.df = self.df
            self.act.binned_df = self.binned_df

        def check_continuous_sleep_times(self):
            """
            INPUT: day vector (XX), binned search activity (ZZ)

            OUTPUT: vector with daily record for longest consecitive time offline 

            DESCRIPTION: 
            Takes vector of binary-encoded sleep-wake periods and tallies
            continuous stretches with zero-encoding (asleep) to a storage list. 

            Then appends the largest element in storage list to a second output
            list equal in len to XX corresponding to the longest offline periods. 

            Finally, multiplies np array'ed output list with binning frequency
            to estimate the longest real-time duration spent offline in date range
            """
            temp = self.binned_df
            #xx, yy, zz = self.pcm
            days, awake = temp['x'], (temp['z'] > 0).values.astype(int)  # convert to binary

            adhoc = pd.DataFrame(np.array([days, awake]).T, columns=['days', 'awake'])  # create a dataframe with the days and awake columns

            for idx, (_, v) in enumerate(list(adhoc.groupby('days')['awake'])):  # for each day, group the awake column by the day
                screen_breaks = [sum(not(i) for i in g) for _, g in groupby(v)]  # count the number of consecutive zeros (screen breaks) in the awake column
                longest_break = np.array(screen_breaks).max() * self.act.freq_intv  # get the longest break in the day and convert to hours
                self.act.sleeps.append(longest_break)  # append the longest break to the list of longest breaks

    class PlotData:
        """ Plot the processed data """
        def __init__(self, act):
            """ Initialize the plotting class """
            super().__init__()
            self.act = act

            self.freq_no = self.act.freq_no  # frequency number
            self.landscape = self.act.landscape  # landscape
            self.friendly = self.act.printer_friendly  # printer friendly

            self.DPI = 450  # dots per inch
            self.figsize = (8,6) if self.landscape else (7,8)  # figure size in inches

            self.px_size = tuple(map(lambda x: x*self.DPI, self.figsize))  # figure size in pixels

            self.lw = 1/(len(self.act.h1))  # line width
            if len(self.act.h1) > 24*5: self.lw = 0  # don't draw lines if too many

            # Horizontal and vertical plot parameters
            horizontal = {'figsize': self.figsize,  # figure size in inches

                          'ax_pdf': [0, 0], 'ax_sleep': [1, 1],  # axis locations for pdf and sleep
                          'labels': ['Activity PDF', 'Time Offline (h)'],  # axis labels for pdf and time offline
                          'hratio': [1, 0.15], 'wratio': [0.1, 1],  # height and width ratios for pdf and time offline

                          'left':   0.1, 'right':  0.95,  # left and right margins
                          'bottom': 0.05, 'top':    0.85,  # bottom and top margins
                          'wspace': 0.12, 'hspace': 0.2,  # width and height space
                        }

            vertical = {'figsize': self.figsize,  # figure size in inches

                        'ax_pdf': [1, 1], 'ax_sleep': [0, 0],  # axis locations for pdf and sleep
                        'labels': ['Time Offline (h)', 'Activity PDF'],  # axis labels for pdf and time offline

                        'hratio': [1, 0.1], 'wratio': [0.2, 1],  # height and width ratios for pdf and time offline

                        'left':   0.10, 'right':  0.85,  # left and right margins
                        'bottom': 0.05, 'top':    0.85,  # bottom and top margins
                        'wspace': 0.22, 'hspace': 0.12,  # width and height space
                        }

            self.plot_params = horizontal if self.landscape else vertical  # select plot parameters based on landscape or not

            self.__main__()

        def __main__(self):
            self.fig = self.plotter()

        def plotter(self):
            """ Plot the actogram """
            p = self.plot_params  # plot parameters
            fig, fig_ax = plt.subplots(figsize=p['figsize'])  # create a figure and axis

            # create a grid of subplots with specific styling options.
            plt.subplots_adjust(bottom=p['bottom'], top=p['top'],  # bottom and top margins
                                left=p['left'], right=p['right'],  # left and right margins
                                wspace=p['wspace'], hspace=p['hspace'])  # width and height space

            # Gridspec allows for more control over the layout of the figure
            spec = gridspec.GridSpec(ncols=2, nrows=2,  # number of columns and rows
                                     height_ratios = p['hratio'],  # height ratios
                                     width_ratios= p['wratio'])  # width ratios
            fig_ax.axis('off')  # turn off the axis

            ax_actogram = fig.add_subplot(spec[0, 1])  # add the actogram axis
            ax_sleep = fig.add_subplot(spec[p['ax_sleep'][0], p['ax_sleep'][1]])  # add the sleep axis
            ax_pdf = fig.add_subplot(spec[p['ax_pdf'][0], p['ax_pdf'][1]])  # add the pdf axis
            ax_nul = fig.add_subplot(spec[1, 0])  # add the null axis

            self.subplot_the_actogram(ax_actogram)  # plot the actogram
            self.subplot_the_timeshare(ax_sleep, ax_actogram)  # plot the timeshare
            self.subplot_the_pdf(ax_pdf, ax_actogram)  # plot the pdf
            self.plot_subplot_titles(ax_nul, fig_ax)  # plot the subplot titles

            return fig  # return the figure

        def subplot_the_actogram(self, ax):
            """ Subplot the actogram """
            cmap = 'binary' if self.friendly else 'binary_r'  # colormap

            lbl = lambda _: '0h' if not _%24 else ''.join('0'+str(_%24))[-2:]  # label function

            xx, yy, zz = [_ for k,_ in self.act.act.items()]  # x, y and z data

            # create a pseudocolor plot on the axes ax with specific styling options.
            ax.pcolormesh(xx, yy, zz,  # 2D arrays to represent the X and Y coordinates of the quadrilateral mesh, and then the colors in zz (each represent (x,y) coordinates)
                          shading='auto', cmap=cmap, vmin=0,  # color shading style automatic based on the shape of the input array, cmap is the colormap used to map zz values to colors, vmin=0 sets the minimum data value that the colormap covers
                          ec='dimgrey', lw=self.lw, clip_on=False)  # ec is the edge color between the rectangles, lw is the line width, clip_on=False means that the lines will be drawn outside of the axes

            if self.landscape:  # if horizontal
                locator = mdates.AutoDateLocator(minticks=1, maxticks=4)  # create a locator for the x axis. This will automatically select the best x axis tick locations based on the data.
                ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))  # set the x axis formatter to the locator

                ax.tick_params(axis='x', direction='out')  # set the x axis tick direction to out
                ax.set_xticks(ax.get_xticks())  # set the x ticks

                ax.set_yticks(np.arange(0, int(self.act.h2[-1]), 6))  # set the y ticks by 6 hour intervals
                ax.set_yticklabels(lbl(_) for _ in ax.get_yticks())  # set the y tick labels by the label function

                ax.invert_yaxis()  # invert the y axis

            else:  # if vertical
                locator = mdates.AutoDateLocator(minticks=1, maxticks=4)  # create a locator for the y axis.
                ax.yaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))  # set the y axis formatter to the locator

                ax.tick_params(axis='y', direction='out')  # set the y axis tick direction to out
                ax.set_yticks(ax.get_yticks())  # set the y ticks

                ax.set_xticks(np.arange(6, int(self.act.h2[-1]), 6))  # set the x ticks by 6 hour intervals
                ax.set_xticklabels(lbl(_) for _ in ax.get_xticks())  # set the x tick labels by the label function

                ax.yaxis.tick_left()  # move the y axis to the left
                ax.invert_yaxis()  # invert the y axis

            return ax  # return the axis

        def subplot_the_pdf(self, ax, ref_ax):
            """ Subplot the probability density function """
            x = self.act.h2  # hours
            pdf = self.act.pdf  # pdf

            if self.landscape:  # if horizontal
                ax.fill_betweenx(x, pdf, color='grey', alpha=0.3,lw=0,step='mid')  # plot the pdf

                ax.spines['top'].set_visible(False)  # remove the top and right spines
                ax.spines['left'].set_visible(False)  # remove the top and right spines

                ax.set_xlim([0, 1])  # set the x limits
                ax.set_xticks(ax.get_xlim())  # set the x ticks
                ax.set_xticklabels(ax.get_xticks())  # set the x tick labels
                ax.xaxis.set_major_formatter(FormatStrFormatter('%d'))  # set the x tick label format

                ax.yaxis.tick_right()  # move the y axis to the right
                ax.set_yticklabels([])  # remove the y tick labels
                ax.set_yticks(ref_ax.get_yticks())  # set the y ticks
                ax.set_ylim(ref_ax.get_ylim())  # set the y limits

                ax.invert_xaxis()

            else:  # if vertical
                ax.fill_between(x, pdf, color='grey', alpha=0.3,lw=0,step='mid')  # plot the pdf

                # remove the right and bottom spines
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_visible(False)

                ax.set_ylim([0, 1])  # set the y limits
                ax.yaxis.tick_left()  # move the y axis to the left
                ax.set_yticks(ax.get_ylim())  # set the y ticks
                ax.set_yticklabels(ax.get_yticks())  # set the y tick labels
                ax.yaxis.set_major_formatter(FormatStrFormatter('%d'))  # set the y tick label format

                ax.xaxis.tick_top()  # move the x axis to the top
                ax.set_xticklabels([])  # remove the x tick labels
                ax.set_xticks(ref_ax.get_xticks())  # set the x ticks
                ax.set_xlim(ref_ax.get_xlim())  # set the x limits

                ax.invert_yaxis()  # invert the y axis

            return ax

        def subplot_the_timeshare(self, ax, ref_ax):
            """ Subplot the timeshare """
            x = self.act.dd  # days
            y1, y2 = self.act.timeshare  # offline and sleep times

            if self.landscape:  # if horizontal
                ax.fill_between(x, y1, color='grey', alpha=0.3, lw=0, step='mid')  # plot the offline time
                ax.fill_between(x, y2, color='k', alpha=0.5, lw=0, step='mid')  # plot the sleep time

                ax.axes.axhline(8, color='k', linestyle='--', lw=0.75)  # plot the 8 hour mark

                ax.spines['right'].set_visible(False)  # remove the right and bottom spines
                ax.spines['bottom'].set_visible(False)  # remove the right and bottom spines

                ax.set_yticks([0, 8, 24])  # set the yticks
                ax.set_ylim(0, 24)  # set the y limits

                ax.xaxis.tick_top()  # move the x axis to the top
                ax.set_xticklabels([])  # remove the x tick labels
                ax.set_xticks(ref_ax.get_xticks())  # set the x ticks
                ax.set_xlim(ref_ax.get_xlim())  # set the x limits

                ax.invert_yaxis()  # invert the y axis

            else:  # if vertical
                ax.fill_betweenx(x, y1, color='grey', alpha=0.3, lw=0, step='mid')  # plot the offline time
                ax.fill_betweenx(x, y2, color='k', alpha=0.5, lw=0, step='mid')  # plot the sleep time

                ax.axes.axvline(8, color='k', linestyle='--', lw=0.75)  # plot the 8 hour mark
    
                ax.spines['left'].set_visible(False)  # remove the left and top spines
                ax.spines['top'].set_visible(False)  # remove the left and top spines

                ax.set_xticks([0, 8, 24])  # set the xticks
                ax.set_xlim(0, 24)  # set the x limits

                ax.yaxis.tick_right()  # move the y axis to the right
                ax.set_yticklabels([])  # remove the y tick labels
                ax.set_yticks(ref_ax.get_yticks())  # set the y ticks
                ax.set_ylim(ref_ax.get_ylim())  # set the y limits

                ax.invert_xaxis()  # invert the x axis

            return ax  # return the axis

        def plot_subplot_titles(self, ax, fig_ax):
            """ Plot the subplot titles """
            p = self.plot_params

            steps = int(60/(self.freq_no/(24)))  # steps in minutes

            if self.landscape:  # if horizontal
                ax.text(1, 1+p['hspace']/2, p['labels'][0], ha='right')  # plot the pdf label
                ax.text(1, p['hspace'], p['labels'][1], ha='right')  # plot the sleep label

                # prepare the title and subtitle
                s = ("Approximate sleep-wake periods, generated from time stamped "
                    "internet browser searches\nbetween {:%d-%b-%Y} and {:%d-%b-%Y}. "
                    "Window steps of {} minutes.".format(self.act.dd[0], self.act.dd[-1], steps))

            else:  # if vertical
                ax.text(1, 1-p['hspace'], p['labels'][0], ha='right')  # plot the pdf label
                ax.text(1, p['hspace']/2, p['labels'][1], ha='right')  # plot the sleep label

                # prepare the title and subtitle
                s = ("Approximate sleep-wake periods, generated from time stamped "
                    "internet browser searches between {:%d-%b-%Y} and {:%d-%b-%Y}. "
                    "Window steps of {} minutes.".format(self.act.dd[0], self.act.dd[-1], steps))

            # plot the title and subtitle
            fig_ax.text(x=0, y=1.1, s='Double-Plotted Online Actogram',
                     ha='left', va='bottom', fontweight='bold', wrap=True)
            fig_ax.text(0, 1.09, s=s, ha='left', va='top', wrap=True)

            # remove the axis
            ax.axis('off')

    class ExportData:
        """ Export the processed data """
        def __init__(self, act, plot):
            super().__init__()
            self.act = act
            self.plot = plot

            self.__main__()

        def __main__(self):
            if self.act.show or self.act.png: self.export_actogram_png()  # export the actogram as a png
            if self.act.save_csv: self.export_csv('visits')  # or export the actogram as a csv

        def show_image_with_matplotlib(self, file_path):
            img = mpimg.imread(file_path)
            imgplot = plt.imshow(img)
            plt.show()

        def export_actogram_png(self):
            """ Export the actogram as a png """
            fig = self.plot.fig

            orientation = 'horizontal' if self.act.landscape else 'vertical'  # orientation
            pngfilepath = 'actograms/actogram_' + orientation +'_' + dt.today().date().isoformat() + '.png'  # png file path
            fig.savefig(pngfilepath, dpi=self.plot.DPI)  # save the figure as a png
            if self.act.show:
                self.show_image_with_matplotlib(pngfilepath)

        def export_csv(self, filename):
            """ Export the actogram as a csv """
            self.act.df.to_csv('temp.csv')

            size_most_recent = 0
            list_exports  = glob.glob('actograms/*.csv')

            if len(list_exports):
                most_recent = sorted(list_exports, key=os.path.getsize)[0]
                size_most_recent = os.path.getsize(most_recent)

            if os.path.getsize('temp.csv') >= size_most_recent:
                self.act.df.to_csv('actograms/' + filename + '.csv')
                os.remove('temp.csv')


## Main entry point (with arguments parser)
def main(argv: Sequence[str] | None = None) -> int:
    """ Main entry point for the command line interface """
    if argv is None: # if argv is empty, fetch from the commandline
        argv = sys.argv[1:]
    elif isinstance(argv, str): # else if argv is supplied but it's a simple string, we need to parse it to a list of arguments before handing to argparse or any other argument parser
        argv = shlex.split(argv) # Parse string just like argv using shlex

    desc = '''WebActogram
Description: Generate actograms from web browsers history. This may help in retrospectively screening sleep-wake patterns & disorders.
This will output result files (a picture of the actogram plot and a csv file with all the detected browsers history) in an actograms folder.'''

    parser = argparse.ArgumentParser(add_help=True, description=desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--freq', type=str, action='store', default='15T', help='Frequency of the actogram. Default is 15T (15 minutes).')

    parser.add_argument('--start', type=str, action='store', default='2021-08-01', help='Start date of the actogram. Default is 2021-08-01.')
    parser.add_argument('--end', type=str, action='store', default=None, help='End date of the actogram. Default is None (today).')

    parser.add_argument('--hourly_blur', type=int, action='store', default=False, help='Hourly blur of the actogram. Default is 0 (no blur).')
    parser.add_argument('--daily_blur', type=int, action='store', default=False, help='Daily blur of the actogram. Default is 0 (no blur).')
    parser.add_argument('--normalize', type=int, action='store', default=True, help='Normalize the actogram. Default is True (normalize).')

    parser.add_argument('--png', action='store_true', default=True, help='Save the actogram as a png. Default is True (save).')
    parser.add_argument('--csv', action='store_true', default=True, help='Save the actogram as a csv. Default is True (save).')
    parser.add_argument('--show', action='store_true', default=True, help='Show the actogram in a window just after generation. Default is True (show).')
    parser.add_argument('--printer_friendly', action='store_true', default=False, help='Printer friendly actogram (black and white). Default is False (no).')
    parser.add_argument('--landscape', action='store_true', default=True, help='Orientation of the plot: True is horizontal, False is vertical. Default is True (horizontal).')
    parser.add_argument('--legacy', action='store_true', default=False, help='Use old internal method to import browser histories data. If false, will use browser-history external module (more browsers supported and all profiles are imported). Default: False (no).')

    ARGS, UNK = parser.parse_known_args(argv)

    act = Actography(ARGS)
    act()
    return 0


## Entrypoint if called from commandline
if __name__ == '__main__':
    main(sys.argv)
