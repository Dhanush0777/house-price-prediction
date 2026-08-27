import os
import json
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'house_price_model.joblib')
LOCATIONS_PATH = os.path.join(BASE_DIR, 'locations.json')
METRICS_PATH = os.path.join(BASE_DIR, 'metrics_summary.json')

# Load Model Pipeline & Metadata
print(f"[*] Loading trained model pipeline from {MODEL_PATH}...")
model_pipeline = joblib.load(MODEL_PATH)
print("[+] Model loaded successfully into memory.")

valid_locations = []
if os.path.exists(LOCATIONS_PATH):
    with open(LOCATIONS_PATH, 'r') as f:
        valid_locations = json.load(f)

metrics_data = {}
if os.path.exists(METRICS_PATH):
    with open(METRICS_PATH, 'r') as f:
        metrics_data = json.load(f)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'UP',
        'service': 'Python ML House Price Inference Service',
        'model_loaded': model_pipeline is not None,
        'locations_count': len(valid_locations)
    }), 200

@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify({
        'status': 'success',
        'locations': valid_locations
    }), 200

@app.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify({
        'status': 'success',
        'metrics': metrics_data
    }), 200

@app.route('/predict', methods=['POST'])
def predict_price():
    try:
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({'status': 'error', 'message': 'No JSON payload provided'}), 400

        # Extract values with flexible key mappings
        location = data.get('location') or data.get('Location') or 'Madhurawada'
        area = data.get('area') or data.get('Area') or data.get('sqft') or data.get('squareFeet')
        bedrooms = data.get('bedrooms') or data.get('Bedrooms') or data.get('beds') or data.get('bhk')
        bathrooms = data.get('bathrooms') or data.get('Bathrooms') or data.get('baths')
        parking = data.get('parking') if data.get('parking') is not None else data.get('Parking', 1)
        property_age = data.get('propertyAge') if data.get('propertyAge') is not None else data.get('property_age', data.get('age', 5))
        floors = data.get('floors') if data.get('floors') is not None else data.get('Floors', 1)

        # Validation
        if area is None or bedrooms is None or bathrooms is None:
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields: area, bedrooms, and bathrooms are mandatory.'
            }), 400

        try:
            area = float(area)
            bedrooms = int(bedrooms)
            bathrooms = int(bathrooms)
            parking = int(parking)
            property_age = int(property_age)
            floors = int(floors)
        except (ValueError, TypeError):
            return jsonify({
                'status': 'error',
                'message': 'Invalid numeric types provided in request parameters.'
            }), 400

        if area <= 0 or bedrooms <= 0 or bathrooms <= 0 or property_age < 0 or floors <= 0:
            return jsonify({
                'status': 'error',
                'message': 'Property parameters must be positive numbers.'
            }), 400

        # Construct input DataFrame for inference pipeline
        input_df = pd.DataFrame([{
            'location': str(location).strip(),
            'area': area,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'parking': parking,
            'property_age': property_age,
            'floors': floors
        }])

        # Perform inference
        prediction_val = model_pipeline.predict(input_df)[0]
        # Floor at reasonable positive price
        predicted_price = max(500000.0, float(round(prediction_val, 2)))

        return jsonify({
            'status': 'success',
            'predictedPrice': predicted_price,
            'currency': 'INR',
            'modelUsed': metrics_data.get('best_model', 'Gradient Boosting Regressor'),
            'inputs': {
                'location': location,
                'area': area,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'parking': parking,
                'propertyAge': property_age,
                'floors': floors
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'ML Inference failed: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"[*] Starting Flask ML Prediction Microservice on http://localhost:{port} ...")
    app.run(host='0.0.0.0', port=port, debug=False)
