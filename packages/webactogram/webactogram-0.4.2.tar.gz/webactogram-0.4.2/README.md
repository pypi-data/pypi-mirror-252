# WebActogram
[![PyPI-Status][1]][2] [![PyPI-Versions][3]][2] [![PyPi-License][4]][2] [![PyPI-Downloads][5]][2]

🌐🏃Use your browser's history as a novel instantaneous mass screening tool for 🌙🛌sleep patterns & maybe disorders!

<img src="actograms/example_actogram_horizontal_2024-01-20.png" alt="image" width="50%" height="auto" />

## Install & Quickstart

### Install with a precompiled binary

This is the easiest way to install if you don't use Python.

Precompiled binaries are available for Windows 64-bits (MacOS and Linux in the future too).

To download, just get the .exe file of the [latest release](https://github.com/Circadiaware/webactogram/releases/latest).

Note: if you cannot find the .exe download on your computer, make sure that you explicitly accepted the download in your browser (eg, Chrome), as it may block it for safety and require you to go to the browser's downloads tab and accept manually the download (there is absolutely no risk, but if you are paranoid you can use the Python module instead, it's the exact same software).

Then just double-click on `webactogram_vX.Y.Z.exe`, it will autogenerate the actogram and then show it in a pop-up window.

On Windows, you may need to manually pass the Windows Defender SmartScreen like this:

![](res/windows_defender_smartscreen.png)

### Install using Python

First you need a modern Python 3 interpreter (Python > 3.7), such as [Miniconda3](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links).

Then, install WebActogram with:

```pip install webactogram```

To generate an actogram and display it, type the following command in a terminal (or `cmd` or PowerShell on Windows):

```webactogram```

Note: First, you need to `cd` in a folder with write permission (so that the actogram image can be saved in a subfolder).

This will create a folder `actograms` in the current folder, and add inside a picture with the latest actogram and a csv file with all the browsers activities recorded.

More options, such as the sampling frequency (and hence granularity of the actogram and its patterns) can be shown with:

```webactogram --help```

## Description
WebActogram is a tool that generates an activity graph, called an online actogram, from web browsers history files. It supports various browsers including Google Chrome, Mozilla Firefox and Safari history files (full list of supported browsers [here](https://browser-history.readthedocs.io/en/latest/browsers.html)).

To screen sleep-wake patterns and disorders, all sleep screening tools require that the user either manually record a sleep diary or wears an actigraphic device or participate in an even more cumbersome constant routine study with melatonin sampling under always dark conditions.

The main limitations of these approaches are:

1. the upfront cost (in money and/or time), as there needs to be a suspicion of a sleep disorder to request such data from a subject or medical tests (especially melatonin sampling),
2. there is a big latency between the time the user first suspects they may have a sleep disorder and the time they have enough data to get diagnosed, as it takes weeks or even months of rigorously acquired data by a very compliant subject for the sleep clinician to then be able to interpret if there is any potential sleep disorder.

Both of these issues make current sleep disorders diagnostic procedures very poor screening procedures, as the hurdles to get enough data to assess whether there is any sleep disorder at all is just too high for most people and is likely causing a big dropout rate. [Behavioral scales are also unfit for circadian rhythm disorders diagnosis](https://pubmed.ncbi.nlm.nih.gov/18041481/).

The web actogram is the first tool that can provide an instantaneous estimation of the user’s sleep-wake pattern, aka actogram, by being a pseudo-actigraphic tool that infers an actogram from the browser’s history. This could allow for mass screening of sleep-wake patterns and disorders via the simple and fast installation of an app.

Multiple web browsers are supported, and the histories of all supported browsers will be merged automatically, and include all profiles installed in all browsers.

Example plots: horizontal (landscape) mode:
![](actograms/example_actogram_horizontal_2022-03-31.png)

Vertical (portrait) mode:
![](actograms/example_actogram_vertical_2022-01-25.png)

The limitations are however as follows:

* The sleep patterns - the main measure of interest - are only very indirectly estimated, as this tool is estimating the wakefulness pattern, and even that is only partially covered since this tool analyzes internet desktop browsers histories (not whole computer usage history nor mobile nor user's activity the whole day).
* The web actogram reliability depends on whether the user is an avid user of web browsers: they must use their web browsers on an almost daily basis. They do not need to use their browser all the time however, but they need to use it regularly, so that we can estimate their wakefulness period. So regularity is necessary, not quantity. But even if quantity is not necessary, the more avid use of browsers, the more datapoints and the more reliable the estimate will be.
* The user must primarily use a web browser on a computer (not on a smartphone - this will be implemented in the future).
* The more data over a longer period, the more precisely and robust the pattern will appear.
* If there are multiple users on the same desktop computer, the result will be unreliable, as the tool will currently merge all profiles histories data in one and hence merge the usage data from different users.

How the actogram is plotted was inspired by [this UCSD tutorial](https://ccb.ucsd.edu/the-bioclock-studio/education-resources/basics/part2.html) and [this scientific paper](https://doi.org/10.1186/1741-7007-8-93).

## Usage
Plots are easily generated from the command line by typing the following command:

```webactogram```

Plots will be saved in a new sub-folder called "actograms" with appropriate timestamp and description. 

The software now supports command line arguments for additional customizability.
For example: 

```python actogram.py --freq '15T' --daily_blur 3 --start '2020-01-01' ```

```python actogram.py --freq '30T' --printer_friendly True```

```python actogram.py --dims (8,8)```

Where: 

```
--freq determines the granularity of binned online/offline periods (default is 15 minutes increments, ex.  --freq '15T')

--start_date sets initial date to plot from, default is 180 days ago (ex. --start_date '2022-01-01')

--daily_blur applies median filtering between days (off by default, ex. --daily_blur 3)  

--period_blur applies median filtering between binned time periods (off by default, ex. --period_blur 5)

--normalize normalizes search frequency against max, then applies binary mask (plot shows periods of some search history vs. none, on by default)

--dims sets the relative dimensions of generated actogram plot (ex. --dims (4, 6))

--printer_friendly sets whether activity is shown in black on white (friendly) or vice versa (False by default, ex. --printer_friendly True)
```

## Privacy statement

The only data that is extracted from your browsers usage is the datetime of visited pages from the browsers histories. The URLs is not extracted, nor any other information. No data is ever leaving your computer.

## Authors

This tool is a fork from the excellent [online_actogram](https://github.com/barrettfdavis/online_actogram) script by Barrett F. Davis who conceived both the idea and the first implementation initially released in [July 2020](https://web.archive.org/web/20221127100155/https://www.reddit.com/r/N24/comments/hxve2w/dont_delete_your_browser_history/).

Since then, it is maintained by Stephen Karl Larroque and the Circadiaware Collective.

Lots of awesome contributors made awesome contributions to further improve this software, we cannot thank them enough!

[![Contributors][6]][7]

For a list of all contributors, please see [the GitHub Contributors graph](https://github.com/circadiaware/webactogram/graphs/contributors) and the [commits history](https://github.com/circadiaware/webactogram/commits/master).

## License

MIT Public License.

## Similar projects

Another project, inspired by this one, was written in Javascript using D3, but it cannot fetch browser's history, it can only plot from an already extracted browser’s history: [Tylian's D3 Browser's History](https://web.archive.org/web/20221207124930/https://tylian.net/d3/history.html).
How to generate the history.txt file ([source](https://www.reddit.com/r/N24/comments/hxve2w/comment/g30ve2y/?utm_source=share&utm_medium=web2x&context=3)): ```It's a dump of the timestamp column with some manual processing to divide every entry by 1000, since Firefox stores them as a nanosecond epoch for some reason..```

[1]: https://img.shields.io/pypi/v/webactogram.svg
[2]: https://pypi.org/project/webactogram
[3]: https://img.shields.io/pypi/pyversions/webactogram.svg?logo=python&logoColor=white
[4]: https://img.shields.io/pypi/l/webactogram.svg
[5]: https://img.shields.io/pypi/dm/webactogram.svg?label=pypi%20downloads&logo=python&logoColor=white
[6]: https://contrib.rocks/image?repo=circadiaware/webactogram
[7]: https://github.com/circadiaware/webactogram/graphs/contributors
