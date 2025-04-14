import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Enable CORS for all routes

# Load the trained model
with open('car_price_model.pkl', 'rb') as file:
    model = pickle.load(file)

# API endpoint for predictions
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Create a DataFrame with a single row
        input_df = pd.DataFrame([data])
        
        # Ensure all numeric columns are properly typed
        numeric_columns = ['vehicle_age', 'km_driven', 'mileage', 'engine', 'max_power', 'seats']
        for col in numeric_columns:
            input_df[col] = pd.to_numeric(input_df[col])
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        
        # Return predicted price
        return jsonify({'predicted_price': float(prediction)})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Serve the HTML page
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)