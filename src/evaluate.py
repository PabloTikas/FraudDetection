import pandas as pd
from xgboost import XGBClassifier
from pathlib import Path
import mlflow
import mlflow.xgboost
from sklearn.metrics import average_precision_score, classification_report, roc_auc_score
import time
import json
import sys
from _utils import split_data


def evaluate_model(X_test: pd.DataFrame, y_test: pd.Series) -> None:
    start_time = time.time()

    try:
        mlruns_path = Path(__file__).parent / '../outputs' / 'mlruns.db'
        mlflow.set_tracking_uri('sqlite:///' + str(mlruns_path))

        client = mlflow.tracking.MlflowClient()

        experiment = client.get_experiment_by_name('FraudDetection')
        runs = client.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=['start_time DESC'],
            max_results=1
        )
        last_run = runs[0]
        run_id = last_run.info.run_id
        logged_models = client.search_logged_models(
            experiment_ids=[experiment.experiment_id],
            filter_string=f"source_run_id = '{run_id}'"
        )
        artifact_location = logged_models[0].artifact_location
        model = mlflow.xgboost.load_model(artifact_location)
        print(f'ℹ️ [INFO] Model successfully retrieved.')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while retrieving last trained model: {e}.')
        sys.exit(1)

    try:
        print(f'ℹ️ [INFO] Evaluating model...')
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1]

        # Compute metrics
        pr_auc = average_precision_score(y_test, y_prob)
        roc_auc = roc_auc_score(y_test, y_prob)
        report = classification_report(y_test, y_pred)
        print(f"ℹ️ [INFO] PR-AUC:  {pr_auc:.4f}")
        print(f"ℹ️ [INFO] ROC-AUC: {roc_auc:.4f}")
        print(f"ℹ️ [INFO] Classification Report: \n")
        print(report)
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while evaluating model: {e}.')
        sys.exit(1)

    try:
        print(f'ℹ️ [INFO] Logging evaluation...')
        dict_report = classification_report(y_test, y_pred, output_dict=True)
        evaluation = {
            "run_id": run_id,
            "artifact_location": artifact_location,
            "pr_auc": pr_auc,
            "roc_auc": roc_auc,
            "classification_report": dict_report
        }

        output_path = Path(__file__).parent / "../outputs" / "evaluation" / f"{run_id}_evaluation.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(evaluation, f, indent=4)

        print(f"ℹ️ [INFO] Evaluation saved to {output_path}")
        total_time = time.time() - start_time
        print(f'ℹ️ [INFO] Model Evaluation phase - Total execution time: {total_time//60} min {total_time%60:.2f} sec.')
    except Exception as e:
        print(f'⚠️ [SYS] An error ocurred while logging model evaluation: {e}.')
        sys.exit(1)

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    dataset_path = script_dir / '../data' / 'preprocessed' / 'PreprocessedDataset.parquet'

    df = pd.read_parquet(dataset_path)

    _, X_test, _, y_test = split_data(df)

    evaluate_model(X_test, y_test)