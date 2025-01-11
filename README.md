# Network Security Phishing Detection Project

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/FastAPI-✔-brightgreen.svg" alt="FastAPI">
  <img src="https://img.shields.io/badge/MLflow-Tracking-orange.svg" alt="MLflow">
  <img src="https://img.shields.io/badge/Docker-Container-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/AWS-ECR | ECS | S3 | IAM-yellow.svg" alt="AWS Deployment">
  <img src="https://img.shields.io/badge/MongoDB-✔-brightgreen.svg" alt="MongoDB">
  <img src="https://img.shields.io/badge/DagsHub-Tracking-purple.svg" alt="DagsHub">
  <img src="https://img.shields.io/badge/AWS EC2-Instance-blue.svg" alt="EC2">
  <img src="https://img.shields.io/badge/GitHub Actions-CI/CD-green.svg" alt="GitHub Actions">
  
</p>

## Overview
This project aims to build an end-to-end MLOps pipeline for **phishing detection** within a network security context. The ML model classifies URLs as phishing (`1`) or legitimate (`0`), leveraging data ingestion from MongoDB, data validation, transformation, model training, and deployment using various **CI/CD** and **AWS** services. 

<p align="center">
  <img src="https://img.icons8.com/color/96/shield.png" width="80" alt="shield emoji" />
</p>

## Table of Contents
1. [Key Features](#key-features)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Technologies Used](#technologies-used)
5. [Local Setup](#local-setup)
6. [Training & Prediction Workflow](#training--prediction-workflow)
7. [Environment Variables](#environment-variables)
8. [CI/CD Pipeline](#cicd-pipeline)
9. [S3 Usage in the Pipeline](#s3-usage-in-the-pipeline)
10. [DagsHub Integration](#dagshub)


---

## Key Features
- **Automated Data Ingestion** from MongoDB and saving as CSV.
- **Data Validation** checks (column counts, schema consistency, drift detection).
- **Data Transformation** using KNNImputer to handle missing values.
- **Model Training** with hyperparameter tuning across multiple classifiers (RandomForest, DecisionTree, LogisticRegression, etc.).
- **Model Tracking** with MLflow and Dagshub.
- **Containerization** via Docker for portable deployment.
- **CI/CD** using GitHub Actions to build, test, and push Docker images to AWS ECR.
- **Deployment** on AWS ECS with scaling and real-time inference.
- **FastAPI** for RESTful inference endpoints.
- **Logging & Exception Handling** with Python's `logging` and custom exception classes.
- **Artifact Storage** and **Model Backups** on AWS S3.

---

## Architecture

![Network Security Phishing Detection Pipeline](C:\Users\yotam\code_projects\networksecurity\architecture_network.png)

Below is a high-level overview of the project pipeline:

      ┌───────────────────────────┐
      │     MongoDB Database      │
      └───────────┬───────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │ Data Ingestion (CSV)  │
       └───────────┬───────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │  Data Validation      │
       └───────────┬───────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │Data Transformation    │
       └───────────┬───────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │    Model Training     │
       │   (MLflow Tracking)   │
       └───────────┬───────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  Model Artifact │
         └─────────────────┘
                  │
                  ▼
     ┌───────────────────────┐
     │ Docker Container (ECR)│
     └───────────┬───────────┘
                 │
                 ▼
         ┌──────────────────┐
         │    AWS ECS       │
         │ (Production Env) │
         └──────────────────┘


1. **MongoDB**: Raw data is stored in a collection and then ingested as a pandas DataFrame.
2. **Data Validation**: Ensures schema compliance and checks for any possible data drift.
3. **Data Transformation**: Cleans and transforms data (imputation, scaling, etc.).
4. **Model Training**: Trains multiple classifiers, logs metrics via MLflow, and saves the best model.
5. **Docker**: The final app is containerized.
6. **AWS ECS**: Container is deployed on ECS (Elastic Container Service).
7. **GitHub Actions**: Automates the entire flow, from code testing to Docker image building and pushing to ECR.
8. **AWS S3**: Stores intermediate artifacts, the final trained model, and backups.

---

## Project Structure

```bash
📦networksecurity
 ┣ 📂networksecurity
 ┃ ┣ 📂components
 ┃ ┃ ┣ 📜data_ingestion.py
 ┃ ┃ ┣ 📜data_transformation.py
 ┃ ┃ ┣ 📜data_validation.py
 ┃ ┃ ┗ 📜model_trainer.py
 ┃ ┣ 📂constants
 ┃ ┃ ┗ 📜training_pipeline.py
 ┃ ┣ 📂cloud
 ┃ ┃ ┗ 📜s3_syncer.py
 ┃ ┣ 📂entity
 ┃ ┃ ┣ 📜artifact_entity.py
 ┃ ┃ ┗ 📜config_entity.py
 ┃ ┣ 📂exception
 ┃ ┃ ┗ 📜exception.py
 ┃ ┣ 📂logging
 ┃ ┃ ┗ 📜logger.py
 ┃ ┣ 📂pipeline
 ┃ ┃ ┗ 📜training_pipeline.py
 ┃ ┣ 📂utils
 ┃ ┃ ┣ 📂main_utils
 ┃ ┃ ┃ ┗ 📜utils.py
 ┃ ┃ ┗ 📂ml_utils
 ┃ ┃   ┣ 📂metric
 ┃ ┃   ┃ ┗ 📜classification_metric.py
 ┃ ┃   ┗ 📂model
 ┃ ┃     ┗ 📜estimator.py
 ┃ ┣ 📜app.py
 ┃ ┣ 📜Dockerfile
 ┃ ┣ 📜requirements.txt
 ┃ ┗ 📜...
 ┣ 📂.github
 ┃ ┗ 📂workflows
 ┃   ┗ 📜main.yaml
 ┣ 📂data_schema
 ┃ ┗ 📜schema.yaml
 ┣ 📂logs
 ┃ ┗ ...
 ┣ 📂final_model
 ┃ ┗ ...
 ┣ 📂templates
 ┃ ┗ 📜table.html
 ┣ 📜README.md  <-- (You are here!)
 ┗ ...
```

# Key directories and files:

- **components**: Contains major pipeline steps (data ingestion, validation, transformation, modeling).
- **pipeline**: Orchestrates the entire end-to-end workflow using `TrainingPipeline`.
- **entity**: Data classes (artifacts and configuration entities) describing inputs/outputs across components.
- **app.py**: FastAPI application file providing two endpoints: training (`/train`) and prediction (`/predict`).
- **requirements.txt**: Project dependencies.
- **Dockerfile**: Instructions to build a Docker image containing this app.


## Technologies Used

- **Python 3.10**
- **FastAPI** for model inference via REST endpoints
- **Scikit-learn** for ML modeling
- **Pandas**, **NumPy** for data manipulation
- **MLflow & Dagshub** for experiment tracking
- **Docker** for containerization
- **AWS ECR, AWS ECS, AWS S3** for hosting containers, storing artifacts, and model deployment
- **GitHub Actions** for CI/CD pipelines
- **MongoDB** (Atlas or self-hosted) for data storage



## Local Setup

### Clone the Repository
```bash
git clone https://github.com/yourusername/networksecurity.git
cd networksecurity
```

### Create and Activate Virtual Environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or on Windows:
venv\Scripts\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Set Environment Variables
Create a .env file in the root directory:
```makefile
MONGO_DB_URL=<your_mongodb_connection>
AWS_ACCESS_KEY_ID=<your_aws_key>
AWS_SECRET_ACCESS_KEY=<your_aws_secret>
AWS_REGION=<aws_region>
```
note: Make sure to keep your credentials secure!

Run the App:
```bash
python app.py
```
The app will start at http://0.0.0.0:8000/docs.

## Training & Prediction Workflow
### Train the Model
Go to:
```bash
http://0.0.0.0:8000/train
```
1. Starts data ingestion from MongoDB.
2. Performs data validation and transformation.
3. Trains multiple models, logs them in MLflow, picks the best model.
4. Final model is saved in final_model/.

### Make Predictions

* Method: POST request to http://0.0.0.0:8000/predict.
* Parameters: A CSV file in the request body.
* Output: The CSV with an additional predicted_column appended, returned as an HTML table or JSON (depending on your logic).

## CI/CD Pipeline
I use **GitHub Actions** to:

1. **Integration**:
    - Lint code, run basic tests.

2. **Build and Push to ECR**:
    - Build a Docker image.
    - Push image to AWS ECR with tag latest.

3. **Continuous Deployment**:
    - Pull the latest image on a self-hosted runner or ECS instance.
    - Run the container with environment variables set.

The **main.yaml** GitHub Actions file orchestrates this entire process automatically on **git push** to the **main** branch.

## Runners

The following runners are available for this repository's CI/CD workflows:
    This runner is listening for GitHub Actions workflows and trigger the github actions workflows.
    **GitHub-hosted runners**: Default runners provided by GitHub Actions.
    **Self-hosted runners** (Repository runners)

## S3 Usage in the Pipeline
During the **TrainingPipeline** run:

* **Artifacts** (intermediate files, metrics, logs) generated by the pipeline are synced to an S3 bucket under artifact/<timestamp>.
* **Final Models** are stored in final_model/<timestamp> within the same S3 bucket.
These sync operations are handled by the S3Sync class, which uploads local directories to S3. In case of re-runs or deployment, you can retrieve these artifacts directly from S3 for consistency and backup.

## DagsHub
DagsHub is a platform that integrates version control for data and models, experiment tracking (via MLflow). By using DagsHub:

**Experiment Tracking**: DagsHub natively supports MLflow, so you can track experiments, metrics, and artifacts seamlessly.
**Easy Integration**: DagsHub repositories work similarly to GitHub, which makes onboarding simple if you already use Git.
