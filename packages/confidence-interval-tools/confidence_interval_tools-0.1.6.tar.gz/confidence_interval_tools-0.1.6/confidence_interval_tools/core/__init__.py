"""
    My numpydoc description of a kind
    of very exhautive numpydoc format docstring.

    Parameters
    ----------
    first : array_like
        the 1st param name `first`
    second :
        the 2nd param
    third : {'value', 'other'}, optional
        the 3rd param, by default 'value'

    Returns
    -------
    string
        a value in a string

    Raises
    ------
    KeyError
        when a key error
    OtherError
        when an other error
"""

### TODO: write docstring, ensure it is accessible

import pandas
import numpy
import matplotlib
from matplotlib import pyplot as plt
import seaborn
from scipy import stats as sps
from typing import Literal


### A collection of type that can be used to make a plot
type datatype = pandas.DataFrame | pandas.Series | numpy.ndarray | list | tuple | int | float | numpy.float16 | numpy.float32 | numpy.float64 | numpy.float80 | numpy.float96 | numpy.float128 | numpy.float256
type numericaltype = int | float | numpy.float16 | numpy.float32 | numpy.float64 | numpy.float80 | numpy.float96 | numpy.float128 | numpy.float256
### A collection of all named matplotlib colors
exec(
    f"type matplotlib_colors_type = Literal{list(matplotlib.colors.CSS4_COLORS.keys())}"
)
### A collection of all linestyles in matplotlib
type matplotlib_linestyles_type = Literal[
    "solid", "dotted", "dashed", "dashdot", "-", ":", "--", "-.", "None", "", ","
] | tuple | None
### A collection of all marker styles in matplotlib
exec(
    f"type matplotlib_markers_type = Literal{list(matplotlib.lines.Line2D.markers.keys())}"
)


### general utility function, to return a dataframe of several vectors, from a function accepting a single vector
def vectorized_to_df(func: callable, *args, **kwargs) -> pandas.DataFrame:
    """General utility function, to return a dataframe calculated with several vectors, from a function accepting a single vector"""
    vec_func = numpy.vectorize(func)
    return pandas.DataFrame(vec_func(*args, **kwargs)).T


### sub-functions for calculating different type of confidence intervals
def extrapolate_quantile_value_linear(v: pandas.Series, q) -> numericaltype:
    """Linear extrapolation for quantiles greater than 1 or lower than 0"""
    if (q >= 0) and (q <= 1):
        return v.quantile(q)
    elif q > 1:  ## references are the last two points
        return (v.quantile(1) - v.quantile((len(v) - 2) / (len(v) - 1))) / (
            1 - (len(v) - 2) / (len(v) - 1)
        ) * (q - 1) + v.quantile(1)
    ## case q < 0 , references are the first two points
    return (v.quantile(0) - v.quantile((1) / (len(v) - 1))) / (
        0 - (1) / (len(v) - 1)
    ) * (q - 0) + v.quantile(0)


def std_ci(v: datatype, std_multiplier: numericaltype) -> tuple:
    """Upper and lower bounds of the CI based on standard deviation (normal approximation around mean)"""
    ### make sure v is a pandas Series, for the use of .mean() and .std()
    v = pandas.Series(v)
    ### return the lower and upper bounds of the confidence interval
    return (
        v.mean() - std_multiplier * v.std(),
        v.mean() + std_multiplier * v.std(),
    )


def ste_ci(v: datatype, ste_multiplier: numericaltype) -> tuple:
    """Upper and lower bounds of the CI based on standard error (normal approximation around mean)"""
    ### make sure v is a pandas Series, for the use of .mean() and .std()
    v = pandas.Series(v)
    ### return the lower and upper bounds of the confidence interval
    return (
        v.mean() - ste_multiplier * v.std() / (len(v) ** (1 / 2)),
        v.mean() + ste_multiplier * v.std() / (len(v) ** (1 / 2)),
    )


def wald_ci(v: pandas.Series) -> tuple:
    """Upper and lower bounds of the CI based on Wald's binomial approximation"""
    q_lower = pandas.Series(
        [
            0.05 - 1.96 / numpy.sqrt(len(v)) * numpy.sqrt(0.05 * (1 - 0.05)),
            0.05 + 1.96 / numpy.sqrt(len(v)) * numpy.sqrt(0.05 * (1 - 0.05)),
        ]
    ).quantile(q=0.25)
    return ()


### A class for drawing a confidence interval in whatever way you prefer, from pre-defined values
### note: this requires matplotlib, matplotlib.pyplot as plt, numpy, pandas, and scipy.stats as sps
class CI_Drawer(object):
    """A class for drawing a confidence interval in whatever way you prefer."""

    def __init__(
        self,
        data: pandas.DataFrame | None = None,  # ok
        x: str | datatype | None = None,  # ok
        y: str | datatype | None = None,  # ok
        lower: str | datatype | None = None,  # partial?
        upper: str | datatype | None = None,  # partial?
        kind: (
            Literal["lines", "bars", "area", "scatterplot", "none"]
            | list[str]
            | tuple[str]
            | None
        ) = None,  # ok
        ci_type: Literal[
            "std",
            "ste",
            "Wald",
            "Wilson",
            "Clopper–Pearson",
            "Agresti–Coull",
            "Rule of three",
        ] = "std",  # ongoing
        extrapolation_type: Literal[
            "linear"
        ] = "linear",  ### TODO: add more options, such as Scholz, Hutson, etc.
        std: str | datatype | None = None,  # ongoing
        std_multiplier: numericaltype = 1.96,  # ok (nothing to do?)
        orientation: Literal["horizontal", "vertical"] = "vertical",  # ok
        draw_lines: bool = False,  # ok
        draw_lower_line: bool | None = None,  # ok
        draw_upper_line: bool | None = None,  # ok
        lines_style: matplotlib_linestyles_type = "solid",  # ok
        lower_line_style: matplotlib_linestyles_type | None = None,  # ok
        upper_line_style: matplotlib_linestyles_type | None = None,  # ok
        lines_color: matplotlib_colors_type = "black",  # ok
        lower_line_color: matplotlib_colors_type | None = None,  # ok
        upper_line_color: matplotlib_colors_type | None = None,  # ok
        lines_linewidth: numericaltype = 1,  # ok
        lower_line_linewidth: numericaltype | None = None,  # ok
        upper_line_linewidth: numericaltype | None = None,  # ok
        lines_alpha: numericaltype = 0.8,  # ok
        lower_line_alpha: numericaltype | None = None,  # ok
        upper_line_alpha: numericaltype | None = None,  # ok
        draw_bars: bool = False,  # ok
        draw_bar_ends: bool | None = None,  # ok
        draw_lower_bar_end: bool | None = None,  # ok
        draw_upper_bar_end: bool | None = None,  # ok
        bars_style: matplotlib_linestyles_type = "solid",  # ok
        bars_color: matplotlib_colors_type = "black",  # ok
        bars_linewidth: numericaltype = 1,  # ok
        bars_alpha: numericaltype = 1,  # ok
        bar_ends_style: matplotlib_linestyles_type = "solid",  # ok
        bar_ends_color: matplotlib_colors_type | None = None,  # ok
        lower_bar_end_color: matplotlib_colors_type | None = None,  # ok
        upper_bar_end_color: matplotlib_colors_type | None = None,  # ok
        bar_ends_width: numericaltype | None = None,  # ok
        bar_ends_ratio: numericaltype = 0.3,  # ok
        hide_bars_center_portion: bool = False,  # ok
        bars_center_portion_length: numericaltype | None = None,  # ok
        bars_center_portion_ratio: numericaltype = 0.5,  # ok
        fill_area: bool = False,  # ok
        fill_color: matplotlib_colors_type = "lavender",  # ok
        fill_alpha: numericaltype = 0.4,  # ok
        plot_limits: bool = False,  # ok
        plot_lower_limit: bool | None = None,  # ok
        plot_upper_limit: bool | None = None,  # ok
        plot_marker: matplotlib_markers_type | None = None,  # ok
        lower_plot_marker: matplotlib_markers_type | None = None,  # ok
        upper_plot_marker: matplotlib_markers_type | None = None,  # ok
        plot_color: matplotlib_colors_type = "black",  # ok
        lower_plot_color: matplotlib_colors_type | None = None,  # ok
        upper_plot_color: matplotlib_colors_type | None = None,  # ok
        plot_alpha: numericaltype = 0.8,  # ok
        lower_plot_alpha: numericaltype | None = None,  # ok
        upper_plot_alpha: numericaltype | None = None,  # ok
        plot_size: numericaltype | None = None,  # ok
        lower_plot_size: numericaltype | None = None,  # ok
        upper_plot_size: numericaltype | None = None,  # ok
        binomial_ci_policy: (
            Literal[
                "conservative",
                "conservative quartile",
                "median",
                "optimistic quartile",
                "optimistic",
            ]
            | int
            | float
        ) = "conservative",  # ok
        ax: matplotlib.axes.Axes | None = None,  # ok
    ):
        ###
        #############################################################################
        ### Argument handling: type check and guessed values
        #############################################################################
        ###
        ### convert binomial_ci_policy to a numeral if it is given as a string
        if isinstance(binomial_ci_policy, str):
            if binomial_ci_policy in self.binomial_ci_policy_dict:
                binomial_ci_policy = self.binomial_ci_policy_dict[binomial_ci_policy]
            else:
                raise ValueError(
                    "'binomial_ci_policy' preset should be one of 'conservative', 'conservative quartile', 'median', optimistic quartile', 'optimistic'."
                )
        elif issubclass(
            type(binomial_ci_policy), (float, int)
        ):  ## issubclass instead of isinstance to also match numpy subtypes (float_, float64, float32, etc.)
            ### check that the numerical value is between 0 and 1
            if (binomial_ci_policy < 0) or (binomial_ci_policy > 1):
                raise ValueError(
                    "'binomial_ci_policy' should be between 0 (conservative) and 1 (optimistic) if given as a numerical value."
                )
        else:
            raise TypeError(
                "'binomial_ci_policy' should be a numerical value between 0 and 1, or one of 'conservative', 'conservative quartile', 'median', optimistic quartile', 'optimistic'."
            )
        ### check matplotlib axes on which to draw
        if isinstance(ax, type(None)):
            ax = plt.gca()
        ### check all optional arguments with None as default value
        ### case where data is provided as a pandas DataFrame
        if isinstance(data, pandas.DataFrame):
            ### check variables that could have been declared as a column name from data
            ### replace them with the numerical series they refer to
            if isinstance(x, str) and (x in data.columns):
                x = data[x].copy()
            elif isinstance(x, str) and not (x in data.columns):
                raise ValueError(
                    f"'{x}' (the value provided for 'x') was not found in the columns of the dataframe."
                )
            ### if x and/or y have not been declared, look for the names 'x' and 'y' in data,
            ### or assume they are the first and second columns, respectively
            elif isinstance(x, type(None)):
                if "x" in data.columns:
                    x = data["x"].copy()
                elif len(data.columns) == 1:
                    ### special case: if data only contains one column, use the index for x
                    x = data.index.copy()
                elif len(data.columns) >= 2:
                    x = data[data.columns[0]].copy()
                else:
                    raise ValueError(
                        "x can only be implicit if 'data' has at least 1 column."
                    )
            if isinstance(y, str) and (y in data.columns):
                y = data[y].copy()
            elif isinstance(y, str) and not (y in data.columns):
                raise ValueError(
                    f"'{y}' (the value provided for 'y') was not found in the columns of the dataframe."
                )
            elif isinstance(y, type(None)):
                if "y" in data.columns:
                    y = data["y"].copy()
                elif len(data.columns) == 1:
                    ### special case: if data only contains one column, assume that column is y
                    y = data[data.columns[0]].copy()
                elif len(data.columns) >= 2:
                    y = data[data.columns[1]].copy()
                else:
                    raise ValueError(
                        "y can only be implicit if 'data' has at least 1 column."
                    )
            if isinstance(std, str) and (std in data.columns):
                std = data[std].copy()
            elif isinstance(std, str) and not (std in data.columns):
                raise ValueError(
                    f"'{std}' (the value provided for 'std') was not found in the columns of the dataframe."
                )
            if isinstance(lower, str) and (lower in data.columns):
                lower = data[lower].copy()
            elif isinstance(lower, str) and not (lower in data.columns):
                raise ValueError(
                    f"'{lower}' (the value provided for 'lower') was not found in the columns of the dataframe."
                )
            if isinstance(upper, str) and (upper in data.columns):
                upper = data[upper].copy()
            elif isinstance(upper, str) and not (upper in data.columns):
                raise ValueError(
                    f"'{upper}' (the value provided for 'upper') was not found in the columns of the dataframe."
                )
        else:
            ### if numerical values as first argument instead of data, take them as y. This might change later
            if isinstance(
                data,
                (
                    pandas.Series,
                    numpy.ndarray,
                    type(list),
                    type(tuple),
                )
                or issubclass(type(data), (float, int)),
            ):
                if isinstance(y, type(None)) and isinstance(
                    x, type(None)
                ):  ## guesswork... Might be removed or implemented further at a later stage
                    y = data
                    x = list(range(1, len(y) + 1))
            ### check variables that could have WRONGLY been declared as a column name from data without any data...
            if isinstance(x, str):
                raise TypeError(
                    "'x' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            if isinstance(y, str):
                raise TypeError(
                    "'y' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            elif isinstance(y, type(None)):
                raise ValueError("If 'data' is not provided, 'y' must be provided.")
            if isinstance(std, str):
                raise TypeError(
                    "'std' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            if isinstance(lower, str):
                raise TypeError(
                    "'lower' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
            if isinstance(upper, str):
                raise TypeError(
                    "'upper' can only be of type 'str' if 'data' is provided as a pandas DataFrame."
                )
        ### "kind" activates one or more toggles
        if isinstance(kind, list) or isinstance(kind, tuple):
            kind = list(kind)  ## make sure kind is a list of strings
        elif isinstance(kind, str) or isinstance(kind, type(None)):
            kind = list([kind])
        else:
            raise TypeError(
                "'kind' can only be of type 'str', 'tuple[str]', 'list[str]', or set to None."
            )
        for kind_i in kind:
            if kind_i == "lines":
                draw_lines = True
            elif kind_i == "bars":
                draw_bars = True
            elif kind_i == "area":
                fill_area = True
            elif kind_i == "scatterplot":
                plot_limits = True
            elif (kind_i == "none") or (isinstance(kind_i, type(None))):
                pass
            else:
                raise ValueError(
                    "Available kinds of confidence intervals: 'lines', 'bars', 'area', 'scatterplot', 'none'."
                )
        ### check type and value of orientation, as it is used to modulate the behavior of the calculations and methods
        if isinstance(orientation, str):
            if (orientation != "vertical") and (orientation != "horizontal"):
                raise ValueError(
                    "'orientation' can only be one of 'horizontal' or 'vertical'."
                )
        else:
            raise TypeError(
                "'orientations' should be of type 'str' (more precisely either 'horizontal' or 'vertical')."
            )
        ###
        #############################################################################
        ### Argument handling: type checking for x, y, data, and calculations
        #############################################################################
        ###
        ### Ensure the compatible formating of x and y numerical series
        y = pandas.Series(y)
        if isinstance(x, type(None)):
            x = y.index
        x = pandas.Series(x)
        ### check that x and y are of equal length
        if len(x) != len(y):
            raise ValueError("The 'x' and 'y' vectors should have the same length.")
        ### store unique values as they will be the base of the other calculations
        unique_x = pandas.Series(x.unique())
        unique_y = pandas.Series(y.unique())
        ### variables non registered (for now), only meant to simplify procedures
        if orientation == "vertical":
            ### default case
            original_axis = x
            original_opposite_axis = y
            unique_axis_name = "x"
            unique_axis = unique_x
            opposite_axis_name = "y"
            opposite_axis = pandas.Series(
                [y.loc[x == val_x].values for val_x in unique_x]
            )
        elif orientation == "horizontal":
            ### this could maybe be done in a more systematic way(?), but at least the current form is explicit
            original_axis = y
            original_opposite_axis = x
            unique_axis_name = "y"
            unique_axis = unique_y
            opposite_axis_name = "x"
            opposite_axis = pandas.Series(
                [x.loc[y == val_y].values for val_y in unique_y]
            )
        else:
            pass
        ### calculate mean, median, q1 and q3 for each horizontal or vertical series
        mean = pandas.Series(
            [
                original_opposite_axis.loc[original_axis == val_i].mean()
                for val_i in unique_axis
            ]
        )
        median = pandas.Series(
            [
                original_opposite_axis.loc[original_axis == val_i].median()
                for val_i in unique_axis
            ]
        )
        q1 = pandas.Series(
            [
                original_opposite_axis.loc[original_axis == val_i].quantile(0.25)
                for val_i in unique_axis
            ]
        )
        q3 = pandas.Series(
            [
                original_opposite_axis.loc[original_axis == val_i].quantile(0.75)
                for val_i in unique_axis
            ]
        )
        ### calculate std or get it from the provided arguments
        if isinstance(std, type(None)):
            ### calculate std or use different methods
            std = pandas.Series(
                [
                    original_opposite_axis.loc[original_axis == val_i].std()
                    for val_i in unique_axis
                ]
            ).fillna(0)
        elif issubclass(
            type(std), (float, int)
        ):  ## issubclass is used here to check numpy float types
            ### same std for the whole data
            std = pandas.Series(
                [std] * len(unique_axis)
            )  ## len(x) should be equal to len(y)
        elif isinstance(
            std, (pandas.Series, pandas.DataFrame, list, tuple, numpy.ndarray)
        ):
            ### each vertical (or horizontal) data series gets their own std, which is provided
            if len(std) == len(unique_axis):
                std = pandas.Series(std)
            elif len(std) == len(original_axis):
                ### Check for confusing duplicates
                if all(
                    [
                        (
                            std[numpy.roll(std[original_axis == val_i].index, 1)].values
                            == std[original_axis == val_i].values
                        ).all()
                        for val_i in unique_axis
                    ]
                ):
                    pass  ## everything looks fine
                else:
                    raise ValueError(
                        f"Different values of 'std' were provided for the same values of '{unique_axis_name}'."
                    )
            else:
                ### reminder: this only happens if lower and upper are None
                raise ValueError(
                    "The 'std' vector has a length that does not match the rest of the data."
                )
        else:
            ### note that the case of std provided as a column name in data was already addressed in the type check for data
            ### type error, most certainly
            raise TypeError(
                "'std' can only be of type 'int', 'float', 'list', 'tuple', 'numpy.ndarray', 'pandas.DataFrame', 'pandas.Series' (or 'str' matching a column name in data if data is provided as a dataframe)."
            )
        ### if any of lower or upper are provided, they take priority over std or any other method
        ### if any of lower or upper is None, estimate them with the requested method (ci_type argument)
        ### the values get stored in ci_df (local variable), and selected afterwards.
        if isinstance(lower, type(None)) or isinstance(upper, type(None)):
            if isinstance(ci_type, str):
                if ci_type == "std":
                    # lower = mean - std_multiplier * std
                    # upper = mean + std_multiplier * std
                    ci_df = vectorized_to_df(std_ci, opposite_axis, std_multiplier)
                elif ci_type == "ste":
                    ci_df = vectorized_to_df(ste_ci, opposite_axis, std_multiplier)
                else:
                    raise ValueError(f"ci_type '{ci_type}' is not implemented.")
            else:
                raise TypeError("'ci_type' can only be of type 'str'.")
        ### if provided, check for confusing duplicates in "lower". If not provided, take from calculated CI
        if isinstance(lower, type(None)):
            lower = ci_df[0]
        elif issubclass(type(lower), (float, int)):
            ### same lower for the whole data
            lower = pandas.Series([lower] * len(unique_axis))
        elif isinstance(
            lower, (pandas.Series, pandas.DataFrame, list, tuple, numpy.ndarray)
        ):
            ### each vertical (or horizontal) data series gets their own lower bound, which is provided
            if len(lower) == len(unique_axis):
                lower = pandas.Series(lower)
            elif len(lower) == len(original_axis):
                ### Check for confusing duplicates
                if all(
                    [
                        (
                            lower[
                                numpy.roll(lower[original_axis == val_i].index, 1)
                            ].values
                            == lower[original_axis == val_i].values
                        ).all()
                        for val_i in unique_axis
                    ]
                ):
                    pass  ## everything looks fine
                else:
                    raise ValueError(
                        f"Different values of 'lower' were provided for the same values of '{unique_axis_name}'."
                    )
            else:
                ### reminder: this only happens if lower and upper are None
                raise ValueError(
                    "The 'lower' vector has a length that does not match the rest of the data."
                )
        else:
            ### note that the case of lower provided as a column name in data was already addressed in the type check for data
            ### type error, most certainly
            raise TypeError(
                "'lower' can only be of type 'int', 'float', 'list', 'tuple', 'numpy.ndarray', 'pandas.DataFrame', 'pandas.Series' (or 'str' matching a column name in data if data is provided as a dataframe)."
            )
        ### if provided, check for confusing duplicates in "upper". If not provided, take from calculated CI
        if isinstance(upper, type(None)):
            upper = ci_df[1]
        elif issubclass(type(upper), (float, int)):
            ### same std for the whole data
            upper = pandas.Series([upper] * len(unique_axis))
        elif isinstance(
            upper, (pandas.Series, pandas.DataFrame, list, tuple, numpy.ndarray)
        ):
            ### each vertical (or horizontal) data series gets their own upper bound, which is provided
            if len(upper) == len(unique_axis):
                upper = pandas.Series(upper)
            elif len(upper) == len(original_axis):
                ### Check for confusing duplicates
                if all(
                    [
                        (
                            upper[
                                numpy.roll(upper[original_axis == val_i].index, 1)
                            ].values
                            == upper[original_axis == val_i].values
                        ).all()
                        for val_i in unique_axis
                    ]
                ):
                    pass  ## everything looks fine
                else:
                    raise ValueError(
                        f"Different values of 'upper' were provided for the same values of '{unique_axis_name}'."
                    )
            else:
                ### reminder: this only happens if lower and upper are None
                raise ValueError(
                    "The 'upper' vector has a length that does not match the rest of the data."
                )
        else:
            ### note that the case of upper provided as a column name in data was already addressed in the type check for data
            ### type error, most certainly
            raise TypeError(
                "'upper' can only be of type 'int', 'float', 'list', 'tuple', 'numpy.ndarray', 'pandas.DataFrame', 'pandas.Series' (or 'str' matching a column name in data if data is provided as a dataframe)."
            )
        ### ensure the type of lower and upper
        lower = pandas.Series(lower)
        upper = pandas.Series(upper)
        ###
        #############################################################################
        ### Argument handling: boolean checks and defaults for optional arguments
        #############################################################################
        ###
        ### if "sub" variables are None, they take the value of the "master" variable
        ### draw_lines
        if isinstance(draw_lower_line, type(None)):
            draw_lower_line = draw_lines
        if isinstance(draw_upper_line, type(None)):
            draw_upper_line = draw_lines
        ### lines_style
        if isinstance(lower_line_style, type(None)):
            lower_line_style = lines_style
        if isinstance(upper_line_alpha, type(None)):
            upper_line_style = lines_style
        ### lines_color
        if isinstance(lower_line_color, type(None)):
            lower_line_color = lines_color
        if isinstance(upper_line_color, type(None)):
            upper_line_color = lines_color
        ### lines_linewidth
        if isinstance(lower_line_linewidth, type(None)):
            lower_line_linewidth = lines_linewidth
        if isinstance(upper_line_linewidth, type(None)):
            upper_line_linewidth = lines_linewidth
        ### lines_alpha
        if isinstance(lower_line_alpha, type(None)):
            lower_line_alpha = lines_alpha
        if isinstance(upper_line_alpha, type(None)):
            upper_line_alpha = lines_alpha
        ### draw_bar_ends
        if isinstance(draw_bar_ends, type(None)):
            draw_bar_ends = draw_bars
        if isinstance(draw_lower_bar_end, type(None)):
            draw_lower_bar_end = draw_bar_ends
        if isinstance(draw_upper_bar_end, type(None)):
            draw_upper_bar_end = draw_bar_ends
        ### bar_ends_color
        if isinstance(bar_ends_color, type(None)):
            bar_ends_color = bars_color
        if isinstance(lower_bar_end_color, type(None)):
            lower_bar_end_color = bar_ends_color
        if isinstance(upper_bar_end_color, type(None)):
            upper_bar_end_color = bar_ends_color
        ### bar_ends_width has priority over bar_ends_ratio
        if isinstance(bar_ends_width, type(None)):
            bar_ends_width = (
                (numpy.max(unique_axis) - numpy.min(unique_axis) + 1)
                / len(unique_axis)
                * bar_ends_ratio
            )
        ### plot_limits
        if isinstance(plot_lower_limit, type(None)):
            plot_lower_limit = plot_limits
        if isinstance(plot_upper_limit, type(None)):
            plot_upper_limit = plot_limits
        ### plot_marker
        if isinstance(lower_plot_marker, type(None)):
            lower_plot_marker = (
                "2" if isinstance(plot_marker, type(None)) else plot_marker
            )
        if isinstance(upper_plot_marker, type(None)):
            upper_plot_marker = (
                "1" if isinstance(plot_marker, type(None)) else plot_marker
            )
        ### plot_color
        if isinstance(lower_plot_color, type(None)):
            lower_plot_color = plot_color
        if isinstance(upper_plot_color, type(None)):
            upper_plot_color = plot_color
        ### plot_size
        if isinstance(lower_plot_size, type(None)):
            lower_plot_size = plot_size
        if isinstance(upper_plot_size, type(None)):
            upper_plot_size = plot_size
        ### plot_alpha
        if isinstance(lower_plot_alpha, type(None)):
            lower_plot_alpha = plot_alpha
        if isinstance(upper_plot_alpha, type(None)):
            upper_plot_alpha = plot_alpha
        ###
        #############################################################################
        ### Instance preparation: saving variables and parameters
        #############################################################################
        ###
        self.data = data
        self.x = x
        self.y = y
        self.unique_x = unique_x
        self.unique_y = unique_y
        self.lower = lower
        self.upper = upper
        self.std = std
        ### other calculated values
        self.mean = mean
        self.median = median
        self.q1 = q1
        self.q3 = q3
        ### Save all toggles in a dictionary
        self.params = {
            "kind": kind,
            "ci_type": ci_type,
            "extrapolation_type": extrapolation_type,
            "std_multiplier": std_multiplier,
            "orientation": orientation,
            "draw_lines": draw_lines,  ## currently not needed, but kept for now in case it would be needed later
            "draw_lower_line": draw_lower_line,
            "draw_upper_line": draw_upper_line,
            "lines_style": lines_style,
            "lower_line_style": lower_line_style,
            "upper_line_style": upper_line_style,
            "lines_color": lines_color,
            "lower_line_color": lower_line_color,
            "upper_line_color": upper_line_color,
            "lines_linewidth": lines_linewidth,
            "lower_line_linewidth": lower_line_linewidth,
            "upper_line_linewidth": upper_line_linewidth,
            "lines_alpha": lines_alpha,
            "lower_line_alpha": lower_line_alpha,
            "upper_line_alpha": upper_line_alpha,
            "draw_bars": draw_bars,
            "draw_bar_ends": draw_bar_ends,
            "draw_lower_bar_end": draw_lower_bar_end,
            "draw_upper_bar_end": draw_upper_bar_end,
            "bars_style": bars_style,
            "bars_color": bars_color,
            "bars_linewidth": bars_linewidth,
            "bars_alpha": bars_alpha,
            "bar_ends_style": bar_ends_style,
            "bar_ends_color": bar_ends_color,
            "lower_bar_end_color": lower_bar_end_color,
            "upper_bar_end_color": upper_bar_end_color,
            "bar_ends_width": bar_ends_width,
            "bar_ends_ratio": bar_ends_ratio,
            "hide_bars_center_portion": hide_bars_center_portion,
            "bars_center_portion_length": bars_center_portion_length,
            "bars_center_portion_ratio": bars_center_portion_ratio,
            "fill_area": fill_area,
            "fill_color": fill_color,
            "fill_alpha": fill_alpha,
            "plot_limits": plot_limits,
            "plot_lower_limit": plot_lower_limit,
            "plot_upper_limit": plot_upper_limit,
            "plot_marker": plot_marker,
            "lower_plot_marker": lower_plot_marker,
            "upper_plot_marker": upper_plot_marker,
            "plot_color": plot_color,
            "lower_plot_color": lower_plot_color,
            "upper_plot_color": upper_plot_color,
            "plot_alpha": plot_alpha,
            "lower_plot_alpha": lower_plot_alpha,
            "upper_plot_alpha": upper_plot_alpha,
            "plot_size": plot_size,
            "lower_plot_size": lower_plot_size,
            "upper_plot_size": upper_plot_size,
            "binomial_ci_policy": binomial_ci_policy,
        }
        self.ax = ax  # ok
        ###
        #############################################################################
        ### Instance preparation: method call(s) upon initialization
        #############################################################################
        ###
        self.draw()

    def __call__(self):
        pass

    ### dictionary for binomial_ci_policy
    binomial_ci_policy_dict = {
        "conservative": 0,
        "conservative quartile": 0.25,
        "median": 0.5,
        "optimistic quartile": 0.75,
        "optimistic": 1,
    }

    def help():
        print("A help message")

    def draw(self) -> None:  ## return ax instead? Or None?
        """Draws a confidence interval using seaborn and matplotlib."""
        if self.params["orientation"] == "vertical":
            ### draw CI lines
            if self.params["draw_lower_line"] == True:
                seaborn.lineplot(
                    x=self.unique_x,
                    y=self.lower,
                    color=self.params["lower_line_color"],
                    linestyle=self.params["lower_line_style"],
                    linewidth=self.params["lower_line_linewidth"],
                    alpha=self.params["lower_line_alpha"],
                )
            if self.params["draw_upper_line"] == True:
                seaborn.lineplot(
                    x=self.unique_x,
                    y=self.upper,
                    color=self.params["upper_line_color"],
                    linestyle=self.params["upper_line_style"],
                    linewidth=self.params["upper_line_linewidth"],
                    alpha=self.params["upper_line_alpha"],
                )
            ### draw ci bars
            if self.params["draw_bars"] == True:
                if self.params["hide_bars_center_portion"] == True:
                    if isinstance(
                        self.params["bars_center_portion_length"], type(None)
                    ):  ## the length has priority over the ratio
                        bars_half_length = (
                            (self.upper - self.lower)
                            * (1 - self.params["bars_center_portion_ratio"])
                            / 2
                        )  ## with ratio
                    else:
                        bars_half_length = (
                            self.upper
                            - self.lower
                            - self.params["bars_center_portion_length"]
                        ) / 2  ## with length
                    ### lower half
                    plt.vlines(
                        x=self.unique_x,
                        ymin=self.lower,
                        ymax=self.lower + bars_half_length,
                        color=self.params["bars_color"],
                        linestyles=self.params["bars_style"],
                        linewidth=self.params["bars_linewidth"],
                        alpha=self.params["bars_alpha"],
                    )
                    ### upper half
                    plt.vlines(
                        x=self.unique_x,
                        ymin=self.upper - bars_half_length,
                        ymax=self.upper,
                        color=self.params["bars_color"],
                        linestyles=self.params["bars_style"],
                        linewidth=self.params["bars_linewidth"],
                        alpha=self.params["bars_alpha"],
                    )
                else:
                    plt.vlines(
                        x=self.unique_x,
                        ymin=self.lower,
                        ymax=self.upper,
                        color=self.params["bars_color"],
                        linestyles=self.params["bars_style"],
                        linewidth=self.params["bars_linewidth"],
                        alpha=self.params["bars_alpha"],
                    )
                ### draw bar ends
                if self.params["draw_bar_ends"] == True:
                    if self.params["draw_lower_bar_end"] == True:
                        plt.hlines(
                            y=self.lower,
                            xmin=self.unique_x - self.params["bar_ends_width"] / 2,
                            xmax=self.unique_x + self.params["bar_ends_width"] / 2,
                            color=self.params["lower_bar_end_color"],
                            linestyles=self.params["bar_ends_style"],
                            linewidth=self.params["bars_linewidth"],
                            alpha=self.params["bars_alpha"],
                        )
                    if self.params["draw_upper_bar_end"] == True:
                        plt.hlines(
                            y=self.upper,
                            xmin=self.unique_x - self.params["bar_ends_width"] / 2,
                            xmax=self.unique_x + self.params["bar_ends_width"] / 2,
                            color=self.params["upper_bar_end_color"],
                            linestyles=self.params["bar_ends_style"],
                            linewidth=self.params["bars_linewidth"],
                            alpha=self.params["bars_alpha"],
                        )
            ### fill CI area
            if self.params["fill_area"] == True:
                plt.fill_between(
                    x=self.unique_x,
                    y1=self.lower,
                    y2=self.upper,
                    color=self.params["fill_color"],
                    alpha=self.params["fill_alpha"],
                )

            ### scatterplot of CI limits
            if self.params["plot_lower_limit"] == True:
                seaborn.scatterplot(
                    x=self.unique_x,
                    y=self.lower,
                    color=self.params["lower_plot_color"],
                    s=self.params["lower_plot_size"],
                    marker=self.params["lower_plot_marker"],
                    alpha=self.params["lower_plot_alpha"],
                )
            if self.params["plot_upper_limit"] == True:
                seaborn.scatterplot(
                    x=self.unique_x,
                    y=self.upper,
                    color=self.params["upper_plot_color"],
                    s=self.params["upper_plot_size"],
                    marker=self.params["upper_plot_marker"],
                    alpha=self.params["upper_plot_alpha"],
                )
        elif self.params["orientation"] == "horizontal":
            ### draw CI lines
            if self.params["draw_lower_line"] == True:
                seaborn.lineplot(
                    x=self.lower,
                    y=self.unique_y,
                    color=self.params["lower_line_color"],
                    linestyle=self.params["lower_line_style"],
                    linewidth=self.params["lower_line_linewidth"],
                    alpha=self.params["lower_line_alpha"],
                    orient="y",
                )
            if self.params["draw_upper_line"] == True:
                seaborn.lineplot(
                    x=self.upper,
                    y=self.unique_y,
                    color=self.params["upper_line_color"],
                    linestyle=self.params["upper_line_style"],
                    linewidth=self.params["upper_line_linewidth"],
                    alpha=self.params["upper_line_alpha"],
                    orient="y",
                )
            ### draw ci bars
            if self.params["draw_bars"] == True:
                if self.params["hide_bars_center_portion"] == True:
                    if isinstance(
                        self.params["bars_center_portion_length"], type(None)
                    ):  ## the length has priority over the ratio
                        bars_half_length = (
                            (self.upper - self.lower)
                            * (1 - self.params["bars_center_portion_ratio"])
                            / 2
                        )  ## with ratio
                    else:
                        bars_half_length = (
                            self.upper
                            - self.lower
                            - self.params["bars_center_portion_length"]
                        ) / 2  ## with length
                    ### lower half
                    plt.hlines(
                        y=self.unique_y,
                        xmin=self.lower,
                        xmax=self.lower + bars_half_length,
                        color=self.params["bars_color"],
                        linestyles=self.params["bars_style"],
                        linewidth=self.params["bars_linewidth"],
                        alpha=self.params["bars_alpha"],
                    )
                    ### upper half
                    plt.hlines(
                        y=self.unique_y,
                        xmin=self.upper - bars_half_length,
                        xmax=self.upper,
                        color=self.params["bars_color"],
                        linestyles=self.params["bars_style"],
                        linewidth=self.params["bars_linewidth"],
                        alpha=self.params["bars_alpha"],
                    )
                else:
                    plt.hlines(
                        y=self.unique_y,
                        xmin=self.lower,
                        xmax=self.upper,
                        color=self.params["bars_color"],
                        linestyles=self.params["bars_style"],
                        linewidth=self.params["bars_linewidth"],
                        alpha=self.params["bars_alpha"],
                    )
                ### draw bar ends
                if self.params["draw_bar_ends"] == True:
                    if self.params["draw_lower_bar_end"] == True:
                        plt.vlines(
                            x=self.lower,
                            ymin=self.unique_y - self.params["bar_ends_width"] / 2,
                            ymax=self.unique_y + self.params["bar_ends_width"] / 2,
                            color=self.params["lower_bar_end_color"],
                            linestyles=self.params["bar_ends_style"],
                            linewidth=self.params["bars_linewidth"],
                            alpha=self.params["bars_alpha"],
                        )
                    if self.params["draw_upper_bar_end"] == True:
                        plt.vlines(
                            x=self.upper,
                            ymin=self.unique_y - self.params["bar_ends_width"] / 2,
                            ymax=self.unique_y + self.params["bar_ends_width"] / 2,
                            color=self.params["upper_bar_end_color"],
                            linestyles=self.params["bar_ends_style"],
                            linewidth=self.params["bars_linewidth"],
                            alpha=self.params["bars_alpha"],
                        )
            ### fill CI area
            if self.params["fill_area"] == True:
                plt.fill_betweenx(
                    y=self.unique_y,
                    x1=self.lower,
                    x2=self.upper,
                    color=self.params["fill_color"],
                    alpha=self.params["fill_alpha"],
                )

            ### scatterplot of CI limits
            if self.params["plot_lower_limit"] == True:
                seaborn.scatterplot(
                    x=self.lower,
                    y=self.unique_y,
                    color=self.params["lower_plot_color"],
                    s=self.params["lower_plot_size"],
                    marker=self.params["lower_plot_marker"],
                    alpha=self.params["lower_plot_alpha"],
                )
            if self.params["plot_upper_limit"] == True:
                seaborn.scatterplot(
                    x=self.upper,
                    y=self.unique_y,
                    color=self.params["upper_plot_color"],
                    s=self.params["upper_plot_size"],
                    marker=self.params["upper_plot_marker"],
                    alpha=self.params["upper_plot_alpha"],
                )
        else:
            pass  ## if orientation is neiher horizontal nor vertical

    def as_dataframe(self):
        """Returns a dataframe with calculated values."""
        if self.params["orientation"] == "vertical":
            unique_axis = self.unique_x
            unique_axis_name = "x"
            opposite_axis = pandas.Series(
                [self.y.loc[self.x == val_x].values for val_x in self.unique_x]
            )
            opposite_axis_name = "y"
        elif self.params["orientation"] == "horizontal":
            unique_axis = self.unique_y
            unique_axis_name = "y"
            opposite_axis = pandas.Series(
                [self.x.loc[self.y == val_y].values for val_y in self.unique_y]
            )
            opposite_axis_name = "x"
        else:
            pass  ## undefined, will probably throw a ValueError before reaching this part
        calculated_data = pandas.DataFrame(
            {
                unique_axis_name: unique_axis,
                "lower": self.lower,
                "upper": self.upper,
                "mean": self.mean,
                "std": self.std,
                # "ste": self.ste,
                "median": self.median,
                "q1": self.q1,
                "q3": self.q3,
                "ci_type": [self.params["ci_type"]] * len(unique_axis),
                opposite_axis_name: opposite_axis,
            }
        )
        return calculated_data
