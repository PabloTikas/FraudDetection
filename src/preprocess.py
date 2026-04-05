import pandas as pd
from pathlib import Path
import sys
import time
from _utils import column_summary

def preprocess_data(data_path: str) -> pd.DataFrame:
    
    start_time = time.time()
    # Load clean dataset

    try: 
        clean_dir = Path(data_path) / 'clean'
        file_path = clean_dir / 'CleanDataset.parquet'
        df = pd.read_parquet(file_path)
        print(f'ℹ️ [INFO] Current number of entries: {len(df)}.')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while loading clean dataset: {e}.')
        sys.exit(1)

    # Feature Engineering

    try:
        # Temporal features

        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = df['date'].dt.hour # The dt accessor lets us apply vectorized operations (faster)
        df['day_of_week'] = df['date'].dt.dayofweek # 0 -> Monday, 6 -> Sunday
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day

        # Date differences

        df['acct_open_date'] = pd.to_datetime(df['acct_open_date'])
        df['expires'] = pd.to_datetime(df['expires'])

        df['days_since_acct_open'] = (df['date'] - df['acct_open_date']).dt.days
        df['days_until_expiration'] = (df['expires'] - df['date']).dt.days

        print(f'ℹ️ [INFO] Cleaning rows with errors during data generation...')

        condition_expiration = (df['days_until_expiration'] <= 0) & (df['errors']=='No errors')
        condition_acct_open = (df['days_since_acct_open'] < 0)

        df = df[~(condition_expiration | condition_acct_open)]

        print(f'ℹ️ [INFO] Current number of entries: {len(df)}.')

        df['years_since_pin_change'] = (df['date'].dt.year - df['year_pin_last_changed']).astype(int)
        df['years_since_pin_change'] = df['years_since_pin_change'].apply(lambda x: x if x> 0 else 0)
        
        df['years_retired'] = df['current_age'] - df['retirement_age']
        df['years_retired'] = df['years_retired'].apply(lambda x: max(0,x))

    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while engineering features: {e}.')
        sys.exit(1)

    # Dropping features

    try:
        features_to_drop = ['date', 'expires', 'acct_open_date', 'year_pin_last_changed', 'retirement_age']
        df.drop(features_to_drop, axis=1, inplace=True)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while dropping features: {e}.')
        sys.exit(1)

    # Category dtypes

    cat_columns = ['use_chip', 'merchant_city', 'errors', 'gender', 'card_brand', 'card_type', 'has_chip', 'merchant_category']

    for col in cat_columns:
        df[col] = df[col].astype('category')

    # Final summary and export
    try:
        summary_global = column_summary(df)
        print('ℹ️ [INFO] Final Dataset Summary\n')
        print(summary_global)
        preprocessed_dir = Path(data_path) / 'preprocessed'
        preprocessed_dir.mkdir(exist_ok=True)
        export_path = preprocessed_dir / 'PreprocessedDataset.parquet'
        df.to_parquet(export_path, index=False)

        print(f'ℹ️ [INFO] Preprocessed data successfully exported to {export_path}.')
        total_time = time.time() - start_time
        print(f'ℹ️ [INFO] Preprocessing phase - Total execution time: {total_time//60} min {total_time%60:.2f} sec.')

    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while exporting data: {e}.')
        sys.exit(1)

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    preprocess_data(data_path=(script_dir / '../data').resolve())
