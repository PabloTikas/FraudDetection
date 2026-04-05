import pandas as pd
from sklearn.model_selection import train_test_split

def column_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Helper function to summarize dataframe columns.

    Args:
        df (pandas.DataFrame)

    Returns:
        summary_df (pandas.DataFrame)
    """
    summary_data = []
    for col_name in df.columns:
        col_dtype = df[col_name].dtype
        num_of_nulls = df[col_name].isnull().sum()
        num_of_non_nulls = df[col_name].notnull().sum()
        num_of_distinct_values = df[col_name].nunique()

        if num_of_distinct_values <= 10:
            distinct_values_counts = df[col_name].value_counts().to_dict()
        else:
            top_10_values_counts = df[col_name].value_counts().head(10).to_dict()
            distinct_values_counts = {k: v for k, v in sorted(top_10_values_counts.items(), key= lambda item: item[1], reverse=True )}
        summary_data.append({
            'col_name': col_name,
            'col_dtype': col_dtype,
            'num_of_nulls': num_of_nulls,
            'num_of_non_nulls': num_of_non_nulls,
            'num_of_distinct_values': num_of_distinct_values,
            'distinct_values_counts': distinct_values_counts
        })
    summary_df = pd.DataFrame(summary_data)
    return summary_df

def split_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:

    X = df.drop('target', axis=1)
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(
        X,y,
        test_size=0.2,
        stratify=y,
        random_state=123
    )

    print(f'ℹ️ [INFO] Train features shape: {X_train.shape}')
    print(f'ℹ️ [INFO] Test features shape: {X_test.shape}')
    print(f'ℹ️ [INFO] Train fraud rate: {y_train.mean():.5f}')
    print(f'ℹ️ [INFO] Test fraud rate: {y_test.mean():.5f}')

    return X_train, X_test, y_train, y_test

    