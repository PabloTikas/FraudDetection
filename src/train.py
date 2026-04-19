import pandas as pd
from xgboost import XGBClassifier
from pathlib import Path
import json
import sys
import time
import mlflow
import mlflow.xgboost
from _utils import split_data
from datetime import datetime

def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> None:
    start_time = time.time()

    try:
        params_path = Path(__file__).parent / '../outputs' / 'tuning' / 'best_params.json'
        with open(params_path, 'r') as f:
            data = json.load(f)
            best_params = data['best_params']
            best_value = data['best_value']
        print(f'ℹ️ [INFO] Hyperparameters successfully retrieved from {params_path}.')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while retrieving optimal hyperparameters: {e}.')
        sys.exit(1)

    # Experiment tracking with MLFlow
    try:
        mlflow_path = Path(__file__).parent / '../outputs' / 'mlruns.db'
        mlflow.set_tracking_uri('sqlite:///' + str(mlflow_path))
        mlflow.set_experiment('FraudDetection')
        with mlflow.start_run(): 
            # Train model with tuned hyperparameters
            xgb_model_tuned = XGBClassifier(
                enable_categorical=True,
                tree_method='hist',
                eval_metric='aucpr',
                random_state=123,
                **best_params
            )

            xgb_model_tuned.fit(X_train, y_train)

            # Log PR-AUC metric
            mlflow.log_metric('Tuning PR-AUC score', best_value)
            mlflow.log_params(best_params)
            today_YYYYMMDDHHMMSS = datetime.now().strftime('%Y%m%d%H%M%S')
            mlflow.xgboost.log_model(xgb_model_tuned, artifact_path=f'{today_YYYYMMDDHHMMSS}_xgb_model')

        print(f'ℹ️ [INFO] Model successfully trained with optimal hyperparameters.')
        print(f'ℹ️ [INFO] Artifact saved to {mlflow_path}.')

        total_time = time.time() - start_time
        print(f'ℹ️ [INFO] Model Training phase - Total execution time: {total_time//60} min {total_time%60:.2f} sec.')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while training the model: {e}.')
        sys.exit(1)


if __name__ == '__main__':
    
    script_dir = Path(__file__).parent
    dataset_path = script_dir / '../data' / 'preprocessed' / 'PreprocessedDataset.parquet'

    df = pd.read_parquet(dataset_path)

    X_train, _, y_train, _ = split_data(df)

    train_model(X_train, y_train)


# To visualize MLFlow UI, use command in root directory: mlflow ui --backend-store-uri sqlite:///outputs/mlruns.db
    


