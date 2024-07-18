"""
    Filename: ancillary.py
      Author: Richard E. Rawson
        Date: 2024-07-16
 Description:


    !ANCILLARY CALCULATIONS
    !    >>> predicted y values given new values for X
    !    along with prediction intervals and confidence intervals

"""

from copy import deepcopy
from typing import OrderedDict, Any

import pandas as pd


def pred(results: OrderedDict[str, Any], X: list, ci: int = 95) -> tuple[float, float] | None:
    """
    Given values for the X variables included in the model, print the predicted y value and a 95% confidence interval.

    Parameters
    ----------
    results : dict  -- all data from multiple_regr()
    X : list -- x values to use for prediction
    ci : int, optional -- confidence interval, by default 95

    Returns
    -------
    tuple[float, float] -- lower and upper limits of the prediction interval

    Examples
    --------
    pred(results, [42], ci=95)
    """

    # FEATURE: Add ability to submit a 2D list, where each list inside the outer list is a set of X values. This would output data for several data points at once, perhaps as a DataFrame of data. Maybe predict() does this already???

    # fmt: off
    alpha: float = round(1 - (ci / 100), 2)

    # Get a list of the X variable names used in this model.
    x_variables: list[str] = results["x_variable_names"]

    # If the user has submitted one set of X values, put that list in a list. The for... loop assumes it will get a list of lists.
    if not isinstance(X[0], list):
        X = [X]
    else:
        X = deepcopy(X)

    for val_list in X:
        if len(x_variables) != len(val_list):
            print(f'X values submitted do not match the model parameters.\nSubmit a list (numbers inside "[ ]", separated by commas) with one value for each of:\n{x_variables}', sep="")
            return None

        # Create a dictionary from the submitted X values.
        exog_dict: dict[str, float | int] = {}
        for ndx, var in enumerate(iterable=x_variables):
            exog_dict.update({var: val_list[ndx]})

        # Create a DataFrame from the dictionary that contains one column for each X variable and the submitted X value for each variable.
        df_new: pd.DataFrame = pd.DataFrame(data=[exog_dict])

        # Get the predicted value for the given X value as a pandas Series.
        pred_y = results['model_results'].predict(df_new)

        # Get the prediction interval (used to estimate the range of possible values for a future observation... an individual response) and confidence interval (used to estimate the range of possible values for a population parameter... an average response).
        pred = results['model_results'].get_prediction(exog=df_new)

        pred_df = pred.summary_frame(alpha=alpha)
        # Rename the columns to make them more understandable.
        pred_df.columns = ["mean", "mean_se", "lower ci", "upper ci", "lower pi", "upper pi"]

        print("\nREGRESSION MODEL:", sep="")
        print(f"{results['y_variable_name'][0]} ~ ", " + ".join(x_variables), "\n", sep="")
        print(f'{" + ".join(x_variables)} --> {df_new.iloc[0, :].values}')
        print(f'Predicted value for {results['y_variable_name'][0]}: {pred_y.iloc[0]}', sep="")

        print('\nPrediction interval:')
        print(f'lower {pred_df.loc[0, 'lower pi']}', sep="")
        print(f'upper {pred_df.loc[0, 'upper pi']}', sep="")

        print('\nConfidence interval:')
        print(f'lower {pred_df.loc[0, 'lower ci']}', sep="")
        print(f'upper {pred_df.loc[0, 'upper ci']}', sep="")

        print("\nPrediction Interval (PI): This interval estimates the range within which a single new observation of the dependent variable (y) for a given value of the independent variable (X) is likely to fall. It is always wider than the confidence interval because it takes into account not only the error in estimating the true regression line (as the CI does) but also the variability around the line of individual points.\n\nConfidence Interval (CI): This interval estimates the range within which the mean of the dependent variable (y) for a given value of the independent variable (X) is likely to fall. It reflects the uncertainty around the estimated regression line itself. In other words, if you were to repeat the study multiple times, the CI would contain the true mean value of y for that X value in a certain percentage of the studies.", sep="")

    return pred_df.loc[0, 'lower pi'], pred_df.loc[0, 'upper pi']


if __name__ == '__main__':
    pass
