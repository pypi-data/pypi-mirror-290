# Confidence Interval Tools

A small python library for calculating and drawing confidence intervals. 


1. [Requirements](#requirements)
2. [Status](#status)
3. [Documentation](#documentation)
    + [Installation](#installation)
    + [Usage](#usage) 
    + [Classes and methods](#classes-and-methods)
4. [Roadmap](#roadmap)
5. [Contribution](#contribution)


## Requirements 

```python
Python^3.12   ## might also work with lower versions, but untested  
pandas^2.2  
matplotlib^3.9  
seaborn^0.13  
scipy^1.14  
numpy^1.26
```


## Status

> [!WARNING]  
> The project is in a very early development phase. Expect important changes between updates. 

**Latest version**: 0.1.6

**Updated**: August 2024

**Changes since previous version**:
+ implemented of the `ste_ci` method for calculating the standard error.
+ added documentation


## Documentation

> [!NOTE]  
> **Last documentation update**: August 2024 

### Installation

This project is published in PyPi under the name `confidence_interval_tools`. 

#### With pip

```bash
pip install confidence_interval_tools
```

For updating to the latest available version:

```bash
pip install -U confidence_interval_tools
```

To force a specific version (for example 0.2.0):

```bash
pip install --force-reinstall -v "confidence_interval_tools==0.2.0"
```

#### With poetry

```bash
poetry add confidence_interval_tools@latest
```

For updating:

```bash
poetry update
```

#### In a Jupyter notebook (notice the exclamation mark)

```python
!pip install -U confidence_interval_tools
```


### Usage

Methods and classes can be imported directly, for example:

```python
from confidence_interval_tools import CI_Drawer

## [...]

a = CI_Drawer(data=data, x="x", y="y", kind=["bars", "area"], ci_type="std")
```

However, for the sake of readability and traceability, it might be better to import (and alias) the whole package at once:

```python
import confidence_interval_tools as cit

## [...]

a = cit.CI_Drawer(data=data, x="x", y="y", kind=["bars", "area"], ci_type="std")
```

As this package aims to be a complement to `Seaborn` and `Matplotlib`, we recommend reading the respective documentation of these two packages:
+ [Seaborn](https://seaborn.pydata.org/tutorial.html)
+ [Matplotlib](https://matplotlib.org/stable/users/index.html)

And additionally:
+ [Pandas](https://pandas.pydata.org/docs/user_guide/index.html)
+ [Numpy](https://numpy.org/doc/stable/user/)
+ [Scipy](https://docs.scipy.org/doc/scipy/tutorial/index.html)

### Classes and methods

#### Main module

> `CI_Drawer` (>=0.1.5)
>
> "A class for drawing a confidence interval in whatever way you prefer."
>
> **Arguments**:
> + `data` (pandas.DataFrame, optional): a pandas dataframe containing the necessary information to draw confidence intervals. If **data** is provided, **x**, **y**, **lower**, **upper**, and **std** can be given as column names.
> + `x` (str | *data type*, optional): column name or list / array / series with information about the horizontal coordinate of the data. If not provided, it will be assumed to be [1, 2, 3, 4, ...].
> + `y` (str | *data type*, optional): column name or list / array / series with information about the vertical coordinate of the data. Usually required unless **lower** and **upper** are provided directly.
> + `lower` (str | *data type*, optional): bypass the internal calculation by directly providing values for the lower bound of each confidence interval.
> + `upper` (str | *data type*, optional): bypass the internal calculation by directly providing values for the upper bound of each confidence interval.
> + `kind` ("lines" | "bars" | "area" | "scatterplot" | "none", optional): a selection of what kind of confidence interval is to be drawn. The default is "none" (does nothing). Several kinds can be seleted at once and passed as a list or tuple, e.g., ["area", "bars"].
> + `ci_type` ("std" | "ste", optional): the type of calculation used for the confidence intervals. Currently available types are: standard deviation (std), standard error (ste). The default is set to "std".
> + `std` (str | *data type*, optional): bypass the internal calculation for the standard deviation by providing pre-calculated values.
> + `std_multiplier` (*numerical type*, optional): constant to be used as a multiplier of the standard deviation or standard error when a normal approximation is done. Currently used for "std" and "ste" CI types. Default is 1.96 (i.e., alpha risk level of 5%, two-sided). 
> + `orientation` ("horizontal" | "vertical", optional): orientation of the confidence interval, i.e., whether a confidence interval should be calculated for each value of **x** ("vertical"), or each value of **y** ("horizontal").
> + CI lines options: 
>    + `draw_lines` (bool, optional): manual toggle for the drawing of CI lines. Same as using **kind="lines"**.
>    + `draw_lower_line` (bool, optional): manual toggle for the drawing of a line for the lower bound of the confidence interval.
>    + `draw_upper_line` (bool, optional): manual toggle for the drawing of a line for the upper bound of the confidence interval.
>   + `lines_style` (*matplotlib linestyles type*, optional): style for the CI lines. Follows the same syntax as [Matplotlib linestyles](https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html). Default: "solid".
>   + `lower_line_style` (*matplotlib linestyles type*, optional): specify a different linestyle for the lower bound. Cf: **lines_style**.
>   + `upper_line_style` (*matplotlib linestyles type*, optional): specify a different linestyle for the upper bound. Cf: **lines_style**.
>   + `lines_color` (*matplotlib colors type*, optional): colo(u)r of the CI lines. See the lst of available [Matplotlib named colo(u)rs](https://matplotlib.org/stable/gallery/color/named_colors.html). Default: "black".
>   + `lower_line_color` (*matplotlib colors type*, optional): specify a different colo(u)r for the lower bound. Cf: **lines_color**.
>   + `upper_line_color` (*matplotlib colors type*, optional): specify a different colo(u)r for the upper bound. Cf: **lines_color**.
>   + `lines_linewidth` (*numerical type*, optional): linewidth for the CI lines. Default: 1 (pt).
>   + `lower_line_linewidth` (*numerical type*, optional): specify the linewidth for the lower bound. Cf: **lines_linewidth**.
>   + `upper_line_linewidth` (*numerical type*, optional): specify the linewidth for the upper bound. Cf: **lines_linewidth**.
>   + `lines_alpha` (*numerical type*, optional): opacity / transparency value (a.k.a. "alpha channel") for the CI lines. Must be a decimal value between 0 and 1. Default: 0.8.
>   + `lower_line_alpha` (*numerical type*, optional): specify the opacity for the lower bound. Cf: **lines_alpha**.
>   + `upper_line_alpha` (*numerical type*, optional): specify the opacity for the upper bound. Cf: **lines_alpha**.
> + CI bars options:
>   + `draw_bars` (bool, optional): manual toggle for the drawing of CI bars. Same as using **kind="bars"**.
>   + `draw_bar_ends` (bool, optional): whether to draw the perpendicular ends of the CI bars. Default: True when **draw_bars** is activated. Can be "abused" to draw the ends without drawing the actual body of the CI bars.
>   + `draw_lower_bar_end` (bool, optional): specify whether to draw the perpendicular ends of the CI bars for the lower bound.
>   + `draw_upper_bar_end` (bool, optional): specify whether to draw the perpendicular ends of the CI bars for the upper bound.
>   + `bars_style` (*matplotlib linestyles type*, optional): linestyle for the CI bars. See [Matplotlib linestyles](https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html). Default: "solid".
>   + `bars_color` (*matplotlib colors type*, optional): colo(u)r of the CI bars. See [Matplotlib named colo(u)rs](https://matplotlib.org/stable/gallery/color/named_colors.html). Default: "black".
>   + `bars_linewidth` (*numerical type*, optional): linewidth for the CI bars. Default: 1 (pt).
>   + `bars_alpha` (*numerical type*, optional): opacity of the CI bars. Default: 1.
>   + `bar_ends_style` (*matplotlib linestyles type*, optional): specify the linestyle used for the perpendicular ends of the CI bars. The default is "solid" and is independent from the linestyle of the main body of the bars.
>   + `bar_ends_color` (*matplotlib colors type*, optional): specify the colo(u)r of both ends of the CI bars. CF: **bars_color**.
>   + `lower_bar_end_color` (*matplotlib colors type*, optional): specify a colo(u)r for the lower bound.
>   + `upper_bar_end_color` (*matplotlib colors type*, optional): specify a colo(u)r for the upper bound.
>   + `bar_ends_width` (*numerical type*, optional): specify a fixed width for the perpendicular ends of the CI bars. Currently relative to the scale of the data, might change in the future (see [roadmap](#roadmap)). Takes priority over the **bar_ends_ratio** if specified.
>   + `bar_ends_ratio` (*numerical type*, optional): width of the perpendicular ends of the CI bars, expressed as a proportion of the average distance between two adjacent x (or y) coordinates. Values greater than 1 should result in overlaps between adjacent CI bars, which is usually not a desired behaviour. Default: 0.3.
>   + `hide_bars_center_portion` (bool, optional): when set to True, the middle part of the CI bars will not be drawn, so as to avoid obscuring the plot (for example if a central tendency was already plotted). Default: False.
>   + `bars_center_portion_length` (*numerical type*, optional): length of the central portion (i.e., the "middle part) of the CI bars. Currently relative to the scale of the data. Takes priority over **bars_center_portion_ratio** when specified. Used with **hide_bars_center_portion**.
>   + `bars_center_portion_ratio` (*numerical type*, optional): length of the central portion of the CI bars, expressed as a proportion of the bars' length. Used with **hide_bars_center_portion**. Default: 0.5.
> + CI area options:
>   + `fill_area` (bool, optional): manual toggle for the drawing of the confidence interval as a shaded area. Same as using **kind="area"**.
>   + `fill_color` (*matplotlib colors type*, optional): colo(u)r used for the shading of the CI area. See [Matplotlib named colo(u)rs](https://matplotlib.org/stable/gallery/color/named_colors.html). Default: "lavender".
>   + `fill_alpha` (*numerical type*, optional): opacity of the shaded area. Default: 0.4.
> + options for the scatterplot of the lowers and upper bounds:
>   + `plot_limits` (bool, optional): manual toggle for plotting the lower and upper bounds of the confidence intervals as separate datapoints. Same as using **kind="scatterplot"**.
>   + `plot_lower_limit` (bool, optional): whether to plot the lower bound.
>   + `plot_upper_limit` (bool, optional): whether to plot the upper bound.
>   + `plot_marker` (*matplotlib markers type*, optional): marker to be used when plotting the lower and upper bounds. See the list of [Matplotlib markers](https://matplotlib.org/stable/api/markers_api.html). Default: see **lower_plot_marker** and **upper_plot_marker**.
>   + `lower_plot_marker` (*matplotlib markers type*, optional): marker to be used when plotting the lower bound. Cf: **plot_marker**.
>   + `upper_plot_marker` (*matplotlib markers type*, optional): marker to be used when plotting the upper bound. Cf: **plot_marker**.
>   + `plot_color` (*matplotlib colors type*, optional): colo(u)r of the markers. See [Matplotlib named colo(u)rs](https://matplotlib.org/stable/gallery/color/named_colors.html). Default: "black".
>   + `lower_plot_color` (*matplotlib colors type*, optional): specify a colo(u)r for the lower bound. Cf: **plot_color**.
>   + `upper_plot_color` (*matplotlib colors type*, optional): specify a colo(u)r for the upper bound. Cf: **plot_color**.
>   + `plot_alpha` (*numerical type*, optional): opacity of the markers used when plotting the lower and upper bounds. Default: 0.8.
>   + `lower_plot_alpha` (*numerical type*, optional): specify the opacity for the lower bound.
>   + `upper_plot_alpha` (*numerical type*, optional): specify the opacity for the upper bound.
>   + `plot_size` (*numerical type*, optional): size of the markers (in pt square) when plotting the lower and upper bounds. Default: None (let Seaborn / Matplotlib decide). 
>   + `lower_plot_size` (*numerical type*, optional): specify a size for the markers of the lower bound. Cf: **plot_size**.
>   + `upper_plot_size` (*numerical type*, optional): specify a size for the markers of the upper bound. Cf: **plot_size**.
> + ax (matplotlib.axes.Axes, optional): a matplotlib Axes object to be used for drawing the confidence intervals. Defaut: last used object, identified with matplotlib.pyplot.gca(). 
>
> **Returns**: a new instance of the CI_Drawer class.
>
> **Instance attributes and methods**:
> + `.data` (pandas.DataFrame): a copy of the dataframe passed as argument.
> + `.x`, `.y` (pandas.Series): a copy of the x and y data passed as arguments.
> + `.lower`, `.upper` (pandas.Series): series containing the (calculated or specified) lower bounds and upper bounds.
> + `.unique_x`, `.unique_y` (pandas.Series): series containing the unique values filtered from x and y respectively.
> + `.std` (pandas.Series): series containing the (calculated or specified) standard deviation for each unique value of x (vertical CI) or y (horizontal CI).
> + `.mean` (pandas.Series): series containing the calculated mean for each unique value of x or y.
> + `.median` (pandas.Series): series containing the calculated median for each unique value of  or y.
> + `.q1`, `.q3` (pandas.Series): series containing the calculated first and third quartiles for each unique value of x or y.
> + `.as_datafrae()` (pandas.DataFrame): returns a dataframe containing most of the information listed above.
> + `.params` (dict): dictionary containing most of the parameters used for deciding what to draw and how to draw.
> + `.draw()` (None): method for drawing (or, redrawing) the confidence intervals with the given parameters. 
> + `.help()` (None): method to return a help message in an interpreter or a jupyter notebook. Not yet implemented.


> `std_ci` (>=0.1.5) 
>
> "Upper and lower bounds of a CI based on standard deviation (normal approximation around mean)"
>
> **Arguments**:
> + `v` (*data type*): a one-dimensional data vector (for example, all y values for a unique value of x) 
> + `std_multiplier` (*numerical type*): a number by which the standard deviation is multiplied to yield the confidence interval. 
> 
> **Returns**: a tuple, of the form (\<lower bound\>, \<upper bound\>).


> `ste_ci` (>=0.1.6)
>
> "Upper and lower bounds of a CI based on standard error (normal approximation around mean)"
>
> **Arguments**:
> + `v` (*data type*): a one-dimensional data vector (for example, all y values for a unique value of x) 
> + `ste_multiplier` (*numerical type*): a number by which the standard error is multiplied to yield the confidence interval. 
> 
> **Returns**: a tuple, of the form (\<lower bound\>, \<upper bound\>).


> `vectorized_to_df` (>=0.1.5)
>
> "General utility function, to return a dataframe calculated with several vectors, from a function accepting a single vector"
>
> **Arguments**:
> + `func` (callable): a callable function (such as **std_ci** or **ste_ci**), accepting a vector (pandas Series) as argument and returning a tuple.
> + `*args`, `**kwargs`: any other positional or keyword argument to be passed to the function.
>
> **Returns**: a pandas.DataFrame built from the output of **func** for each individual vector (stacked vertically). 


## Roadmap

Features to be added, changes to be implemented in future versions:
+ Add more methods for the calculation of confidence intervals
+ Ensure the support of Matplotlib's parametrized linestyles.
+ Create and expose a submodule for drawing methods (e.g., lines, bars, etc.)
+ Add the capability to draw and configure boxes (as in boxplots)? ... See solutions by Seaborn and Matplotlib for now.
+ Write a more detailed, wiki-like documentation, either on Gitlab or a separate website like readthedocs.com 
+ Support passing a configuration dictionary to avoid re-typing all arguments every time.
+ Add support for providing a nominal alpha risk level, in complement of the std_multiplier argument.
+ Add a clipping option, for bounded scales.
+ Add a rounding option, for categorical scales.
+ Express the width of bar_ends_width in pt or similarly convenient unit of measurement, independent of the scale of the data.
+ Add support for individual values of bars_center_portion_length and bars_center_portion_ratio.
+ Improve loading time if possible.
+ _Maybe more to come..._ 


## Contribution

Feel free to contribute, report bugs, suggest features, etc., on [GitLab](https://gitlab.com/aufildelanuit/confidence-interval-tools).