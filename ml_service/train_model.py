import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def run_ml_pipeline():
    print("=" * 70)
    print("AI-BASED HOUSE PRICE PREDICTION - MACHINE LEARNING PIPELINE")
    print("=" * 70)

    # 1. Load Dataset
    data_path = os.path.join('dataset', 'house_data.csv')
    df = pd.read_csv(data_path)
    print(f"\n[STEP 1] Dataset Loaded Successfully from '{data_path}'")
    print(f"Total Records: {df.shape[0]} | Total Features: {df.shape[1]}")
    
    # 2. Understand Dataset
    print("\n--- First 5 Records ---")
    print(df.head())
    print("\n--- Dataset Info ---")
    print(df.info())
    print("\n--- Statistical Summary ---")
    print(df.describe())

    # 3. Missing Values & Duplicates
    print("\n[STEP 2] Data Quality Check:")
    print("Missing values per column:\n", df.isnull().sum())
    print(f"Duplicate rows count: {df.duplicated().sum()}")

    # 4. Exploratory Data Analysis (EDA)
    os.makedirs('ml_service/eda_plots', exist_ok=True)
    
    plt.figure(figsize=(10, 6))
    sns.histplot(df['price'] / 100000, kde=True, color='royalblue', bins=30)
    plt.title('House Price Distribution (in Lakhs INR)', fontsize=14, fontweight='bold')
    plt.xlabel('Price (₹ in Lakhs)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.tight_layout()
    plt.savefig('ml_service/eda_plots/price_distribution.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    sns.boxplot(x='location', y=df['price'] / 100000, data=df, palette='Set2')
    plt.title('House Price by Location (in Lakhs INR)', fontsize=14, fontweight='bold')
    plt.xlabel('Location', fontsize=12)
    plt.ylabel('Price (₹ in Lakhs)', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('ml_service/eda_plots/location_vs_price.png')
    plt.close()

    numeric_cols = ['area', 'bedrooms', 'bathrooms', 'parking', 'property_age', 'floors', 'price']
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='Blues', fmt='.2f', linewidths=1)
    plt.title('Correlation Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('ml_service/eda_plots/correlation_matrix.png')
    plt.close()
    print("\n[STEP 3] EDA plots generated and saved to 'ml_service/eda_plots/'.")

    # 5. Define Features & Target
    X = df.drop(columns=['price'])
    y = df['price']

    categorical_features = ['location']
    numerical_features = ['area', 'bedrooms', 'bathrooms', 'parking', 'property_age', 'floors']

    # 6. Train-Test Split (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
    print(f"\n[STEP 4] Dataset Split: {len(X_train)} Training samples, {len(X_test)} Testing samples.")

    # 7. Preprocessing Pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features),
            ('num', StandardScaler(), numerical_features)
        ]
    )

    # 8. Train Multiple Regression Models
    models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(alpha=1.0),
        'Decision Tree': DecisionTreeRegressor(random_state=42, max_depth=12),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=15),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, learning_rate=0.1)
    }

    results = []
    trained_pipelines = {}

    print("\n[STEP 5] Training & Evaluating Regression Models...")
    print("-" * 80)
    print(f"{'Model':<22} | {'MAE (INR)':<15} | {'RMSE (INR)':<15} | {'R2 Score':<10}")
    print("-" * 80)

    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', model)
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        results.append({
            'Model': name,
            'MAE': mae,
            'RMSE': rmse,
            'MSE': mse,
            'R2': r2
        })
        trained_pipelines[name] = pipeline
        
        print(f"{name:<22} | Rs. {mae:>11,.2f} | Rs. {rmse:>11,.2f} | {r2:>8.4f}")
    
    print("-" * 80)

    # 9. Select the Best Model (highest R2 Score)
    results_df = pd.DataFrame(results).sort_values(by='R2', ascending=False)
    best_model_name = results_df.iloc[0]['Model']
    best_pipeline = trained_pipelines[best_model_name]
    best_r2 = results_df.iloc[0]['R2']
    best_rmse = results_df.iloc[0]['RMSE']
    best_mae = results_df.iloc[0]['MAE']

    print(f"\n[STEP 6] Best Model Selected: {best_model_name}")
    print(f"R2 Score: {best_r2:.4f} | RMSE: Rs. {best_rmse:,.2f} | MAE: Rs. {best_mae:,.2f}")

    # 10. Save the Trained Model & Artifacts
    os.makedirs('ml_service/model', exist_ok=True)
    model_save_path = os.path.join('ml_service', 'model', 'house_price_model.joblib')
    joblib.dump(best_pipeline, model_save_path)
    print(f"\n[STEP 7] Complete Pipeline saved to '{model_save_path}'")

    # Save unique locations for frontend dropdowns & validation
    locations_list = sorted(list(df['location'].unique()))
    with open(os.path.join('ml_service', 'locations.json'), 'w') as f:
        json.dump(locations_list, f, indent=2)
    print(f"Locations list ({len(locations_list)} locations) saved to 'ml_service/locations.json'")

    # Save metrics summary to JSON for backend/analytics verification
    metrics_summary = {
        'best_model': best_model_name,
        'r2_score': round(float(best_r2), 4),
        'rmse': round(float(best_rmse), 2),
        'mae': round(float(best_mae), 2),
        'all_models': results
    }
    with open(os.path.join('ml_service', 'metrics_summary.json'), 'w') as f:
        json.dump(metrics_summary, f, indent=2)

    # Test sample inference
    sample_house = pd.DataFrame([{
        'location': 'Madhurawada',
        'area': 1500.0,
        'bedrooms': 3,
        'bathrooms': 2,
        'parking': 1,
        'property_age': 5,
        'floors': 2
    }])
    sample_pred = best_pipeline.predict(sample_house)[0]
    print("\n--- Test Verification Prediction ---")
    print(f"Input: Madhurawada, 1500 sqft, 3 BHK, 2 Baths, 1 Parking, 5 yrs age, 2 Floors")
    print(f"Predicted Fair Market Price: Rs. {sample_pred:,.2f} (approx Rs. {sample_pred/100000:.2f} Lakhs)")
    print("=" * 70)

if __name__ == '__main__':
    run_ml_pipeline()
