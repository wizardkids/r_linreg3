
# ====================================================================

""" MAIN ENTRY POINT

    Entry point for submission of data (X and y variables).
    Determine if submitted data is valid for multiple linear regression.
    Data are rejected if they don't fit the specified criteria, along with information about how to fix things, if possible
"""

# ====================================================================

"""
Generate the statistical model using statsmodels.

Perform regression analysis and generate intermediary statistics.

Return the results as a dictionary:
    {
        "x_bar": x_bar,
        "y_bar": y_bar,
        "SXX": SXX,
        "SYY": SYY,
        "SXY": SXY,
        "anova": anova_results,
        ...
    }

Once "results" are returned, the user can access any of about 50 statistical variables, which may be single values of a list (e.g., SE_coefficients or t_statistics), or a table (e.g., anova, corr_matrix).


USAGE
    >>> results = linreg(X, y)

To get x_bar, for example, use:
    >>> results["x_bar"]

"""

# ====================================================================

""" HELP & INFORMATION ABOUT STATISTICS

    details about definitions and methods of calculation are maintained in separate dictionaries

    >>> definitions("x_bar")
    >>> calculations("x_bar")

    >>> help()
            Help returns information about how to use the program, including details about each function that the user has access to.
"""

# ====================================================================

""" ANCILLARY CALCULATIONS
    >>> predicted y values given new values for X
    along with prediction intervals and confidence intervals

"""

# ====================================================================

""" METHODS FOR MODIFYING X VARIABLES (non-destructive)
    >>> interaction
    >>> poly
    >>> encode
    >>> dummy
"""
