FROM python:3.11-slim

# System deps that some ML wheels (xgboost) need at runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first so this layer caches when only code changes
COPY app/app_requirements.txt .
RUN pip install --no-cache-dir -r app_requirements.txt

# Copy app code, model artifact, category metadata, launcher
COPY app/api.py app/frontend.py app/model.py app/serving_model.pkl app/valid_categories.json app/runapp.sh ./

# Make bash script executable
RUN chmod +x runapp.sh

# 7860 = Gradio UI, 8000 = FastAPI (also exposed so you can curl it)
EXPOSE 7860 8000

CMD ["./runapp.sh"]