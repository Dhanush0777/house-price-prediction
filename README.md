# AI-Based House Price Prediction System Using Machine Learning & Java Full Stack

> **B.Tech CSE (AI & ML) Summer Internship Project**  
> An enterprise-grade, multi-tier full-stack application combining Machine Learning with Java Spring Boot, MySQL, and modern web technologies.

---

## 1. System Architecture

```
+-----------------------------------------------------------------------------------+
|                                 CLIENT TIER                                       |
|  - HTML5, CSS3, JavaScript (Fetch API), Bootstrap 5, FontAwesome                  |
|  - Modern single-page responsive interface (Port 8080 or standalone index.html)   |
+-----------------------------------------|-----------------------------------------+
                                          | HTTP REST (JSON)
                                          v
+-----------------------------------------------------------------------------------+
|                        APPLICATION BACKEND TIER (Port 8080)                       |
|  - Java 17/21/25 + Spring Boot 3 (Spring Web, Spring Data JPA, Hibernate, Maven)  |
|  - Validates DTOs, coordinates business logic, logs transactions                  |
|  - RestTemplate calls Python ML Inference Microservice                            |
+--------------------+------------------------------------+-------------------------+
                     |                                    |
     HTTP POST (JSON)| Port 5001               JDBC (SQL) | Port 3306
                     v                                    v
+------------------------------------+   +------------------------------------------+
|         AI / ML TIER (Port 5001)   |   |             DATABASE TIER                |
|  - Python 3 + Flask + Scikit-learn |   |  - MySQL 8.0 / Embedded H2 Database      |
|  - Preprocessing (OneHotEncoder +  |   |  - Table: `predictions`                  |
|    StandardScaler Pipeline)        |   |  - Persists property queries, timestamps,|
|  - Gradient Boosting Regressor     |   |    and computed fair market valuations   |
|    (R² = 0.9755, RMSE = ₹6.99L)    |   +------------------------------------------+
+------------------------------------+
```

---

## 2. Machine Learning Pipeline & Results

The dataset comprises **1,500 real-world residential property records** across 10 prominent urban localities with structural parameters (Built-up Area, Bedrooms, Bathrooms, Parking, Age, Floors).

### Model Evaluation & Comparison Table

| Model | MAE (₹) | RMSE (₹) | $R^2$ Score (Accuracy) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting Regressor** | **₹4,72,898.66** | **₹6,99,163.25** | **0.9755 (97.55%)** | **Selected for Production** |
| **Random Forest Regressor** | ₹5,02,078.83 | ₹8,03,088.39 | 0.9676 (96.76%) | Evaluated |
| **Ridge Regression** | ₹7,31,881.16 | ₹10,89,703.74 | 0.9404 (94.04%) | Evaluated |
| **Linear Regression** | ₹7,36,276.04 | ₹10,91,457.74 | 0.9402 (94.02%) | Baseline |
| **Decision Tree Regressor** | ₹7,54,712.59 | ₹15,80,425.50 | 0.8747 (87.47%) | Evaluated |

---

## 3. Project Directory Structure

```
project/
├── dataset/
│   └── house_data.csv                    # 1,500 housing records
├── ml_service/
│   ├── train_model.py                   # EDA, training, & evaluation script
│   ├── app.py                           # Flask REST API microservice (Port 5001)
│   ├── requirements.txt                 # Python dependencies
│   ├── locations.json                   # Supported localities
│   ├── metrics_summary.json             # Actual evaluation results
│   ├── model/
│   │   └── house_price_model.joblib     # Exported trained ML pipeline
│   └── eda_plots/                       # Generated EDA charts
├── backend/
│   ├── pom.xml                          # Maven build dependencies
│   └── src/main/
│       ├── java/com/houseprice/
│       │   ├── HousePriceApplication.java
│       │   ├── config/                  # CorsConfig, RestTemplateConfig
│       │   ├── controller/              # HousePriceController REST API
│       │   ├── dto/                     # PredictionRequest, PredictionResponse, etc.
│       │   ├── exception/               # GlobalExceptionHandler, Custom Exceptions
│       │   ├── model/                   # HousePrediction JPA Entity
│       │   ├── repository/              # HousePredictionRepository (Spring Data JPA)
│       │   └── service/                 # HousePredictionService (Business Logic)
│       └── resources/
│           ├── application.properties   # App configuration & DB settings
│           └── static/                  # Built-in Web UI (index.html, css, js)
├── frontend/
│   ├── index.html                       # Standalone UI interface
│   ├── css/style.css                    # Modern styling
│   └── js/app.js                        # JavaScript Fetch API logic
├── database/
│   └── schema.sql                       # MySQL DDL & DML scripts
├── run_project.bat                      # One-click Windows launcher
└── README.md                            # Comprehensive documentation
```

---

## 4. How to Run the Project

### Option A: One-Click Execution (Windows)
Double-click `run_project.bat`. It will automatically start the Python ML microservice, start the Spring Boot backend, and open `http://localhost:8080/` in your browser.

### Option B: Manual Step-by-Step Execution

#### Step 1: Start the Python ML Service
```bash
python ml_service/app.py
```
*The ML inference API will start on `http://localhost:5001`.*

#### Step 2: Start the Java Spring Boot Backend
```bash
cd backend
java -jar target/house-price-prediction-backend-1.0.0.jar
```
*(Or compile with: `mvn package -DskipTests`)*  
*The Spring Boot backend will start on `http://localhost:8080`.*

#### Step 3: Access the Web Application
Open your browser and navigate to:
`http://localhost:8080/`

---

## 5. REST API Endpoints Reference

| Method | Endpoint | Description | Sample Status |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/predict` | Computes ML prediction & persists transaction | `201 Created` |
| `GET` | `/api/predictions` | Lists all historical prediction records | `200 OK` |
| `GET` | `/api/predictions/{id}` | Fetches a single prediction by ID | `200 OK` |
| `DELETE`| `/api/predictions/{id}` | Deletes a prediction record by ID | `200 OK` |
| `GET` | `/api/analytics` | Returns total valuations, avg, min, max prices | `200 OK` |
| `GET` | `/api/locations` | Returns supported property localities | `200 OK` |
| `GET` | `/api/metrics` | Returns ML model comparison scores | `200 OK` |

---

## 6. Sample Prediction Request & Response

### Request (`POST /api/predict`):
```json
{
  "location": "Madhurawada",
  "area": 1500,
  "bedrooms": 3,
  "bathrooms": 2,
  "parking": 1,
  "propertyAge": 5,
  "floors": 2
}
```

### Response (`201 Created`):
```json
{
  "id": 1,
  "location": "Madhurawada",
  "area": 1500.0,
  "bedrooms": 3,
  "bathrooms": 2,
  "parking": 1,
  "propertyAge": 5,
  "floors": 2,
  "predictedPrice": 7344527.85,
  "formattedPrice": "₹73,44,527.85",
  "formattedPriceInLakhs": "73.45 Lakhs",
  "predictionDate": "2026-08-27T13:42:14",
  "modelUsed": "Gradient Boosting Regressor"
}
```
