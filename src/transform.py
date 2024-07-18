"""
    Filename: transform.py
      Author: Richard E. Rawson
        Date: 2024-07-16
 Description: This module contains various methods for transforming data in a pandas DataFrame. Each of these methods uses a deepcopy of the provided DataFrame. This way, the original (provided) DataFrame is not modified. It is still possible to modify the original DataFrame by using the returned DataFrame to replace the original one.
"""

import sys
from copy import deepcopy

import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder


def interaction(df: pd.DataFrame, column1: str, column2: str) -> pd.DataFrame:
    """
    This is a function that takes two df column names and creates a third column that is the interaction between the two.     The new column is named "{column1}*{column2}".

    Parameters:
    ----------
        df (pd.DataFrame): The DataFrame containing the columns.
        column1 (str): The name of the first column.
        column2 (str): The name of the second column.

    Returns:
    ----------
        pd.DataFrame: The DataFrame with the new column added.
    """

    df_314066: pd.DataFrame = deepcopy(df)

    if column1 not in df_314066.columns or column2 not in df_314066.columns:
        print("One or both columns are not in the DataFrame")
        sys.exit()

    new_column_name: str = f"{column1}*{column2}"
    df_314066[new_column_name] = df_314066[column1] * df_314066[column2]

    return df_314066


def poly(df: pd.DataFrame, column: str, order: int) -> pd.DataFrame:
    """
    Compute a polynomial of a specified order for a specific column in the DataFrame. The new column is named as the original column name followed by the order of the polynomial requested.

    Parameters
    ----------
    df : pd.DataFrame -- any DataFrame (with numeric columns)
    column : str -- column name to use for computing the polynomial
    order : int -- order of the resulting polynomial

    Returns
    -------
    DataFrame -- original DataFrame with one additional column containing the polynomial of the specified order
    """

    df_314066: pd.DataFrame = deepcopy(df)

    if order < 2:
        print('Order of a polynomial must be at least 2.')
        sys.exit()
    if round(order, 0) != order:
        print("Order must be an integer.")
        sys.exit()

    if column not in df_314066.columns:
        print(f"Column {column} not found in DataFrame")
        sys.exit()

    new_column_name: str = f'{column}{order}'
    df_314066[new_column_name] = df_314066[column] ** order

    return df_314066


def encode(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Encode a binary column with 0 and 1. Replace the original column with the encoded column.

    Parameters:
    ----------
    df (pd.DataFrame): DataFrame with a binary column that can be encoded.
    column (str): Name of the column to encode.

    Returns:
    -------
    pd.DataFrame: DataFrame with the encoded column replacing the original column.
    """
    df_314066: pd.DataFrame = deepcopy(df)
    if df_314066[column].nunique() != 2:
        print("Column must have exactly two unique values.")
        sys.exit()

    if column not in df_314066.columns:
        print("Column name not found in DataFrame.")
        sys.exit()

    label_encoder = LabelEncoder()
    df_314066[column] = label_encoder.fit_transform(df_314066[column])

    return df_314066


def dummy(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    This function creates dummy variables for a specified column in a DataFrame as a means of representing categorical data as binary vectors. Two or more columns will be added to encode a single column with more than 2 unique values. The original column will be retained.

    This function has limited options for encoding categorical data, but chooses to encode using the most commonly used options. For details, see https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html.

    The "drop" option is not used, meaning that all features will be retained, even if they are not needed for the model. If a column has 4 features (e.g., North, South, East, West), incorporating all of them into a regression model is likely to result in collinearity. Therefore, it is advisable to ignore at least one column when fitting.

    Parameters
    ----------
    df : pd.DataFrame -- any DataFrame with a numeric column that can be encoded
    column : str -- the name of the column to encode

    Returns
    -------
    DataFrame -- the original DataFrame with the encoded columns
    """

    if column not in df.columns:
        print("Error: Column name not found in DataFrame.")
        sys.exit()

    if df[column].nunique() > 4:
        print("Encoding a column with more than 4 unique values is not supported.")
        sys.exit()

    encoder = OneHotEncoder(sparse_output=False)
    encoded_column = encoder.fit_transform(df[[column]])
    encoded_columns = encoder.get_feature_names_out([column])
    encoded_column_df = pd.DataFrame(data=encoded_column, columns=encoded_columns)
    df_314066: pd.DataFrame = pd.concat([df, encoded_column_df], axis=1)

    return df_314066


if __name__ == '__main__':
    pass
