"""
    Filename: model.py
      Author: Richard E. Rawson
        Date: 2024-07-16
 Description:


    !Generate the statistical model using statsmodels.

    !Perform regression analysis and generate intermediary statistics.

    !Return the results as a dictionary:
    !    {
    !        "x_bar": x_bar,
    !        "y_bar": y_bar,
    !        "SXX": SXX,
    !        "SYY": SYY,
    !        "SXY": SXY,
    !        "anova": anova_results,
    !        ...
    !    }

    !Once "results" are returned, the user can access any of about 50 statistical variables, which may be single values of a list (e.g., SE_coefficients or !t_statistics), or a table (e.g., anova, corr_matrix).

    !USAGE
    !    >>> results = linreg(X, y)

    !To get x_bar, for example, use:
    !    >>> results["x_bar"]

"""


if __name__ == '__main__':
    pass
