"""
    Filename: info.py
      Author: Richard E. Rawson
        Date: 2024-07-16
 Description:


    !HELP & INFORMATION ABOUT STATISTICS

    !    details about definitions and methods of calculation are maintained in separate dictionaries

    !    >>> definitions("x_bar")
    !    >>> calculations("x_bar")

    !    >>> help()
    !            Help returns information about how to use the program, including details about each function that the user has access to.

"""

description = {
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


calculations = {
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
    "x_bar": "sum(xi))/n or np.mean(x)",
    "y_bar": "(sum(yi))/n or np.mean(y)",
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


def included_vars() -> list[list[str]]:
    """
    Utility function that provides a list of variables included in {all_stats}. This function is called by multiple_regr() to create an ordered list of variables in {all_stat}.

    CODENOTE:
        [vars_list] should contain all the variables that are included in {all_stats}.

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


if __name__ == '__main__':
    pass
