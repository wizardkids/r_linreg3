"""
    Filename: info.py
      Author: Richard E. Rawson
        Date: 2024-07-16
 Description:

"""

from typing import OrderedDict, Any

DESCRIPTIONS: dict[str, str] = {
    "model_results": "statsmodels model_results; since this variable holds the statsmodels result for model.fit(), any method from statsmodels can be applied to this variable\nExample -- results['model_results'][0].summary()",
    "x_variable_names": "names of variables in the X dataset",
    "y_variable_name": "name of the y variable",
    "n": "number of observations",
    "y": "dependent variable",
    "X": "independent variable(s)",
    "sumx": "sum of x values",
    "sumy": "sum of y values",
    "sumxy": "sum of x*y values",
    "sumx2": "sum of x-squared values",
    "sumy2": "sum of y-squared values",
    "x_bar": "mean of xi; one mean for each X column",
    "y_bar": "mean of yi",
    "SXX": "corrected sum of squares for the xi's",
    "SYY": "corrected sum of squares for the yi's",
    "SXY": "corrected sum of cross products",
    "anova": "Stepwise ANOVA table",
    "anova_summary": "statsmodels' OLS Regression Results",
    "coefficients": "list of parameter coefficients",
    "intercept": "estimate for intercept",
    "slope": "estimate(s) for the regression parameters",
    "SE_coefficients": "list of SE for coefficients",
    "std_error_b0": "SE of the intercept parameter estimate",
    "std_error_b1": "SE of the parameter estimates",
    "t_statistics": "t statistics for coefficients",
    "t_pvalues": "p value for each of the t statistics in multiple regression",
    "t_intercept": "intercept / std_error_B0",
    "t_intercept_p": "p value for intercept",
    "t_slope": "slope / std_error_B1",
    "t_slope_p": "p value for slope",
    "DFM": "degrees of freedom of the model; equals the number of parameters",
    "DFR": "degrees of freedom of the residuals; the number of observations minus the number of parameters in the model",
    "DFT": "total degrees of freedom; the number of observations minus 1",
    "k": "The dof is defined as the rank of the regressor matrix minus 1 if a constant is included.; used internally by statsmodels in the context of F-statistic and individual coefficient hypothesis testing to appropriately scale the variance components; usually but not always the same as DFM",
    "SS_model": "sum of squares of the model",
    "RSS": "sum of the squared residuals (residual sum of squares): sum((yi - y_hat)^2) or sum(squared residuals) or SYY - ((SXY * SXY) / SXX)",
    "SS_total": "total sum of squared; same as SYY: sum((yi - y_bar)^2)",
    "MSE_total": "the sum of MSE_model (MSE for the model) and MSE (MSE of the residuals)",
    "MSE_model": "average variation of the fitted values around the mean of the observed values: (sum((y_hat - y_bar)^2)/k; The explained sum of squares (SS_model) divided by the model degrees of freedom.",
    "MSE": "also MSE_resid; mean squared error of the residuals; mean squared error tells you how close a regression line is to a set of points. It does this by taking the distances from the points to the regression line and squaring them. Squaring removes any negative signs and gives more weight to larger differences.",
    "SEE": "standard error of the estimate or standard error of the regression;",
    "r_squared": "coefficient of determination; This is defined here as 1 - ssr/centered_tss if the constant is included in the model and 1 - `ssr`/`uncentered_tss` if the constant is omitted.",
    "r_squared_adj": "adjusted r_squared; compensates for adding X variables that have low effect on the model; This is defined here as 1 - (nobs-1)/df_resid * (1-rsquared) if a constant is included and 1 - nobs/df_resid * (1-rsquared) if no constant is included.",
    "correlation": "correlation between y and the X variables: sqrt(r_squared)",
    "F": "ratio of MSE_model and MSE_residuals, divided their degrees of freedom, p and n-p-1, respectively; this means that F corrects for the number of parameters, since otherwise, just adding parameters would increase F",
    "F_pvalue": "p value for F statistic",
    "Durbin-Watson": "Durbin-Watson statistic; diagnose the presence of autocorrelation in the residuals of a regression model; Autocorrelation occurs when the errors of a model are not independent; Value close to 2: No significant autocorrelation; Value closer to 0: Positive autocorrelation; Value closer to 4: Negative autocorrelation.",
    "corr_matrix": "the correlation matrix of the X and y variables",
    "cov_matrix": "covariance matrix",
    "fitted_values": "predicted y values",
    "residuals": "the difference between the ith observed value and the value predicted by our linear model"
}


CALCULATIONS: dict[str, str] = {
    "model_results": "model.fit()",
    "x_variable_names": "x_variable names",
    "y_variable_name": "y variable name",
    "n": "model_results.nobs or len(X)",
    "y": "pandas dataframe",
    "X": "pandas dataframe",
    "sumx": "sum(xi)",
    "sumy": "sum(yi)",
    "sumxy": "sum(xi * yi)",
    "sumx2": "sum((xi^2))",
    "sumy2": "sum((yi)^2)",
    "x_bar": "sum(xi)/n or np.mean(x)",
    "y_bar": "sum(yi)/n or np.mean(y)",
    "SXX": "sum((xi - x_bar)^2)",
    "SYY": "sum((yi - y_bar)^2)",
    "SXY": "sum((xi - x_bar) * (yi - y_bar))",
    "anova": "statsmodels.stats.anova.anova_lm(model_results)",
    "anova_summary": "model_results.summary()",
    "coefficients": "model_results.params",
    "intercept": "model_results.params[0]",
    "slope": "model_results.params[1:] or SXY / SXX",
    "SE_coefficients": "model_results.bse",
    "std_error_b0": "model_results.bse",
    "std_error_b1": "model_results.bse",
    "t_statistics": "model_results.tvalues",
    "t_pvalues": "model_results.t_pvalues",
    "t_intercept": "model_results.tvalues",
    "t_intercept_p": "model_results.t_pvalues[0]",
    "t_slope": "model_results.tvalues[1:]",
    "t_slope_p": "model_results.t_pvalues[1:]",
    "DFM": "len(model_results.params)",
    "DFR": "n - DFM",
    "DFT": "n - 1",
    "k": "model_results.df_model",
    "SS_model": "model_results.ess",
    "RSS": "model_results.ssr",
    "SS_total": "model_results.centered_tss",
    "MSE_total": "MSE_model + MSE",
    "MSE_model": "model_results.mse_model",
    "MSE": "model_results.mse_resid or RSS / (n-k) or sum((yi - y_hat)^2) / (n-k))",
    "SEE": "np.sqrt(MSE) or sum of the squared difference y - y-hat divided by df; same units as the y variable",
    "r_squared": "model_results.rsquared or SS_model / SS_total or SSreg ",
    "r_squared_adj": "model_results.rsquared_adj",
    "correlation": "np.sqrt(r_squared)",
    "F": "model_results.fvalue or MSE_model / MSE",
    "F_pvalue": "model_results.f_pvalue",
    "Durbin-Watson": "model_results.durbin_watson",
    "corr_matrix": "all_vars.corr(), where all_vars is a DataFrame with X and y variables",
    "cov_matrix": "model_results.cov_params()",
    "fitted_values": "model_results.fittedvalues",
    "residuals": "model_results.resid or yi - fitted_values"
}


def print_variables(data: OrderedDict[str, Any] = None) -> None:
    """
    Print to the terminal a list of all variables exposed in the "results" dictionary. The list is organized with headings to make it slightly easier to find a particular variable.
    """

    section = 0
    for k, v in DESCRIPTIONS.items():
        # Insert headings at the appropriate places.
        match k:
            case 'x_variable_names':
                if section in [0, 1]:
                    print("\nDATA")
                    print("-" * 32)
            case 'sumx':
                if section in [0, 2]:
                    print("\nUNDERLYING STATISTICS")
                    print("-" * 32)
            case 'anova':
                if section in [0, 3]:
                    print("\nREGRESSION MODEL")
                    print("-" * 32)
            case 'SS_model':
                if section in [0, 4]:
                    print("\nMODEL FIT STATISTICS")
                    print("-" * 32)
            case 'corr_matrix':
                if section in [0, 5]:
                    print("\nADDITIONAL INFORMATION")
                    print("-" * 32)

        # Print the variable name.
        if data:
            print(f'{k}: {data[k]}')
        else:
            print(k, sep='')

    return None


def var_info(results: OrderedDict[str, Any], variable_name: str = "", all_rows: bool = False) -> None:
    """
    Print detailed information about a single variable. This includes the variable name, its value computed for this regression, a description, and the method of calculation or source of the variable's quantity. For variables that hold DataFrames, include an option to print the whole data set or just the first few rows.

    Parameters
    ----------
    results : Dict[str, Any] -- results of linear regression
    variable_name : str, optional -- name of the variable to get information about, by default ""
    print_all_rows : bool, optional -- if True, print all rows for variables that are dataframes, by default False
    """

    if variable_name == "":
        print("Variable name missing.")
        print_variables()
        print()
        return

    if variable_name not in results:
        print(f'"{variable_name}" not found in results.')
        print_variables()
        print()
        return

    result = results[variable_name]

    print(f"\nRESULTS FOR {variable_name}")
    print("-" * 32)

    if variable_name in ['y', 'X', 'fitted_values', 'residuals', 'corr_matrix', 'corr_matrix_exog', 'cov_matrix']:
        if all_rows:
            print(result.to_string(index=False, header=True, justify="left"))
        else:
            print(result.head())
    else:
        if isinstance(result, list):
            for item in result:
                print(" " * 4, item)
        else:
            print(" " * 4, result)

    print()
    print(f" DESCRIPTION:\n {DESCRIPTIONS[variable_name]}", sep="")
    print()
    print(f" CALCULATION:\n {CALCULATIONS[variable_name]}", sep="")
    print()


# def print_variables() -> None:
#     """
#     Print a list of all variables available in the results dictionary.

#     Parameters
#     ----------
#     results : Dict[str, Any] -- dictionary containing regression results
#     """
#     print("\nVARIABLES:")
#     variable_names = list(DESCRIPTIONS.keys())
#     print(", ".join(variable_names))


def included_vars() -> list[list[str]]:
    """
    Utility function that provides a list of variables included in {all_stats}. This function is not meant to be accessible to the end-user, but is called by multiple_regr() to create an ordered list of variables in {all_stat}.

    CODENOTE:
        [vars_list], below, should contain all the variables that are included in {all_stats} and needs to be updated if {all_stats} is changed.

    Returns
    -------
    list[list[str]] -- variables list
    """

    # fmt: off
    vars_list: list[list[str]] = [
        ["model_results"],
        ["x_variable_names", "y_variable_name", "n", "y", "X"],
        ["sumx", "sumy", "sumxy", "sumx2", "sumy2", "x_bar", "y_bar", "SXX", "SYY", "SXY"],
        ["anova", "anova_summary", "coefficients", "intercept", "slope", "SE_coefficients", "std_error_b0", "std_error_b1", "t_statistics", "t_pvalues", "t_intercept", "t_intercept_p", "t_slope", "t_slope_p", "DFM", "DFR", "DFT", "k"],
        ["SS_model", "RSS", "SS_total", "MSE_total", "MSE_model", "MSE", "SEE", "r_squared", "r_squared_adj", "correlation", "F", "F_pvalue"],
        ["Durbin-Watson", "corr_matrix", "cov_matrix", "fitted_values", "residuals"],
        ["const"]
    ]
    # fmt: on
    return vars_list


def calculation(var: str = "") -> None:
    """
    Print the method by which the requested variable was calculated (or obtained). print_variables() can be used to get a list of available variables in regression results.

    Parameters
    ----------
    var : str -- a variable name (a key in {CALCULATIONS})

    Examples
    --------
    calculations("x_bar")

    Output --> x_bar: sum(xi))/n or np.mean(x)
    """

    print()

    if not var:
        print("Variable name missing.\n")
        print_variables()
        print()
        return None

    if var != "" and var not in CALCULATIONS.keys():
        if var.lower() not in ["h", "help"]:
            print(f'"{var}" not found in results.\n')
        print_variables()
        print()
        return None

    for k, v in CALCULATIONS.items():
        if k != "const":
            if var:
                if k == var:
                    print(k, ": ", v, sep="")
            else:
                print(k, ": ", v, sep="")

    return None


def description(var: str = "") -> None:
    """
    Print a description of a variable (its definition or meaning). print_variables() can be used to get a list of available variables in regression results.

    Parameters
    ----------
    var : str -- a variable name (key in {DESCRIPTIONS})

    Examples
    --------
    description("x_bar")

    Output --> x_bar: mean of xi; one mean for each X column

    """

    print()

    if not var:
        print("Variable name missing.\n")
        print_variables()
        print()
        return None

    if var != "" and var not in DESCRIPTIONS.keys():
        if var.lower() not in ["h", "help"]:
            print(f'"{var}" not found in results.\n')
        print_variables()
        print()
        return None

    for k, v in DESCRIPTIONS.items():
        if k != "const":
            if var:
                if k == var:
                    print(k, ": ", v, sep="")
                    break
            else:
                print(k, ": ", v, sep="")

    return None


def methods() -> None:
    """
    List all exposed methods used in r_linreg module. Submodules
    include reports, info, transform, and ancillary.
    """
    txt = """
EXPOSED FUNCTIONS:

    r_linreg:
        linreg(x, y, const=True)
            initial function to run linear regression analysis.
            Results are returned as a dictionary.

    reports:
        anova(results)
            ANOVA table;
        descriptive(results, ci)
            print a table of descriptive statistics
            ci is the confidence interval, defaults to 95
        print_variables(results)
            - list all variables in regression results;
            - if results is provided as an argument, each variable
            is printed with its value
        OLS_results(results)
            OLS Regression Results table from statsmodels

    info:
        calculation("var")
            source or method of calculation for one variable ("var")
        definition("var")
            definition for one variable ("var")
        print_variables(results)
            - list all variables in regression results;
            - if results is provided as an argument, each variable
            is printed with its value
        methods()
            an annotated list of all exposed methods
        usage()
            notes on linreg() usage
        var_info(results, var, all_rows=False)
            - prints value, definition, and calculation for one
              variable ("var")
            - "all_rows": False prints DataFrame head() only

    ancillary:
        pred(results, X: list, ci)
            print predicted y and 95 % confidence interval for
            provided values of X variable(s)

    transform:
        dummy(df, column)
            returns DataFrame with column converted to dummy variables (e.g.,
            column containing "East", "South", and "West" becomes three columns with those names)
        encode(df, column)
            returns DataFrame with a binary column converted to a categorical
            variable (0, 1)
        interaction(df, column1, column2)
            returns the DataFrame with a new column that is the interaction
            between column1 and column2
        poly(df, column, order)
            create a new column that is the provided polynomial of a
            current column.
"""
    print(txt)


def usage() -> None:
    """
    Provide usage help and details for this module.
    """

    txt = """

USAGE:

    >>> import r_linreg
    >>> import reports
    >>> import info
    >>> import methods

r_linreg returns a dictionary holding all variables and their values. It is the only output from r_linreg. The dictionary can be queried by variable name to get individual results or the reports module can be used.

r_linreg can handle x and y data as pandas Series, pandas.DataFrames or as python lists. DataFrames can have more than one x variable and lists can be 2-dimensional. The y variable can only be a Series or one-dimension list.

Typical usage:

    >>> results = r_linreg.linreg(x, y)

The "results" dictionary has the following key:value format:

    {variable: variable_value}

Access data associated with a variable (quotes required)...

    >>> results['x_bar'] --> [202.95]  (a list is returned that contains the mean for each x variable)

Access a brief description of the variable
    >>> description['x_bar'] --> 'mean of xi; one mean for each X column'

Access the method used to calculate the variable
    >>> calculation['x_bar'] --> sum(xi)/n or np.mean(x)

Use print_vars() to see a list of all variables returned in "results". While the list of variables accessible directly from "results" is sizable, it is not exhaustive. The complete RegressionResults returned by statsmodels can be accessed via results['model_results'] and then model_results can be used to access any method or attribute of statsmodels.regression.linear_model.RegressionResults. For more information, see:

https://www.statsmodels.org/dev/generated/statsmodels.regression.linear_model.RegressionResults.html
    """

    print(txt)

    return None


if __name__ == '__main__':
    pass
