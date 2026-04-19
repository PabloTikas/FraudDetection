from load import load_data
from preprocess import preprocess_data
from tune import tune_model
from train import train_model
from evaluate import evaluate_model
from _utils import split_data
from pathlib import Path
import sys
import pandas as pd
import time

def run_pipeline():

    print('ℹ️ [INFO] Starting pipeline...')
    start_time = time.time()

    print('ℹ️ [INFO] Phase 1: Loading dataset.\n')
    try:
        script_dir = Path(__file__).parent
        data_path = script_dir / '../data'
        load_data(data_path=data_path)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while loading the dataset: {e}.')
        sys.exit(1)

    print('ℹ️ [INFO] Phase 2: Preprocessing dataset.\n')
    try:
        preprocess_data(data_path=data_path)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while preprocessing the dataset: {e}.')
        sys.exit(1)

    print('ℹ️ [INFO] Phase 3: Splitting dataset.\n')
    try:
        script_dir = Path(__file__).parent
        dataset_path = script_dir / '../data' / 'preprocessed' / 'PreprocessedDataset.parquet'
        df = pd.read_parquet(dataset_path)
        X_train, X_test , y_train, y_test = split_data(df)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while splitting the dataset: {e}.')
        sys.exit(1)

    print('ℹ️ [INFO] Phase 4: Tuning model.\n')
    try:
        tune_model(X_train, y_train)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while tuning the model: {e}.')
        sys.exit(1)

    print('ℹ️ [INFO] Phase 5: Training model.\n')
    try:
        train_model(X_train, y_train)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while training the model: {e}.')
        sys.exit(1)

    print('ℹ️ [INFO] Phase 6: Evaluating model.\n')
    try:
        evaluate_model(X_test, y_test)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while evaluating the model: {e}.')
        sys.exit(1)

    total_time = time.time() - start_time
    print(f'ℹ️ [INFO] Pipeline total execution time: {total_time//60} min {total_time%60:.2f} sec.')


if __name__ == '__main__':
    run_pipeline()  

    
