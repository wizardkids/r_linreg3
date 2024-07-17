"""
    Filename: reports.py
      Author: Richard E. Rawson
        Date: 2024-07-16
 Description:

"""


from typing import Any
from typing import OrderedDict as ODictType

import info
import pandas as pd
from statsmodels.stats.descriptivestats import Description


def anova(results: ODictType[str, Any]) -> None:
    """
    Print the OLS Regression Results table provided by statsmodels.

    NOTES:
        - sm.stats.anova_lm(model, typ=1) is sensitive to the order of variables.

        - sm.stats.anova_lm(model, typ=2) is not sensitive to the order of variables and is usually appropriate for balanced designs or unbalanced designs with orthogonal factors.

        - sm.stats.anova_lm(model, typ=3) is not sensitive to the order of variables and is often used for unbalanced designs or models with interactions.

    Parameters
    ----------
    results : ODictType[str, Any] -- dictionary of results from running linear regression analysis
    """

    print()
    print(results['anova_summary'])

    return None


def descriptive(results: ODictType[str, Any], ci: int = 95) -> None:
    """
    This function provides a table of descriptive statistics for the regression data. The table includes: nobs, mean, std_err upper_ci, lower_ci, std, coef_var, range, max, min, median

    CODENOTE:
        https://www.statsmodels.org/stable/generated/statsmodels.stats.descriptivestats.Description.html#statsmodels.stats.descriptivestats.Description

        The Description class from the statsmodels.stats.descriptivestats module provides extended descriptive statistics for data in a pandas DataFrame.

        Statistics: The stats parameter allows you to specify a sequence of statistics to compute. If not provided, a full set of statistics is computed.

        Numeric and Categorical Data: It can handle both numeric and categorical data, providing relevant statistics for each.

        Alpha: The alpha parameter sets the significance level for confidence intervals (default is 0.05 for 95% confidence intervals).

        Use T-Distribution: The use_t parameter determines whether to use the Student’s t-distribution to construct confidence intervals.

        Percentiles: You can specify which percentiles to calculate with the percentiles parameter.

        Top Categories: The ntop parameter sets the number of top categorical labels to report.

        The selectable statistics include common measures like mean, standard deviation, confidence intervals, range, maximum, minimum, median, skewness, kurtosis, and more. It also includes tests for normality like the Jarque-Bera test.

    Parameters
    ----------
    results : ODictType[str, Any] -- results of linear regression analysis

    ci : int, optional -- confidence interval level, by default 95
    """

    # By way of example, a 95% CI has to be converted to an alpha of 0.05
    alpha: float = round(1 - (ci / 100), 2)

    df_desc: pd.DataFrame = pd.concat(
        [results['X'], results['y']], axis=1)

    desc = Description(df_desc, alpha=alpha, stats=['nobs', 'missing', 'mean', 'std_err', 'ci', 'std', 'coef_var', 'range', 'max', 'min', 'median'])

    ds: str = " DESCRIPTIVE STATISTICS ".center(34, "=")
    print("\n", ds, "\n", desc.numeric, sep='')

    return None


def summary(results: ODictType[str, Any]) -> None:
    """
    Print a summary table of key results of linear regression and an anova table, courtesy of statsmodels.

    Parameters
    ----------
    results : ODictType[str, Any] -- dictionary of 52 linear regression results from statsmodels and computations.
    """

    if results['const']:
        labels: list = ['CONSTANT'] + results['x_variable_names']
    else:
        labels: list = results['x_variable_names']

    print(f"{'PREDICTOR':^14}")
    print(f"{'VARIABLES':^14}{'COEFFICIENT':>13}{'STD ERROR':>13}{'STUDENT\'S T':>13}{'P':>12}")
    print("-" * 65)

    # fmt: off
    for i, label in enumerate(labels):
        print(f"{label[:14]:>14}{results['coefficients'][i]:>13.4f}{results['SE_coefficients'][i]:>13.4f}{results['t_statistics'][i]:>13.4f}{results['t_pvalues'][i]:>12.4f}")
    print(
        f"\n{'CASES INCLUDED'.ljust(20, ' ')}{results['n']:<9.0f}MISSING CASES  0")
    print(f"DEGREES OF FREEDOM  {results['DFR']:.0f}")
    print(
        f"OVERALL F           {results['F']:<9.4g}P VALUE {results['F_pvalue']:.4g}")
    print(f"ADJUSTED R SQUARED  {results['r_squared_adj']:.4g}")
    print(f"R SQUARED           {results['r_squared']:.4f}")
    print(f"RESID. MEAN SQUARE  {results['MSE']:.4g}")
    print("\n")

    print(
        f"STEPWISE ANALYSIS OF VARIANCE OF {results['y_variable_name']}".center(68, " "))

    # Now print an anova table.
    print(results['anova'])
    print('\n** Type 1 ANOVA: sensitive to the order of variables. \n', sep="")

    return None
