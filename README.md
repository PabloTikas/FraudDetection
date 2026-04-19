# FraudDetection
An end-to-end machine learning project for fraud detection in financial transactions.

## Executive Summary

This project walks through the full lifecycle of a machine learning product, from raw data exploration to a containerized, deployed web application. Starting with a synthetic financial transactions dataset, I performed exploratory data analysis, built and tuned a fraud detection classifier, then packaged the model behind a FastAPI backend and a Gradio frontend — all containerized with Docker and deployed to Hugging Face Spaces.

**Key learnings:**
- **Phase 1 — EDA & Tableau:** How to query a relational dataset with SQL to uncover data quality issues, distribution patterns, and fraud signals before touching any model; and how to translate those findings into an interactive dashboard that tells a clear story to a non-technical audience.
- **Phase 2 — Modeling & Experimentation:** Navigating class imbalance in fraud detection and choosing evaluation metrics (Recall, F1, PR-AUC) that reflect real business cost; and running systematic, reproducible experiments with Optuna for hyperparameter optimization.
- **Phase 3 — Modularization:** Refactoring Jupyter notebooks into a clean, importable Python module structure with well-separated concerns, so the codebase can grow and be reused beyond the notebook environment.
- **Phase 4 — Serving:** Building a REST API with FastAPI (Pydantic validation, automatic OpenAPI docs) and coupling it to an interactive Gradio UI so non-technical users can interact with the model directly.
- **Phase 5 — Containerization:** Writing a Dockerfile from scratch — layer ordering for cache efficiency, system-level dependencies for ML wheels, and exposing multiple ports for a multi-service app.
- **Phase 6 — Deployment:** Deploying a containerized ML app to Hugging Face Spaces and validating the end-to-end flow in a production-like environment.

**Live demo:** https://huggingface.co/spaces/PabloTikas/FraudDetectionApp

**Fraud Analysis Dashboard:** https://public.tableau.com/app/profile/pablo.tikas.pueyo/viz/FraudDashboard_17748659627020/Dashboard1


## Use of Artificial Intelligence

Most of the code in this project was written by myself, using AI tools (Claude and ChatGPT) primarily for debugging — looking up error messages, understanding unexpected behavior, and validating my reasoning. I believe this is the most effective way to learn in a project like this: doing the work yourself and using AI to unblock, not to shortcut.

The two areas where I leaned on AI more like a copilot were the **Gradio frontend** and the **Dockerfile**. Both were outside my prior experience. For the frontend, AI helped me structure the component layout and understand Gradio's API. For the Dockerfile, it helped me grasp the fundamentals of containerization — layer ordering, caching strategies, and how to expose multiple services — which I then applied and adapted myself.

## Data source
**Financial Transactions Dataset: Analytics (Kaggle)**

*This comprehensive financial dataset created by Caixabank Tech for the 2024 AI Hackathon combines transaction records, customer information, and card data from a banking institution, spanning across the 2010s decade. The dataset is designed for multiple analytical purposes, including synthetic fraud detection, customer behavior analysis, and expense forecasting.*

https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets

**Observation:** User and card attributes are static snapshots, not historical records. Features like `current_age`, `yearly_income`, and `per_capita_income` 
may not reflect their actual values at transaction time. Additionally, engineered features such as `avg_amount_cli`, `trans_count_cli`, and `years_since_pin_change` 
are computed using the entire dataset, introducing potential data leakage. These limitations are acknowledged and accepted throughout the project.

## Phase 1: Exploratory Data Analysis

### Phase Goals

- Develop a deep understanding of the dataset: fields in each table, relationships between fields, number of records, number of nulls, etc.
- Create an exhaustive report on the raw dataset.
- Create an insightful, interactive dashboard.

### Tech Stack

- **DBeaver** for database management + SQL queries.
- **Tableau Public** for data visualization.

## Phase 2: Modeling & Experimentation.

### Phase Goals

- Preprocess and prepare the dataset for modeling.
- Define a fraud-appropiate evaluation metric.
- Train and compare multiple classification models, tracking experiments systematically to ensure reproducibility and fair comparison.
- Select the best-performing model and optimize it through hyperparameter tuning.
- Evaluate final model performance on the test set and create a comprehensive Phase Report.

### Tech Stack

- **Jupyter Notebook** on **VSCode** as the development environment.
- **UV** for project dependencies management.
- Python Libraries:
    - **pandas** for Data Processing and Feature Engineering.
    - **scikit-learn** for Data Splitting and Modeling.
    - **optuna** for Hyperparameter Optimization.
    - **matplotlib** and **seaborn** for Visualization and Reporting.

## Phase 3: Modularization

### Phase Goals

- Refactor the experimental Jupyter notebooks into a clean, importable Python module structure.
- Separate concerns: data loading, preprocessing, training, tuning, and evaluation each become standalone, reusable components.
- Ensure the model artifact and its prediction pipeline can be imported cleanly by the serving layer.

### Tech Stack

- **Python modules** replacing notebook cells.
- **UV** for dependency management.
- **MLflow** for model artifact serialization and versioning.

## Phase 4: Serving (FastAPI + Frontend)

### Phase Goals

- Expose the model as a REST API so predictions can be requested programmatically.
- Build an interactive frontend that lets non-technical users submit transactions and receive fraud predictions without writing any code.

### Tech Stack

- **FastAPI** for the prediction API (input validation via Pydantic, automatic OpenAPI docs).
- **Gradio** for the interactive web frontend.
- **Uvicorn** as the ASGI server for FastAPI.

## Phase 5: Containerization

### Phase Goals

- Package the entire application (API + frontend + model artifact) into a single, reproducible Docker image.
- Ensure the image runs identically in any environment without manual dependency setup.

### Tech Stack

- **Docker** for containerization.
- A multi-service launch script (`runapp.sh`) that starts both the FastAPI backend and the Gradio frontend inside the same container.

## Phase 6: Deployment to Hugging Face Spaces

### Phase Goals

- Deploy the containerized application to a publicly accessible URL with zero infrastructure management.
- Validate the end-to-end flow in a production-like environment.

### Tech Stack

- **Hugging Face Spaces** (Docker runtime) for hosting.
- **GitHub** as the source repository connected to the Space.