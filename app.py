# app.py

import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Load and prepare model + encoders
@st.cache_resource
def load_model():
    model = pickle.load(open("model.pkl", "rb"))
    encoders = pickle.load(open("encoders.pkl", "rb"))
    return model, encoders

model, encoders = load_model()

st.title("🚗 Car Price Predictor")
st.write("Enter the details of the car below:")

# Form for input
brand = st.selectbox("Brand", encoders['brand'].classes_)
model_input = st.selectbox("Model", encoders['model'].classes_)
vehicle_age = st.number_input("Vehicle Age (years)", 0.0, 50.0)
km_driven = st.number_input("Kilometers Driven", 0, 1000000)
seller_type = st.selectbox("Seller Type", encoders['seller_type'].classes_)
fuel_type = st.selectbox("Fuel Type", encoders['fuel_type'].classes_)
transmission = st.selectbox("Transmission Type", encoders['transmission_type'].classes_)
mileage = st.number_input("Mileage (km/l)", 0.0, 100.0)
engine = st.number_input("Engine (cc)", 0.0, 10000.0)
max_power = st.number_input("Max Power (BHP)", 0.0, 1000.0)
seats = st.number_input("Seats", 1, 10)

if st.button("Predict Price"):
    # Encode the input
    input_df = pd.DataFrame([{
        'brand': encoders['brand'].transform([brand])[0],
        'model': encoders['model'].transform([model_input])[0],
        'vehicle_age': vehicle_age,
        'km_driven': km_driven,
        'seller_type': encoders['seller_type'].transform([seller_type])[0],
        'fuel_type': encoders['fuel_type'].transform([fuel_type])[0],
        'transmission_type': encoders['transmission_type'].transform([transmission])[0],
        'mileage': mileage,
        'engine': engine,
        'max_power': max_power,
        'seats': seats
    }])

    predicted_price = model.predict(input_df)[0]
    st.success(f"💰 Predicted Price: ₹ {round(predicted_price, 2)}")
