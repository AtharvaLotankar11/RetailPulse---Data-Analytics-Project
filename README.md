# RetailPulse – AI-Powered Customer Analytics & Demand Forecasting Platform

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/MachineLearning-RetailAnalytics-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-ProductionReady-orange?style=for-the-badge">
</p>

---

# 📊 Project Overview

RetailPulse is an end-to-end AI-powered Retail Analytics and Demand Forecasting platform designed to help retail businesses make data-driven decisions using Data Science, Machine Learning, Forecasting, and Business Intelligence techniques.

The system analyzes customer behavior, predicts future sales demand, identifies customers likely to churn, and provides inventory optimization recommendations through an interactive Streamlit dashboard.

This project simulates a real-world industry-level analytics pipeline involving:
- Data Cleaning
- Exploratory Data Analysis
- Customer Analytics
- Machine Learning
- Time-Series Forecasting
- Inventory Optimization
- Dashboard Development
- Deployment

---

# 🚀 Business Problem

Retail businesses commonly face problems such as:

- Inaccurate sales forecasting
- Overstocking and understocking
- Poor customer retention
- Revenue loss due to inventory inefficiencies
- Lack of customer insights
- Inefficient demand planning

RetailPulse solves these problems using:
- Predictive analytics
- Customer segmentation
- Demand forecasting
- Churn prediction
- Inventory optimization

---

# 🎯 Project Objectives

The main objectives of RetailPulse are:

- Analyze retail sales trends
- Identify customer purchasing patterns
- Segment customers using RFM analysis
- Predict future sales demand
- Detect customer churn risk
- Optimize inventory recommendations
- Provide interactive analytics dashboards
- Deploy a production-ready web application

---

# 🧠 Core Modules

The project consists of 4 major modules.

---

## 1. Sales Analytics Module

Provides insights into:
- Revenue trends
- Monthly sales
- Best-selling products
- Country-wise performance
- Product-wise analysis
- Daily sales trends

---

## 2. Customer Analytics Module

Provides:
- RFM analysis
- Customer segmentation
- Customer behavior analysis
- Churn prediction
- High-value customer identification

---

## 3. Demand Forecasting Module

Predicts:
- Future sales demand
- Product demand trends
- Seasonal sales patterns
- Forecast graphs
- Monthly forecasting insights

---

## 4. Inventory Optimization Module

Provides:
- Reorder quantity recommendations
- Low stock alerts
- Overstock analysis
- Inventory recommendations
- Demand-based stock planning

---

# 🏗️ System Architecture

```text
Raw Retail Dataset
        ↓
Data Cleaning & Preprocessing
        ↓
Feature Engineering
        ↓
Exploratory Data Analysis
        ↓
Customer Segmentation + Churn Prediction
        ↓
Demand Forecasting
        ↓
Inventory Optimization
        ↓
Streamlit Dashboard
        ↓
Docker Containerization
        ↓
Deployment (Cloud/Local)
```

## Container Architecture

```text
┌─────────────────────────────────────────┐
│         Docker Container                │
│  ┌───────────────────────────────────┐  │
│  │   Streamlit Application           │  │
│  │   - Home.py                       │  │
│  │   - Sales Dashboard               │  │
│  │   - Customer Dashboard            │  │
│  │   - Forecast Dashboard            │  │
│  │   - Inventory Dashboard           │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │   Python 3.11 Runtime             │  │
│  │   - ML Libraries                  │  │
│  │   - Data Processing               │  │
│  │   - Visualization Tools           │  │
│  └───────────────────────────────────┘  │
│                                         │
│  Port: 8501                             │
│  Health Check: /_stcore/health          │
└─────────────────────────────────────────┘
         ↓
    Host Machine
    localhost:8501
```

---

# 📁 Project Structure

```text
RetailPulse/
│
├── data/
│   ├── cleaned_retail.csv
│   ├── customer_segments.csv
│   ├── forecast_results.csv
│   └── inventory_recommendations.csv
│
├── notebooks/
│   ├── 01_data_cleaning_and_eda.ipynb
│   ├── 02_Customer_analytics.ipynb
│   └── forecasting.ipynb
│
├── dashboard/
│   ├── Home.py
│   └── pages/
│       ├── 1_Sales_Dashboard.py
│       ├── 2_Customer_Dashboard.py
│       ├── 3_Forecast_Dashboard.py
│       └── 4_Inventory_Dashboard.py
│
├── models/
│
├── assets/
│
├── reports/
│
├── requirements.txt
│
└── README.md
```

---

# 📦 Datasets Used

## Primary Datasets

- UCI Online Retail Dataset
- Online Retail II Dataset
- Kaggle Retail Dataset

---

# 📌 Important Dataset Columns

| Column Name | Description |
|---|---|
| InvoiceNo | Invoice Number |
| StockCode | Product Code |
| Description | Product Description |
| Quantity | Product Quantity |
| InvoiceDate | Transaction Date |
| UnitPrice | Price Per Unit |
| CustomerID | Customer Identifier |
| Country | Customer Country |

---

# ⚙️ Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn, XGBoost |
| Forecasting | Prophet, ARIMA, LSTM |
| Dashboard | Streamlit |
| Containerization | Docker, Docker Compose |
| Deployment | Streamlit Cloud / Docker / Cloud Platforms |
| Version Control | GitHub |
| Notebook Environment | Jupyter Notebook |
| CI/CD | GitHub Actions |

---

# 🔄 Complete Workflow

---

# Step 1 – Dataset Collection

Tasks:
- Download retail datasets
- Understand dataset structure
- Identify important columns
- Validate dataset quality

Output:
- Raw dataset files

---

# Step 2 – Environment Setup

Install required libraries:

```bash
pip install pandas numpy matplotlib seaborn plotly streamlit scikit-learn prophet xgboost joblib openpyxl
```

---

# Step 3 – Load Dataset

Tasks:
- Load CSV/Excel files
- Understand datatypes
- View sample records
- Check dataset dimensions

Example:

```python
import pandas as pd

df = pd.read_csv("online_retail.csv")
```

---

# Step 4 – Data Cleaning

Tasks:
- Remove null values
- Remove duplicate records
- Remove cancelled orders
- Convert date columns
- Handle outliers
- Remove invalid quantities

Important Operations:
- Drop null CustomerID
- Remove negative quantities
- Convert InvoiceDate to datetime

Output:
- Cleaned dataset

---

# Step 5 – Feature Engineering

Created Features:
- TotalPrice
- Recency
- Frequency
- Monetary
- Monthly sales
- Customer lifetime value
- Rolling averages

Example:

```python
df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
```

Output:
- Feature-engineered dataset

---

# Step 6 – Exploratory Data Analysis (EDA)

Analysis Performed:
- Monthly sales trends
- Revenue analysis
- Top-selling products
- Seasonal trends
- Customer behavior analysis
- Country-wise performance

Visualizations:
- Bar charts
- Pie charts
- Heatmaps
- Correlation matrices
- Line graphs

Output:
- EDA notebook
- Business insights

---

# Step 7 – Customer Segmentation (RFM Analysis)

Processes:
- RFM score calculation
- Customer clustering
- Segment analysis

Algorithms Used:
- KMeans Clustering
- DBSCAN

Customer Groups:
- Premium Customers
- Loyal Customers
- Regular Customers
- At-risk Customers
- Low-value Customers

Output:
- Segmented customers
- Cluster visualizations

---

# Step 8 – Demand Forecasting

Objective:
Predict future product demand and sales.

Models Used:
- Prophet
- ARIMA
- LSTM

Forecasting Tasks:
- Daily forecasting
- Monthly sales prediction
- Seasonal analysis
- Trend analysis

Metrics:
- MAE
- RMSE
- MAPE

Output:
- Forecast graphs
- Predicted demand values

---

# Step 9 – Churn Prediction

Objective:
Identify customers likely to stop purchasing.

Features Used:
- Recency
- Frequency
- Monetary
- Purchase intervals
- Customer activity

Models Used:
- XGBoost
- Random Forest
- Logistic Regression

Prediction Classes:
- High churn risk
- Medium churn risk
- Low churn risk

Metrics:
- Accuracy
- Precision
- Recall
- AUC Score

Output:
- Churn prediction model
- Customer risk analysis

---

# Step 10 – Inventory Optimization

Objective:
Recommend stock levels using forecasted demand.

Logic:

```python
Suggested_Stock = Forecasted_Demand - Current_Inventory
```

Features:
- Reorder quantity
- Low stock alerts
- Overstock analysis

Output:
- Inventory recommendation system

---

# Step 11 – Streamlit Dashboard Development

The dashboard contains 4 pages.

---

## 📈 Sales Dashboard

Features:
- Revenue KPIs
- Monthly sales trends
- Country-wise revenue
- Product analysis
- Daily sales trends

---

## 👥 Customer Dashboard

Features:
- RFM analysis
- Customer segmentation
- Churn analysis
- Customer insights
- Cluster visualizations

---

## 📉 Forecast Dashboard

Features:
- Forecast visualizations
- Future demand predictions
- Seasonal trend analysis
- Forecast comparisons

---

## 📦 Inventory Dashboard

Features:
- Inventory recommendations
- Stock alerts
- Overstock analysis
- Understock warnings

---

# 👨‍💻 Team Structure & Responsibilities

---

## Member 1 – Data Processing & EDA Lead

**Name:** Het Patel

Responsibilities:
- Dataset collection
- Data cleaning
- Feature engineering
- Exploratory Data Analysis
- Visualization preparation

Deliverables:
- Clean dataset
- EDA notebook
- Business insights report

Technologies:
- Pandas
- NumPy
- Matplotlib
- Seaborn

---

## Member 2 – Customer Analytics Lead

**Name:** Ved Zala

Responsibilities:
- RFM analysis
- Customer segmentation
- Churn prediction
- Customer behavior analysis

Deliverables:
- Segmentation model
- Churn prediction model
- Cluster analysis

Technologies:
- Scikit-learn
- XGBoost
- KMeans

---

## Member 3 – Forecasting & Inventory Lead

**Name:** Parth Shah

Responsibilities:
- Time-series analysis
- Demand forecasting
- Forecast visualization
- Inventory optimization logic

Deliverables:
- Forecasting model
- Inventory recommendation system

Technologies:
- Prophet
- ARIMA
- LSTM

---

## Member 4 – Dashboard & Deployment Lead

**Name:** Atharva Lotankar

Responsibilities:
- Streamlit dashboard
- UI integration
- Model integration
- Deployment
- GitHub management

Deliverables:
- Working dashboard
- Live deployment link
- Demo presentation

Technologies:
- Streamlit
- GitHub
- Streamlit Cloud

---

# 🗓️ Weekly Execution Plan

---

## Week 1 – Data Preparation & EDA

Tasks:
- Data cleaning
- Missing value handling
- Feature engineering
- Trend analysis

---

## Week 2 – Machine Learning Development

Tasks:
- RFM analysis
- Clustering
- Time-series forecasting
- Churn prediction

---

## Week 3 – Dashboard Integration

Tasks:
- Streamlit UI development
- Graph integration
- Dashboard testing
- Model integration

---

## Week 4 – Deployment & Finalization

Tasks:
- GitHub cleanup
- Deployment
- Demo recording
- Documentation
- Final report creation

---

# 📊 Dashboard Features

The Streamlit dashboard includes:
- Interactive charts
- KPIs
- Filters
- Forecast visualizations
- Segment analysis
- Inventory alerts
- Downloadable reports

---

# 📌 Streamlit Pages

| Page | Description |
|---|---|
| Home | Project Overview |
| Sales Dashboard | Revenue & Sales Analytics |
| Customer Dashboard | Segmentation & Churn Analysis |
| Forecast Dashboard | Demand Forecasting |
| Inventory Dashboard | Inventory Recommendations |

---

# ▶️ Running the Project

---

## 1. Clone Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

---

## 2. Navigate to Project Folder

```bash
cd RetailPulse
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

---

## 4. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Run Streamlit Dashboard

```bash
streamlit run dashboard/Home.py
```

---

# 🌐 Deployment

## Live Application

🚀 **Live Demo:** [RetailPulse Dashboard](https://retailpulse-analytics.streamlit.app)

✅ **Status:** Successfully deployed and operational!

> Access the live dashboard to explore customer analytics, sales trends, demand forecasting, and inventory management in real-time.

### Docker Command Reference

**Essential Commands:**
```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs -f

# Restart application
docker-compose restart

# Rebuild and start
docker-compose up -d --build

# Check container status
docker ps

# Execute commands in container
docker exec -it retailpulse bash

# View resource usage
docker stats retailpulse

# Remove all containers and images
docker-compose down -v
docker system prune -a
```

**Debugging Commands:**
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' retailpulse

# View last 100 log lines
docker logs --tail 100 retailpulse

# Follow logs in real-time
docker logs -f retailpulse

# Check container processes
docker top retailpulse

# Inspect container configuration
docker inspect retailpulse
```

---

## Deployment Platforms

RetailPulse supports multiple deployment options:

### 🐳 Docker (Recommended)
- **Best for:** Production deployments, local development, CI/CD pipelines
- **Advantages:** Consistent environment, easy scaling, portable
- **Setup time:** < 5 minutes
- **Documentation:** See Docker Deployment section above

### ☁️ Cloud Platforms

#### Streamlit Cloud
- **Best for:** Quick demos, prototypes, free hosting
- **Advantages:** Zero configuration, automatic updates from GitHub
- **Limitations:** Resource constraints, public repositories preferred

#### AWS ECS/Fargate
- **Best for:** Enterprise production deployments
- **Advantages:** Auto-scaling, load balancing, AWS ecosystem integration
- **Requirements:** AWS account, ECR for container registry

#### Azure Container Instances
- **Best for:** Serverless container deployments
- **Advantages:** Pay-per-second billing, quick deployment
- **Requirements:** Azure account, Azure Container Registry

#### Google Cloud Run
- **Best for:** Serverless, auto-scaling deployments
- **Advantages:** Scale to zero, pay per request
- **Requirements:** GCP account, Container Registry

#### Render
- **Best for:** Simple cloud deployments with Docker
- **Advantages:** Easy setup, automatic SSL, free tier available
- **Requirements:** GitHub repository

#### Kubernetes
- **Best for:** Large-scale, multi-container orchestration
- **Advantages:** Advanced orchestration, high availability
- **Requirements:** K8s cluster, container registry

---

## 🐳 Docker Deployment (Recommended)

RetailPulse is fully containerized using Docker for easy deployment, scalability, and consistency across environments.

### Prerequisites

- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose 2.0+ (included with Docker Desktop)
- 2GB+ available RAM
- 1GB+ available disk space

### Quick Start with Docker Compose

The easiest way to run RetailPulse is using Docker Compose:

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/RetailPulse.git
cd RetailPulse

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Access the dashboard
# Open browser: http://localhost:8501
```

**Stop the application:**
```bash
docker-compose down
```

**Rebuild after code changes:**
```bash
docker-compose up -d --build
```

### Alternative: Docker CLI

For more control, use Docker CLI commands directly:

```bash
# Build the image
docker build -t retailpulse-analytics:latest .

# Run the container
docker run -d \
  -p 8501:8501 \
  --name retailpulse \
  -v $(pwd)/data:/app/data:ro \
  retailpulse-analytics:latest

# View real-time logs
docker logs -f retailpulse

# Stop the container
docker stop retailpulse

# Remove the container
docker rm retailpulse

# Remove the image
docker rmi retailpulse-analytics:latest
```

### Development Mode with Hot-Reload

For active development with automatic code reloading:

```bash
# Start in development mode
docker-compose -f docker-compose.dev.yml up

# The dashboard will automatically reload when you save changes
# Access at: http://localhost:8501
```

**Development features:**
- Live code reloading on file changes
- Full project mounted as volumes
- Streamlit's `runOnSave` enabled
- Immediate feedback during development

### Docker Configuration Details

#### Dockerfile Features

- **Multi-stage build** for optimized image size (~500MB)
- **Python 3.11-slim** base image
- **Non-root user** for enhanced security
- **Health checks** for container monitoring
- **Environment variables** for Streamlit configuration
- **Minimal dependencies** for faster builds

#### Docker Compose Services

**Production (`docker-compose.yml`):**
- Read-only data volumes for security
- Automatic restart policy
- Health check monitoring
- Isolated network
- Port mapping: 8501:8501

**Development (`docker-compose.dev.yml`):**
- Read-write volumes for hot-reload
- Full project mounted
- Development-friendly settings
- Streamlit auto-reload enabled

### Environment Variables

Configure the application using environment variables:

```bash
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
STREAMLIT_SERVER_RUN_ON_SAVE=true  # Dev mode only
```

### Volume Mounts

The Docker setup uses volumes for data persistence:

```yaml
volumes:
  - ./data:/app/data:ro              # Data files (read-only)
  - ./notebooks:/app/notebooks:ro    # Jupyter notebooks (read-only)
  - ./.streamlit:/app/.streamlit:ro  # Streamlit config (read-only)
```

### Health Checks

The container includes automatic health monitoring:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3
  CMD curl -f http://localhost:8501/_stcore/health || exit 1
```

**Check container health:**
```bash
docker ps
# Look for "healthy" status in the STATUS column

# Or use inspect
docker inspect --format='{{.State.Health.Status}}' retailpulse
```

### Troubleshooting Docker Deployment

#### Container won't start
```bash
# Check logs for errors
docker logs retailpulse

# Verify port availability
netstat -an | grep 8501  # Linux/Mac
netstat -an | findstr 8501  # Windows
```

#### Permission issues
```bash
# Ensure data files are readable
chmod -R 755 data/

# Check container user
docker exec retailpulse whoami
```

#### Memory issues
```bash
# Increase Docker memory limit (Docker Desktop)
# Settings → Resources → Memory → 4GB+

# Check container resource usage
docker stats retailpulse
```

#### Rebuild from scratch
```bash
# Remove everything and rebuild
docker-compose down -v
docker system prune -a
docker-compose up -d --build
```

### Docker Best Practices

✅ **Security:**
- Runs as non-root user (UID 1000)
- Read-only volume mounts in production
- No sensitive data in image layers
- Minimal attack surface

✅ **Performance:**
- Multi-stage builds reduce image size
- Layer caching for faster rebuilds
- Optimized dependency installation
- Health checks for reliability

✅ **Portability:**
- Works on Linux, macOS, Windows
- Consistent environment across machines
- Easy CI/CD integration
- Cloud-ready architecture

---

## Deployment Steps

### Deploying to Streamlit Cloud

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Sign up for Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io/)
   - Sign in with your GitHub account

3. **Deploy Application**
   - Click "New app"
   - Select your repository: `RetailPulse_Team_1`
   - Set main file path: `dashboard/Home.py`
   - Click "Deploy"

4. **Configure Settings** (if needed)
   - Python version: 3.11
   - Advanced settings: Add any environment variables

5. **Verify Deployment**
   - Wait for build to complete
   - Test all dashboard pages
   - Verify data loads correctly

### Deploying with Docker to Cloud Platforms

#### AWS ECS
```bash
# Push to ECR and deploy to ECS
aws ecr get-login-password --region region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.region.amazonaws.com
docker tag retailpulse-analytics:latest aws_account_id.dkr.ecr.region.amazonaws.com/retailpulse:latest
docker push aws_account_id.dkr.ecr.region.amazonaws.com/retailpulse:latest
```

#### Azure Container Instances
```bash
az container create --resource-group myResourceGroup --name retailpulse --image retailpulse-analytics --dns-name-label retailpulse --ports 8501
```

#### Google Cloud Run
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/retailpulse-analytics
gcloud run deploy retailpulse --image gcr.io/PROJECT_ID/retailpulse-analytics --platform managed
```

## Post-Deployment Checklist

### Application Verification
- [ ] All pages load without errors
- [ ] Data visualizations render correctly
- [ ] Filters and interactions work
- [ ] CSV exports function properly
- [ ] Navigation between pages works smoothly

### Docker-Specific Checks
- [ ] Container starts successfully (`docker ps` shows "healthy")
- [ ] Health checks pass (`docker inspect` shows healthy status)
- [ ] Container logs show no errors (`docker logs`)
- [ ] Port 8501 is accessible
- [ ] Volume mounts work correctly
- [ ] Container restarts automatically on failure
- [ ] Resource usage is within limits (`docker stats`)

### Cloud Deployment Checks
- [ ] Application accessible via public URL
- [ ] SSL/HTTPS enabled (if applicable)
- [ ] Environment variables configured
- [ ] Monitoring and logging enabled
- [ ] Auto-scaling configured (if applicable)

### Final Steps
- [ ] Share deployment URL with team
- [ ] Document any custom configurations
- [ ] Set up monitoring alerts
- [ ] Create backup strategy

---

# 📈 Key Performance Metrics

| Module | Metrics |
|---|---|
| Forecasting | RMSE, MAPE |
| Churn Prediction | Accuracy, AUC |
| Segmentation | Silhouette Score |
| Dashboard | User Experience |

---

# ⚠️ Challenges Faced

Technical Challenges:
- Handling missing values
- Time-series forecasting complexity
- Dashboard integration
- Deployment debugging

Team Challenges:
- Merge conflicts
- Coordination issues
- Model integration

---

# ✅ Best Practices Followed

Technical:
- Modular code structure
- Reusable functions
- Clean notebooks
- Version control using GitHub
- Saved trained models

Team:
- Daily updates
- Weekly meetings
- Shared documentation
- Common coding standards

---

# 📸 Dashboard Screenshots

## Home Page
![Home Dashboard](assets/screenshots/home.png)
*Overview page with KPIs and quick insights*

## Sales Dashboard
![Sales Dashboard](assets/screenshots/sales_dashboard.png)
*Revenue trends, top products, and sales analytics*

## Customer Dashboard
![Customer Dashboard](assets/screenshots/customer_dashboard.png)
*Customer segmentation and RFM analysis*

## Forecast Dashboard
![Forecast Dashboard](assets/screenshots/forecast_dashboard.png)
*Demand forecasting and predictive analytics*

## Inventory Dashboard
![Inventory Dashboard](assets/screenshots/inventory_dashboard.png)
*Stock alerts and inventory recommendations*

---

# 🔮 Future Enhancements

- Real-time streaming analytics with live data pipelines
- Advanced deep learning models (LSTM, Transformer) for multi-step forecasting
- AI-powered personalized recommendation engine

---

# 📚 Learning Outcomes

This project provides practical experience in:
- Data preprocessing
- Data visualization
- Machine learning
- Time-series forecasting
- Customer analytics
- Dashboard development
- Deployment pipelines
- GitHub collaboration

---

# 🧪 Example Streamlit Components

```python
import streamlit as st

st.title("RetailPulse Dashboard")

st.metric("Total Revenue", "$1,200,000")

st.sidebar.selectbox(
    "Select Country",
    ["UK", "USA", "Germany"]
)
```

---

# 📌 Important Python Libraries Used

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from sklearn.cluster import KMeans
from prophet import Prophet
```

---

# 📦 Final Deliverables

The final submission includes:

- GitHub Repository
- Streamlit Dashboard
- Live Deployment Link
- Project Report PDF
- README Documentation

---

# 🏁 Final Outcome

At the end of the project, the team successfully develops:

✅ Industry-level retail analytics solution  
✅ Machine learning forecasting system  
✅ Customer intelligence platform  
✅ Inventory optimization system  
✅ Interactive business dashboard  
✅ Deployment-ready web application  

---

# 🙌 Conclusion

RetailPulse is a complete end-to-end Data Science and Analytics solution designed to solve real-world retail business problems.

The project combines:
- Data Analytics
- Machine Learning
- Forecasting
- Customer Intelligence
- Dashboard Development
- Deployment

This project demonstrates strong practical skills in:
- Retail analytics
- Business intelligence
- Machine learning engineering
- Dashboard development
- Production deployment

---

# 👥 Development Team

| <img src="https://github.com/Vedzala.png" width="100" height="100" style="border-radius:50%"><br/>**Ved Zala**<br/>Customer Analytics Lead<br/>[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/Vedzala) | <img src="https://github.com/Hetpatel5681.png" width="100" height="100" style="border-radius:50%"><br/>**Het Patel**<br/>Data Processing & EDA Lead<br/>[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/Hetpatel5681) | <img src="https://github.com/23dcs120.png" width="100" height="100" style="border-radius:50%"><br/>**Parth Shah**<br/>Forecasting & Inventory Lead<br/>[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/23dcs120) | <img src="https://github.com/AtharvaLotankar11.png" width="100" height="100" style="border-radius:50%"><br/>**Atharva Lotankar**<br/>Dashboard & Deployment Lead<br/>[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=flat&logo=github)](https://github.com/AtharvaLotankar11) |
|:---:|:---:|:---:|:---:|

---

Developed for:
Zidio Development – Data Science & Analytics Domain

---