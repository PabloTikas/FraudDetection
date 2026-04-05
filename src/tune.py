import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
import optuna
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import average_precision_score
import numpy as np
import sys
from pathlib import Path
from _utils import split_data
import time
import json




def tune_model(X_train: pd.DataFrame, y_train: pd.Series) -> tuple[float, dict]:
    start_time = time.time()
    try:
        # Subsample data for tuning (for limited computational power)
        X_tune, _, y_tune, _ = train_test_split(X_train, y_train,
                                                train_size=0.5,
                                                stratify=y_train,
                                                random_state=123)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while splitting the data: {e}.')
        sys.exit(1)
    
    # Define optimization objective
    def objective(trial):
        
        params = {
            'n_estimators':      200,  # fixed ceiling, early stopping decides actual number
            'max_depth':         trial.suggest_int('max_depth', 2, 8),
            'min_child_weight':  trial.suggest_int('min_child_weight', 1, 10),
            'lambda':            trial.suggest_float('lambda', 1e-2, 10.0, log=True),
            'alpha':             trial.suggest_float('alpha', 1e-2, 10.0, log=True),
            'subsample':         trial.suggest_float('subsample', 0.6, 1.0),
            'colsample_bytree':  trial.suggest_float('colsample_bytree', 0.6, 1.0),
            'learning_rate':     trial.suggest_float('learning_rate', 1e-2, 0.3, log=True),
            'gamma':             trial.suggest_float('gamma', 1e-3, 1.0, log=True),
            'scale_pos_weight':  trial.suggest_float('scale_pos_weight', 1.0, 100)
        }

        model = XGBClassifier(
            enable_categorical=True,
            tree_method='hist',
            eval_metric='aucpr',
            random_state=123,
            early_stopping_rounds=50,
            **params
        )

        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=123)
        scores = []

        for train_idx, val_idx in cv.split(X_tune, y_tune):
            X_tr  = X_tune.iloc[train_idx]
            X_val = X_tune.iloc[val_idx]
            y_tr  = y_tune.iloc[train_idx]
            y_val = y_tune.iloc[val_idx]

            model.fit(
                X_tr, y_tr,
                eval_set=[(X_val, y_val)],
                verbose=False
            )

            y_proba = model.predict_proba(X_val)[:, 1]
            scores.append(average_precision_score(y_val, y_proba))

        return np.mean(scores)
    
    try:    
        sampler = optuna.samplers.TPESampler(seed=123)
        study = optuna.create_study(
            study_name = 'xGBoost Hyperparameter Tuning',
            direction='maximize',
            sampler=sampler
        )

        print(f'ℹ️ [INFO] Optimizing xGBoost Classifier hyperparameters...\n')

        study.optimize(objective,
                    n_trials=15,
                    n_jobs=-1,
                    show_progress_bar=True)
        
        print(f'ℹ️ [INFO] Successful hyperparameter optimization.')
        print(f'ℹ️ [INFO] Best value: {study.best_value}.')
        print(f'ℹ️ [INFO] Best parameters: {study.best_params}.')    

    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while optimizing hyperparameters: {e}.')
        sys.exit(1)

    try:
        output_path = Path(__file__).parent / '../outputs' / 'tuning' / 'best_params.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump({'best_value': study.best_value, 'best_params': study.best_params}, f, indent=4)
        
        print(f'ℹ️ [INFO] Best params saved to {output_path}.')
        
        total_time = time.time() - start_time
        print(f'ℹ️ [INFO] Model Tuning phase - Total execution time: {total_time//60} min {total_time%60:.2f} sec.')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while exporting hyperparameters: {e}.')
        sys.exit(1)

if __name__=='__main__':

    script_dir = Path(__file__).parent
    dataset_path = script_dir / '../data' / 'preprocessed' / 'PreprocessedDataset.parquet'

    df = pd.read_parquet(dataset_path)

    X_train, _ , y_train, _ = split_data(df)

    tune_model(X_train, y_train)



    



