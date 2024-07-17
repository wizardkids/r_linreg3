"""
    Filename: r_linreg.py
     Version: 3.00
      Author: Richard E. Rawson
        Date: 2024-07-16
 Description: Wrapper for statsmodels linear regression that not only performs regression but makes a long list of intermediary statistics accessible to the user.

     SOURCE:
            Applied Linear Regression, Sandy Weisberg, John Wiley & Sons, 1985
            https://online.stat.psu.edu/stat501

DESCRIPTION:
            This program is a wrapper for linear regression performed by statsmodels. In addition to returning a regression model, the program can report virtually every intermediary and end result of that computation. The program uses statsmodels, but the user does not need to know how to use that package. Instead, the main function, linreg() takes two parameters, X and y, and computes everything most users would care to know, and more.

            The purpose of this module is not speed or versatility. The goals are very restricted and are:

                (1) Provide easy access to linear regression analysis (see "EXAMPLE USAGE" below). X and y data can be passed to linreg() in several different formats, described in detail below. "Easy" means there is a single command that takes one or more "X" variable(s) and a "y" variable. "Easy" also means that r_linreg can take "X" and "y" in flexible formats.

                (2) Underlying parameters generated by regression analysis can be retrieved easily. See definitions() or calculations() for a complete list of statistical parameters.

      NOTES:
            (1) Other forms of regression including Logistic Regression, Stepwise Regression, Ridge Regression, Lasso Regression, and ElasticNet Regression are not addressed in this module.

            (2) An intercept is optional, but included by default.

STATSMODELS:
    https://www.statsmodels.org/dev/examples/notebooks/generated/formulas.html

    from statsmodels.formula.api import ols

    -- example of OLS by way of R-like formula:

    model =  ols(formula="Lottery ~ Literacy + Wealth + Literacy*Wealth", data=df)

        where: df is a pandas DataFrame containing Literacy, Wealth (X columns), and Lottery (y) columns.

    model_results = model.fit()

    fit() returns RegressionResults (here, in the variable "model_results")

    See:
    https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.RegressionResults.html#statsmodels.regression.linear_model.RegressionResults

DATA INPUTS:
    - X: python list, pandas.Series, or pandas.DataFrame -- [int, float]
    - y: python list, pandas.Series, or pandas.DataFrame -- [int, float]

    - Data (X and y) are examined for validity of format and content, and converted to pandas.DataFrame.
    - Python lists are converted to pandas.DataFrame before computations are conducted.
    - For Series and DataFrames, the index is reset to 1 for cases where X or y comprise a subset of the original pandas data.
    - For multiple regression, with more than one X variable, n-dimensional lists can be used, but for simplicity's sake, use pandas.DataFrames for input. Formatting a multi-dimension list so that rows and columns are what is expected can be challenging, but a DataFrame makes organizing data correctly very easy.

=========== EXAMPLE USAGE =====================================================

# BUG -- the following needs to be edited in light of refactoring.

For details, use usage()

    >>> import r_linreg as linreg
    >>> import reports
    >>> import info
    >>> import methods

>>> results = linreg.linreg(X, y)  # X and y, as described above

>>> results['r_squared']       # access individual parameters (quotes required)
0.9949660912754924

>>> reports.summary(results)    # print a summary of the regression parameters

>>> reports.report(results)     # print all variables and values, computed during analysis
n: 17
k: 1
sumx: 3450.2
sumx2: 700759.02
sumxy: 482143.511
sumy: 2373.3
sumy2: 331754.4034
x_bar: 202.95294117647057
y_bar: 139.6058823529412
SXX: 530.7823529411756
SXY: 475.2957058823527
SYY: 427.76281176470604
    ...


    ! Entry point for submission of data (X and y variables).
    ! Determine if submitted data is valid for multiple linear regression.
    ! Data are rejected if they don't fit the specified criteria, along with information about how to fix things, if possible
"""

import sys
import warnings
from collections import OrderedDict
from typing import Any
from typing import OrderedDict as ODictType

import info
import numpy as np
import pandas as pd
from icecream import ic
from patsy import PatsyError
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.stattools import durbin_watson
from statsmodels.tools import add_constant

warnings.filterwarnings(action="ignore", module="statsmodels")

print()


def linreg(x: list | pd.Series | pd.DataFrame, y: list | pd.Series | pd.DataFrame, const=True) -> OrderedDict[str, list | str]:
    """
    This is the entry point for the r_linreg package. linreg() first sends data to validate_data() to reject bad data types and contents. Then x,y are sent to clean_x_data() and clean_y_data() to modify x and y, as needed. Finally, a model is created and regression analysis is performed via multiple_regr().

    Parameters
    ----------
    x : list | pd.Series | pd.DataFrame -- [int, float, np.int32, np.int64, np.float32, np.float64, '%Y-%m-%d', or datetime]
    y : list | pd.Series | pd.DataFrame -- [int, float, np.int32, np.int64, np.float32, np.float64, '%Y-%m-%d', or datetime]
    const : bool, optional -- default is True; determines whether or not to include a constant in the regression analysis

    Returns
    -------
    OrderedDict[str, list | str] -- dictionary of 52 linear regression statistics either calculated or revealed by statsmodels

    Notes:
        - When using a python list for the x variable(s), it is best to use a single dimension list. For lists of more than one dimension, you will have fewer problems if you convert your data to a pandas.DataFrame first. This will ensure that the original list was in the correct (expected) format.
    """

    # If data are not validated, the program will have exited after validate_data().
    validate_data(x, y)

    # Convert x data to pandas DataFrame.
    x = clean_x_data(x)

    # Convert y data to pandas DataFrame.
    y = clean_y_data(y)

    # Final check for proper shape and contents of x and y data. If check fail, the program will have exited already.
    x, y = final_check(x, y)

    all_stats: ODictType[str, Any] = multiple_regr(x, y, const)

    return all_stats
    # return None


def validate_data(x: list | pd.Series | pd.DataFrame, y: list | pd.Series | pd.DataFrame) -> None:
    """
    Validate data structures and x,y contents.
        -- x and y can't be empty
        -- x and y must be of types pandas DataFrame, pandas Series, and/or list

    caveat emptor:
        x can contain text, but only such text that can be converted using transform.encode() or transform.dummy() functions. If x contains text that can't be thusly converted, the program will generate an error and exit... possibly ungracefully.
    """

    # Validate x and y data types as list, Series, or DataFrames
    x_type_valid: bool = isinstance(x, (pd.Series, pd.DataFrame, list))
    y_type_valid: bool = isinstance(y, (pd.Series, pd.DataFrame, list))
    if not x_type_valid or not y_type_valid:
        print("x and y must be of type list, pandas Series, or pandas DataFrame.")
        exit()

    # x and y can't be empty.
    if len(x) == 0 or len(y) == 0:
        print("\nx or y contains no data.")
        exit()

    # y can't be a DataFrame with more than 1 column or a list of >1 dimension.
    if isinstance(y, pd.DataFrame) and len(y.columns) > 1:
        print("\ny must be a 1-dimensional list or pandas Series.")
        exit()


def clean_x_data(_x: list | pd.Series | pd.DataFrame) -> pd.DataFrame:
    """
    A function to clean and format input data _x, which can be a list, pandas Series, or pandas DataFrame, into a standardized pandas DataFrame format.
    If _x is a DataFrame, resets the index.
    If _x is a Series, converts it to a DataFrame and resets the index.
    If _x is a list, converts it to a DataFrame, assigns human-readable column names.

    Parameters
    ----------
    _x : list | pd.Series | pd.DataFrame -- Input data that needs to be cleaned and formatted.
    Returns:

    Returns
    -------
    x : pd.DataFrame -- The cleaned and formatted input data in the form of a pandas DataFrame.
    """

    # If x is a DataFrame, we don't need to do anything besides reset the index to integers starting at -0-. drop=True prevents the current index from being added as a column.
    if isinstance(_x, pd.DataFrame):
        x = _x.reset_index(drop=True)

    #  If x is a pd.Series, convert the Series to a DataFrame and reset the index.
    elif isinstance(_x, pd.Series):
        x: pd.DataFrame = pd.DataFrame(_x)
        x: pd.DataFrame = x.reset_index(drop=True)

    # If x is a python list, convert to a pandas.DataFrame.
    elif isinstance(_x, list):

        # Convert a python n-dimension list to a DataFrame.
        x: pd.DataFrame = pd.DataFrame(_x)

        # Column names in a DataFrame made from a [list] are ints. These are converted to more human-readable strings in the form of x_variable1, x_variable2...
        for old_label in range(len(list(x.columns))):
            new_label: str = f'x_variable{old_label + 1}'
            x: pd.DataFrame = x.rename(columns={old_label: new_label})

    return x


def clean_y_data(_y: list | pd.Series | pd.DataFrame) -> pd.DataFrame:
    """
    A function to clean and format input data _y, which can be a list, pandas Series, or pandas DataFrame, into a standardized pandas DataFrame format.
    If _y is a DataFrame, resets the index.
    If _y is a Series, converts it to a DataFrame and resets the index.
    If _y is a list, converts it to a DataFrame, assigns human-readable column names.

    Parameters
    ----------
    _y : list | pd.Series | pd.DataFrame -- Input data that needs to be cleaned and formatted.
    Returns:

    Returns
    -------
    y : pd.DataFrame -- The cleaned and formatted input data in the form of a pandas DataFrame.
    """

    # If y is a DataFrame, we don't need to do anything besides reset the index to integers starting at -0-. drop=True prevents the current index from being added as a column.
    if isinstance(_y, pd.DataFrame):
        y = _y.reset_index(drop=True)

    #  If y is a pd.Series, convert the Series to a DataFrame and reset the index.
    elif isinstance(_y, pd.Series):
        y: pd.DataFrame = pd.DataFrame(_y)
        y: pd.DataFrame = y.reset_index(drop=True)

    # If x is a python list, convert to a pandas.DataFrame.
    elif isinstance(_y, list):

        # Convert y as a 1-dimension list to a DataFrame.
        y: pd.DataFrame = pd.DataFrame(_y)

        # Column names in a DataFrame made from a [list] are ints. Change the column name to a generic "y"
        y: pd.DataFrame = y.rename(columns={0: 'y'})

    return y


def final_check(x: pd.DataFrame, y: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    At this point, we should have two DataFrames, one for the x variable(s) and one for the y variable. We need to do some error checking.
            (1) Are the columns of data either floats or ints?
                    If not, attempt conversion from strings to numbers.
            (2) Does y have only one column?
            (3) Are x and y the same length?

    Parameters:
    -------
        x : pd.DataFrame - Input DataFrames for x values.
        y : pd.DataFrame - Input DataFrames for y values.

    Returns:
    -------
        tuple[pd.DataFrame, pd.DataFrame] - The processed x and y data frames.
    """

    # (1) Are the columns of data in x and y either float or int or can they be converted to float or int? Note that columns with numeric strings can be converted to floats.
    try:
        # If x contains > 1 column, all columns will be converted to float64.
        x: pd.DataFrame = x.astype(dtype=np.float64)
    except ValueError:
        print('Could not convert string in "x" to float.')
        sys.exit()

    try:
        y: pd.DataFrame = y.astype(dtype=np.float64)
    except ValueError:
        print('Could not convert string in "y" DataFrame to float.')
        sys.exit()

    # (2) Does y have only one column?
    if y.shape[1] != 1:
        print("y can only have one column.")
        print()
        print(y.head())
        sys.exit()

    # (3) Are x and y the same length?
    if x.shape[0] != y.shape[0]:
        print("x shape:", x.shape)
        print(x.tail())
        print()
        print("y shape:", y.shape)
        print(y.tail())
        print("x and y do not have equal numbers of items.")
        sys.exit()

    return x, y


def create_model(x_data: pd.DataFrame, y_data: pd.DataFrame, include_constant: bool):
    """
    Create the statsmodel model for x_data and y_data.

    Parameters
    ----------
    x_data : pd.DataFrame -- 1 or more x variables
    y_data : pd.DataFrame -- the y variable
    include_constant : bool -- True if a constant should be included

    Returns
    -------
    RegressionResultsWrapper -- statsmodels fitted model
    """

    # Add a constant column to x_data if include_constant == True.
    if include_constant:
        x_data = add_constant(data=x_data)

    # Concatenate x_data and y_data to create the dataframe.
    df = pd.concat([x_data, y_data], axis=1)

    # Create the "formula"
    formula = "y_data ~ " + " + ".join(x_data.columns[1:]) if include_constant else "y_data ~ " + " + ".join(x_data.columns)

    try:
        # Create the statsmodels model.
        model = ols(formula, df)

    # If there is an error, print a message and exit.
    except (PatsyError, ValueError) as err:
        print("\nRegression analysis cannot be run.\nData contain one or more non-numeric values.\n")
        print(err)
        exit()

    # Fit the model and return the results.
    return model.fit()


def multiple_regr(X: pd.DataFrame, y: pd.DataFrame, const: bool) -> ODictType[str, Any]:
    """
    Some computations are done "by hand" [e.g., x_bar is calculated as the X.mean()] and statsmodels is used to conduct conputations where needed. All regression parameters are stored in {all_stats}.

    Parameters
    ----------
    X : pd.DataFrame -- one or more independent variables
    y : pd.DataFrame -- response (dependent) variable
    const : bool -- if True, include a constant

    Returns
    -------
    all_stats ODictType[str, Any] -- dictionary containing 52 statistical parameters
    """

    # Preserve the original X and y DataFrames for insertion into {all_stats}.
    X_original: pd.DataFrame = X.copy()
    y_original: pd.DataFrame = y.copy()

    # Fit the model.
    model_results = create_model(X, y, const)

    # Get Stepwise ANOVA table. See anova() docstring for comments on anova types.
    anova_results = anova_lm(model_results, typ=1)

    # statsmodels' OLS Regression Results table.
    anova_summary = model_results.summary()

    # Get the correlation matrix of X and y variables.
    all_vars: pd.DataFrame = pd.concat([X, y], axis=1)
    corr_matrix: pd.DataFrame = all_vars.corr()

    # rename_columns() provides generic column headings  to make the following calculations simpler.
    X = rename_columns(X, const)
    y.columns = ["yi"]

    # Parameter estimates
    params = model_results.params.to_list()

    # number of observations
    n: float = model_results.nobs

    # Derive the various degrees of freedom quantities.
    DFM: int = len(params)  # degrees of freedom of the model
    DFR: float = n - DFM  # degrees of freedom of the residuals
    DFT: float = n - 1  # total degrees of freedom
    k = model_results.df_model  # degrees of freedom

    # DataFrame of residuals of the model.
    residuals = model_results.resid.to_frame()
    residuals = residuals.rename(columns={0: 'residuals'})

    # Get the Durbin-Watson statistic.
    dw: np.float64 = durbin_watson(model_results.resid)

    # DataFrame of fitted values.
    fitted_values = model_results.fittedvalues.to_frame()
    fitted_values: pd.DataFrame = fitted_values.rename(
        columns={0: 'fitted_values'})

    # -- Calculate the total, model, and residual sum of squared:
    # total, or cumulative, sum of squares; sum of yi - y_bar
    SS_total: np.float64 = model_results.centered_tss if const else model_results.uncentered_tss

    # sum of squares for the model (or regression)
    SS_model: np.float64 = model_results.ess

    # Sum of squared residuals
    RSS: np.float64 = model_results.ssr

    # Average difference between the observed and fitted values: mean squared error of the model or residual mean square
    MSE_residuals: float = model_results.mse_resid
    MSE: float = MSE_residuals
    # Average difference between the observed values and the mean of those values.
    MSE_model: np.float64 = model_results.mse_model

    # MSE_total: The uncentered total sum of squares divided by the number of observations.
    MSE_total: np.float64 = model_results.mse_total

    # SEE: standard error of the estimate; measures variation in the ei's
    SEE: np.float64 = np.sqrt(MSE_residuals)

    r_squared: np.float64 = model_results.rsquared  # R-squared of the model.
    # Adjusted R-squared.
    r_squared_adj: np.float64 = model_results.rsquared_adj
    F: np.float64 = model_results.fvalue  # F value
    F_pvalue: np.float64 = model_results.f_pvalue  # p value for F

    # t-statistic for a given parameter estimate.
    t_statistics: list[float] = model_results.tvalues.to_list()

    # The two-tailed p values for the t-stats of the params.
    t_pvalues: list[float] = model_results.pvalues.to_list()

    # mean of y
    y_bar: float = y["yi"].mean()

    # "SYY": "sum((yi - y_bar)^2)"
    SYY: np.float64 = np.sum((y["yi"] - y_bar) ** 2)

    # "sumy": "sum(yi)"
    sumy: np.float64 = y["yi"].sum()

    # "sumy2": "sum((yi)**2)"
    sumy2: np.float64 = (y["yi"] ** 2).sum()

    # ----- PROCESS THE X VARIABLES INTO lists -----

    col_names = list(X.columns)

    # mean of each column in X
    x_bar_series = X.mean()
    x_bar: list[float] = x_bar_series.tolist()

    # "sumx": "sum(xi)" for each column in X
    sumx_series = X.sum()
    sumx: list[float] = sumx_series.tolist()

    # "sumx2": "sum((xi**2))" for each column in X
    sumx2: list[np.float64] = [(X[col] ** 2).sum(axis=0) for col in col_names]

    # "sumxy": "sum(xi * yi)" for each column in X.
    sumxy: list[np.float64] = [(X[col] * y['yi']).sum() for col in col_names]

    # "SXX": "sum((xi - x_bar)^2)" for each column in X.
    SXX: list[np.float64] = [np.sum((X[col] - x_bar[X.columns.get_loc(col)]) ** 2, axis=0) for col in col_names]

    # "SXY": "sum((xi - x_bar) * (yi - y_bar))" for each column in X.
    SXY: list[np.float64] = [((X[col] - x_bar[X.columns.get_loc(col)]) *
                              (y['yi'] - y_bar)).sum() for col in col_names]

    # standard errors of the parameter estimates.
    SE_coefficients: list[float] = model_results.bse.to_list()

    # correlation coefficient
    correlation: np.float64 = np.sqrt(r_squared)

    # covariance matrix
    cov_matrix: pd.DataFrame = model_results.cov_params()

    all_data = {
        "model_results": model_results,
        "x_variable_names": list(X_original.columns),
        "y_variable_name": list(y_original.columns)[0],
        "n": n,
        "y": y,
        "X": X,
        "sumx": sumx,
        "sumy": sumy,
        "sumxy": sumxy,
        "sumx2": sumx2,
        "sumy2": sumy2,
        "x_bar": x_bar,
        "y_bar": y_bar,
        "SXX": SXX,
        "SYY": SYY,
        "SXY": SXY,
        "anova": anova_results,
        "anova_summary": anova_summary,
        "coefficients": params,
        "intercept": params[0],
        "slope": params[1:],
        "SE_coefficients": SE_coefficients,
        "std_error_b0": SE_coefficients[0],
        "std_error_b1": SE_coefficients[1:],
        "t_statistics": t_statistics,
        "t_pvalues": t_pvalues,
        "t_intercept": t_statistics[0],
        "t_intercept_p": t_pvalues[0],
        "t_slope": t_statistics[1:],
        "t_slope_p": t_pvalues[1:],
        "DFM": DFM,
        "DFR": DFR,
        "DFT": DFT,
        "k": k,
        "SS_model": SS_model,
        "RSS": RSS,
        "SS_total": SS_total,
        "MSE_total": MSE_total,
        "MSE_model": MSE_model,
        "MSE": MSE,
        "SEE": SEE,
        "r_squared": r_squared,
        "r_squared_adj": r_squared_adj,
        "correlation": correlation,
        "F": F,
        "F_pvalue": F_pvalue,
        "Durbin-Watson": dw,
        "corr_matrix": corr_matrix,
        "cov_matrix": cov_matrix,
        "fitted_values": fitted_values,
        "residuals": residuals,
        "const": const,
    }

    # Create a list of keys in the order the we want items to appear when iterated.
    vars_list: list[list[str]] = info.included_vars()
    key_list = []
    for i in vars_list:
        for j in i:
            key_list.append(j)

    # ! =======================================================================
    #! The following is for the developer only. It checks that I haven't added a key to {all_data} and forgotten to include it in the list in included_vars() or vice versa.
    for k in all_data.keys():
        if k not in key_list:
            print(f'The key "{k}" from all_data was not found in included_vars().')
            sys.exit()
    for k in key_list:
        if k not in all_data.keys():
            print(f'The key "{k}" from included_vars() was not found in all_data.')
            sys.exit()
    # ! ======================================================================

    # Create the ordered dictionary. The reports() function requires that {all_stats} maintains a set order.
    all_stats: ODictType[str, Any] = OrderedDict((k, all_data[k]) for k in key_list)

    return all_stats


def rename_columns(df: pd.DataFrame, has_constant: bool) -> pd.DataFrame:
    """
    Renames columns in the data_frame to generic "x_variable1", "x_variable2",
    and so on, making references to columns in the DataFrame more generic.

    If has_constant is True, the first column is not renamed.

    Parameters
    ----------
    data_frame : pd.DataFrame -- target dataframe
    has_constant : bool -- True if there is a constant term (column)

    Returns
    -------
    pd.DataFrame -- dataframe with renamed columns
    """

    new_names = {col: col for col in df.columns}
    if has_constant:
        new_names.update({col: f'X{i + 1}' for i, col in enumerate(df.columns[1:])})
    else:
        new_names.update({col: f'X{i + 1}' for i, col in enumerate(df.columns)})

    return df.rename(columns=new_names)


if __name__ == "__main__":
    """
    "Forbes data" obtained from "Applied Linear Regression" by Weisberg
    """
    print()

    x: list[float] = [
        194.5,
        194.3,
        197.9,
        198.4,
        199.4,
        199.9,
        200.9,
        201.1,
        201.4,
        201.3,
        203.6,
        204.6,
        209.5,
        208.6,
        210.7,
        211.9,
        212.2
    ]

    y: list[float] = [
        131.79,
        131.79,
        135.02,
        135.55,
        136.46,
        136.83,
        137.82,
        138.0,
        138.06,
        138.05,
        140.04,
        142.44,
        145.47,
        144.34,
        146.3,
        147.54,
        147.8
    ]

    # X = pd.DataFrame(x)
    # x = X.reset_index(drop=True)
    # x.columns = ["BoilPT"]

    # Y = pd.DataFrame(y)
    # y = Y.reset_index(drop=True)
    # y.columns = ["LogPress"]

    # ===========================================================

    # df: pd.DataFrame = pd.read_csv(
    #     "c:/Users/rickr/OneDrive/Python on OneDrive/Python Projects/ISL/data/default.csv")

    # df = encode(df, "student")
    # df = encode(df, "default")

    # x = df.loc[0:, ["balance", "income"]]
    # y = df.loc[0:, ["default"]]

    results = linreg(x, y, const=True)

    # for k, v in results.items():
    #     try:
    #         print(k, type(v[0]), v[0], sep=": ")
    #     except:
    #         print(k, "type not printable", sep=": ")

    for k, v in results.items():
        print(f'{k}: {v}')

    # reports.anova(results)
    # info.definitions(results, "x_bar")
    # reports.descriptive(results, 90)
    # info.var_info(results, "sumx")
    # methods.pred(results, [200], 95)
    # reports.report(results, section=7)
    # reports.summary(results)

    # reports.anova(results)
    # info.calculations(results, "x_bar")
    # info.definitions(results, "x_bar")
    # reports.descriptive(results, 90)
    # info.var_info(results, "sumx")
    # methods.pred(results, [200], 95)
    # reports.report(results, section=7)
    # reports.summary(results)
    # info.list_vars(results)
    # info.methods()
    # print()
    # info.usage(results)

    # for k, v in results.items():
    #     print(k, v)

    # r_utils.print_documentation("methods.py", function_names_only=True)
    # out = info.list_variables(results)

    # print(out)

    # print(results['corr_matrix'][0])

    # for k, v in results.items():
    #     print(f'{k}: {v}')