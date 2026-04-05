import pandas as pd
from pathlib import Path
import sys
import time
from _utils import column_summary

def load_data(data_path: str) -> pd.DataFrame:

    start_time = time.time()
    raw_dir = Path(data_path) / 'raw'
    trans_data_path = Path(raw_dir) / 'transactions_data.csv'
    users_data_path = Path(raw_dir) / 'users_data.csv'
    cards_data_path = Path(raw_dir) / 'cards_data.csv'
    mcc_data_path = Path(raw_dir) / 'mcc_codes.csv'
    labels_data_path = Path(raw_dir) / 'binary_train_labels.csv'

    try:
        df_transactions = pd.read_csv(trans_data_path)
        df_users = pd.read_csv(users_data_path)
        df_cards = pd.read_csv(cards_data_path)
        df_mcc_codes = pd.read_csv(mcc_data_path, delimiter=';')
        df_fraud_labels = pd.read_csv(labels_data_path)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while loading the data: {e}.')
        sys.exit(1)
    
    # Create a SINGLE dataset

    try:

        df = pd.merge(df_transactions, df_users, how='left', left_on = 'client_id', right_on='id', suffixes=('_trans', '_cli'))
        df = pd.merge(df, df_cards, how='left', left_on='card_id', right_on='id')
        mcc_dict = df_mcc_codes.set_index('mcc_code')['description'].to_dict()
        df['merchant_category'] = df['mcc'].apply(lambda x: mcc_dict[x])
        df = pd.merge(df, df_fraud_labels, how='left', left_on='id_trans', right_on = 'Unnamed: 0')
        print(f'ℹ️ [INFO] Current number of entries: {len(df)}.')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while merging the dataframes: {e}.')
        sys.exit(1)

    # Convert to appropiate data types
    # Date fields
    try:
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M:%S')
        df['expires'] = pd.to_datetime(df['expires'], format='%m/%Y')
        df['acct_open_date'] = pd.to_datetime(df['acct_open_date'], format='%m/%Y')

        # Quant fields

        df['amount'] = df['amount'].str.replace('$', '').astype(float) # The str accessor lets us apply string operators vectorized accross entire Series
        df['per_capita_income'] = df['per_capita_income'].str.replace('$', '').astype(float)
        df['yearly_income'] = df['yearly_income'].str.replace('$', '').astype(float)
        df['total_debt'] = df['total_debt'].str.replace('$', '').astype(float)
        df['credit_limit'] = df['credit_limit'].str.replace('$', '').astype(float)

        # Target -> binary

        df['target'] = df['target'].astype('Int64')
    
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while converting data types: {e}.')
        sys.exit(1)

    try:
        print(f"ℹ️ [INFO] Ratio of transactions with negative amounts: {len(df[df['amount']<0])/len(df):.2f}.")
        print(f"ℹ️ [INFO] Ratio of fraudulent transactions with negative amounts: {len(df[(df['target'] == 1) & (df['amount']<0)])/len(df[df['target']==1]):.2f}.")

        print(f'ℹ️ [INFO] Dropping transactions with negative ammounts...')
        df = df[df['amount']>=0]
        print(f'ℹ️ [INFO] Current number of entries: {len(df)}.')

        print(f'ℹ️ [INFO] Dropping unlabeled transactions...')
        df = df[~df['target'].isnull()]
        print(f'ℹ️ [INFO] Current number of entries: {len(df)}.')
        df['errors'] = df['errors'].fillna('No errors')


    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while removing rare values & filling nulls: {e}.')
        sys.exit(1)


    # Aggregate features

    try:
        trans_count_cli = df[df['target']==0].groupby('client_id_x')['id_trans'].count().reset_index()
        trans_count_cli.columns = ['client_id_x', 'trans_count_cli']

        df = pd.merge(df, trans_count_cli, on='client_id_x', how='left')

        avg_amount_cli = df[df['target']==0].groupby('client_id_x')['amount'].mean().reset_index()
        avg_amount_cli.columns = ['client_id_x', 'avg_amount_cli']

        df = pd.merge(df, avg_amount_cli, on='client_id_x', how='left')

        max_amount_cli = df[df['target']==0].groupby('client_id_x')['amount'].max().reset_index()
        max_amount_cli.columns = ['client_id_x', 'max_amount_cli']

        df = pd.merge(df, max_amount_cli, on='client_id_x', how='left')

        trans_count_card = df[df['target']==0].groupby('card_id')['id_trans'].count().reset_index()
        trans_count_card.columns = ['card_id', 'trans_count_card']

        df = pd.merge(df, trans_count_card, on='card_id', how='left')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while aggregating features: {e}.')
        sys.exit(1)

    # Drop columns

    try:
        columns_to_drop = ['id_trans', 'client_id_x', 'card_id', 'merchant_id', 'merchant_state', 'zip', 'mcc', 'id_cli', 'birth_year', 'birth_month', 'address', 'id', 'client_id_y', 'card_number', 'cvv', 'card_on_dark_web', 'Unnamed: 0']
        df.drop(columns_to_drop, axis=1, inplace=True)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while dropping columns: {e}.')
        sys.exit(1)
    
    # Final summary and export
    try:
        summary_global = column_summary(df)
        print('ℹ️ [INFO] Final Dataset Summary\n')
        print(summary_global)
        clean_dir = Path(data_path) / 'clean'
        clean_dir.mkdir(exist_ok=True)
        export_path = clean_dir / 'CleanDataset.parquet'
        df.to_parquet(export_path, index=False)

        print(f'ℹ️ [INFO] Clean data successfully exported to {export_path}.')
        total_time = time.time() - start_time
        print(f'ℹ️ [INFO] Loading phase - Total execution time: {total_time//60} min {total_time%60:.2f} sec.')

    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while exporting data: {e}.')
        sys.exit(1)


if __name__ == '__main__':
    script_dir = Path(__file__).parent
    load_data(data_path=(script_dir / '../data').resolve())



