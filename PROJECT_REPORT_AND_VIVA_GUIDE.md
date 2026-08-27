# INTERNSHIP CASE STUDY REPORT & VIVA DEFENSE GUIDE

**Project Title:** AI-Based House Price Prediction System Using Machine Learning & Java Full Stack Development  
**Academic Degree:** B.Tech CSE (Artificial Intelligence & Machine Learning)  
**Internship Domain:** Java Full Stack Development with AI Integration  

---

## 1. ABSTRACT
Real estate valuation has traditionally suffered from high subjectivity, broker bias, and slow manual appraisals. This project presents an enterprise-grade, multi-tier web application that automates fair market house price prediction using machine learning regression algorithms integrated with a Java Spring Boot backend, a relational database, and a responsive web interface. 

A dataset of 1,500 residential records across 10 prominent urban localities was analyzed through Exploratory Data Analysis (EDA) and feature engineering. Multiple regression models—Linear Regression, Ridge Regression, Decision Tree, Random Forest, and Gradient Boosting—were trained and evaluated. The Gradient Boosting Regressor achieved the highest accuracy with an $R^2$ score of **0.9755 (97.55%)**, a Root Mean Squared Error (RMSE) of **₹6,99,163.25**, and a Mean Absolute Error (MAE) of **₹4,72,898.66**. The trained pipeline was serialized and deployed as a Python Flask microservice, which communicates via JSON REST APIs with a Java Spring Boot backend. The backend enforces input validation, coordinates business transactions, logs historical valuation queries into MySQL via Spring Data JPA, and exposes endpoints to a modern Bootstrap 5 web frontend.

---

## 2. PROBLEM STATEMENT
Manual property appraisal methods are time-consuming, expensive, and subjective. Rule-of-thumb per-square-foot calculations fail to account for multi-variable interactions like age depreciation, parking spaces, floor level, and locality premiums. There is an absence of unified full-stack applications that combine machine learning models with enterprise backend persistence and intuitive web interfaces.

---

## 3. OBJECTIVES
1. Develop an end-to-end Machine Learning pipeline in Python for real estate valuation.
2. Compare multiple regression models ($R^2$, RMSE, MAE) and select the optimal model.
3. Expose the ML model via a high-performance Python Flask REST inference service.
4. Architect a Java Spring Boot 3 enterprise backend implementing clean N-tier separation (`Controller`, `Service`, `Repository`, `Model`, `DTO`, `Exception`).
5. Persist prediction transactions in a relational database (MySQL/H2) with Spring Data JPA.
6. Design a modern, responsive web frontend (HTML5, CSS3, JavaScript Fetch API, Bootstrap 5).
7. Implement robust error handling, client/server input validation, and real-time analytics.

---

## 4. SYSTEM ARCHITECTURE & INTEGRATION FLOW

### High-Level Data Flow:
```
[User Browser (HTML5/CSS/JS/Bootstrap 5)]
        │
        │ 1. HTTP POST /api/predict (JSON)
        ▼
[Java Spring Boot Backend (Port 8080)]
        │
        │ 2. HTTP POST /predict (JSON via RestTemplate)
        ▼
[Python ML Flask Service (Port 5001)]
        │
        │ 3. OneHotEncoding + StandardScaler + GradientBoosting Inference
        ▼
[Predicted Price: ₹73,44,527.85]
        │
        │ 4. HTTP 200 JSON Response
        ▼
[Java Spring Boot Backend]
        │
        │ 5. INSERT into `predictions` table via Spring Data JPA / Hibernate
        ▼
[MySQL Database (Port 3306) / H2 In-Memory DB]
        │
        │ 6. Formatted Response JSON with INR Currency & Analytics
        ▼
[User Browser: Live Animated Result Card & History Update]
```

---

## 5. MACHINE LEARNING METHODOLOGY & RESULTS

### Feature Set
- **Locality (`location`)**: Categorical (10 locations: MVP Colony, Seethammadhara, Siripuram, Rushikonda, Madhurawada, Yendada, Gajuwaka, Muralinagar, Sujathanagar, Pendurthi)
- **Built-up Area (`area`)**: Numerical (sq.ft: 500 – 4800)
- **Bedrooms (`bedrooms`)**: Discrete (1 to 5 BHK)
- **Bathrooms (`bathrooms`)**: Discrete (1 to 5)
- **Parking Spaces (`parking`)**: Discrete (0 to 3)
- **Property Age (`property_age`)**: Discrete (0 to 25 years)
- **Total Floors (`floors`)**: Discrete (1 to 4)
- **Target Variable (`price`)**: Continuous (in Indian Rupees ₹)

### Preprocessing Pipeline:
- Categorical features encoded with `OneHotEncoder(handle_unknown='ignore')`.
- Numerical features scaled with `StandardScaler()`.
- Combined using `ColumnTransformer` and encapsulated in `scikit-learn.pipeline.Pipeline`.
- Split: 80% Training set (1,200 records), 20% Testing set (300 records), `random_state=42`.

### Actual Experimental Results:

| Model | MAE (₹) | RMSE (₹) | $R^2$ Score | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Gradient Boosting Regressor** | **₹4,72,898.66** | **₹6,99,163.25** | **0.9755** | **Optimal: Captures non-linear boosts & depreciation** |
| **Random Forest Regressor** | ₹5,02,078.83 | ₹8,03,088.39 | 0.9676 | Strong ensemble performance |
| **Ridge Regression (L2)** | ₹7,31,881.16 | ₹10,89,703.74 | 0.9404 | Regularized baseline |
| **Linear Regression** | ₹7,36,276.04 | ₹10,91,457.74 | 0.9402 | Standard linear baseline |
| **Decision Tree Regressor** | ₹7,54,712.59 | ₹15,80,425.50 | 0.8747 | Prone to variance on continuous target |

---

## 6. BACKEND & DATABASE SPECIFICATIONS

- **Framework:** Spring Boot 3.3.4 (Java 17/21/25 LTS)
- **Architectural Pattern:** Layered Microservice / RESTful API
- **ORM / Persistence:** Spring Data JPA + Hibernate
- **Database Engine:** MySQL 8.0 (with zero-config embedded H2 fallback)
- **Entity Model:** `HousePrediction` (`id`, `location`, `area`, `bedrooms`, `bathrooms`, `parking`, `property_age`, `floors`, `predicted_price`, `prediction_date`)
- **Key Backend Endpoints:**
  - `POST /api/predict` — Validates input, requests prediction from Python, saves to database, returns DTO.
  - `GET /api/predictions` — Returns historical logs sorted chronologically.
  - `GET /api/predictions/{id}` — Fetches specific prediction by ID.
  - `DELETE /api/predictions/{id}` — Removes record from database.
  - `GET /api/analytics` — Computes aggregate metrics (total queries, average, minimum, maximum valuation).
  - `GET /api/locations` — Returns locality catalog.
  - `GET /api/metrics` — Exposes model evaluation comparison statistics.

---

## 7. COMPREHENSIVE VIVA / INTERVIEW Q&A PREPARATION

### A. Machine Learning Questions

**Q1: What is Machine Learning and why did you choose regression for this problem?**  
**Answer:** Machine Learning is a subfield of Artificial Intelligence where algorithms learn patterns from historical data to make predictions without being explicitly programmed. We chose regression because the target variable (`price`) is a continuous numerical value (currency in INR), unlike classification which predicts discrete categories.

**Q2: What is the difference between Linear Regression, Decision Trees, and Random Forest / Gradient Boosting?**  
**Answer:**
- *Linear Regression* models a linear relationship between features and the target ($y = \beta_0 + \sum \beta_i X_i$). It cannot easily model complex non-linear feature interactions without manual polynomial terms.
- *Decision Trees* split feature space hierarchically into orthogonal regions, capable of learning non-linear relationships, but are prone to high variance and overfitting.
- *Random Forest* is an ensemble technique using bagging (Bootstrap Aggregating) where multiple independent decision trees are trained on random subsets of data and features, and their outputs are averaged to reduce variance.
- *Gradient Boosting* builds trees sequentially, where each subsequent tree corrects the residual errors made by the previous trees, resulting in the highest predictive accuracy.

**Q3: What is $R^2$ Score, RMSE, and MAE?**  
**Answer:**
- **$R^2$ Score (Coefficient of Determination):** Measures the proportion of variance in the target variable explained by the model ($R^2 = 1 - \frac{SS_{res}}{SS_{tot}}$). An $R^2$ of 0.9755 means our model explains 97.55% of the price variance.
- **MAE (Mean Absolute Error):** The average magnitude of errors without direction ($\frac{1}{n}\sum |y_i - \hat{y}_i|$).
- **RMSE (Root Mean Squared Error):** The square root of the average squared errors ($\sqrt{\frac{1}{n}\sum (y_i - \hat{y}_i)^2}$). It penalizes large errors more heavily than MAE.

**Q4: What is One-Hot Encoding and why did you use it?**  
**Answer:** Machine learning models require numerical inputs. Categorical variables like `location` have no natural ordinal hierarchy. One-Hot Encoding transforms each categorical location into a binary column (0 or 1), preventing the model from assuming false numerical order (e.g. assuming Location 3 is greater than Location 1).

---

### B. Java & Spring Boot Questions

**Q5: What is Spring Boot and why did you use it instead of traditional Spring MVC?**  
**Answer:** Spring Boot provides an opinionated, production-ready framework that eliminates boilerplate XML configuration through auto-configuration, starter dependencies, and embedded servers (Tomcat), enabling rapid development of microservices and RESTful backends.

**Q6: What is Dependency Injection (DI) and Inversion of Control (IoC)?**  
**Answer:** IoC is a design principle where the control of object creation and lifecycle is transferred from the application code to the Spring container. Dependency Injection is the mechanism used by Spring to inject required dependencies (e.g., `@Autowired HousePredictionRepository` into `HousePredictionService`) via constructor or field injection, promoting loose coupling and testability.

**Q7: How does Spring Data JPA work?**  
**Answer:** Spring Data JPA provides a high-level abstraction over Hibernate and JDBC. By extending `JpaRepository<HousePrediction, Long>`, Spring automatically implements standard CRUD operations (`save`, `findAll`, `findById`, `deleteById`) and custom `@Query` methods at runtime without writing raw SQL.

---

### C. Full-Stack Integration Questions

**Q8: How does Java communicate with Python in your architecture?**  
**Answer:** Through HTTP REST API calls. The Python ML inference engine runs as a lightweight Flask microservice on port 5001. The Java Spring Boot backend uses `RestTemplate` to make an HTTP `POST` request with a JSON payload containing property attributes. Python receives the JSON, passes it through the deserialized ML pipeline (`house_price_model.joblib`), and returns a JSON response containing `predictedPrice`.

**Q9: How does the Frontend communicate with the Java Backend?**  
**Answer:** The modern web frontend uses the asynchronous JavaScript `fetch()` API to make non-blocking HTTP requests (`POST /api/predict`, `GET /api/predictions`, `DELETE /api/predictions/{id}`) to the Spring Boot REST controller on port 8080. When the promise resolves, JavaScript dynamically updates the DOM elements (result cards, stats, and history table) without full page reloads.

**Q10: How does the system handle errors and service unavailability?**  
**Answer:** We implemented a `GlobalExceptionHandler` with `@RestControllerAdvice` in Spring Boot. If the Python ML service is down or unreachable, `RestTemplate` throws a `RestClientException`, which is caught and mapped to a custom `MlServiceException` returning a user-friendly `HTTP 503 Service Unavailable` response instead of crashing the server.
