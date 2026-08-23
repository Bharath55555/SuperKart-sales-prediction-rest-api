import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Product Sales Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for product features
Product_Weight = st.number_input("Product_Weight", min_value=0.0, max_value=40.0, step=0.1, value=10.0)
Product_Sugar_Content = st.selectbox("Product_Sugar_Content", ["Low Sugar", "Medium Sugar", "High Sugar"])
Product_Allocated_Area = st.number_input("Product_Allocated_Area", min_value=0.0, max_value=10.0, step=0.01, value=0.5)
Product_MRP  = st.number_input("Product_MRP", min_value=0.0, max_value=1000.0, step=0.1, value=100.0)
Store_Size = st.selectbox("Store_Size", ["Small", "Medium", "High"])
Store_Location_City_Type = st.selectbox("Store_Location_City_Type",["Tier 1", "Tier 2", "Tier 3"])
Store_Type = st.selectbox("Store_Type",["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"])
Store_Age = st.number_input("Store_Age", min_value=0, step=1, value=10)
Product_Id_char = st.selectbox("Product_Id_char", ["FD", "DR", "NC"])
Product_Type_Category = st.selectbox("Product_Type_Category", ["Perishables", "Non Perishables"])

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
        'Product_Weight': product_data['Product_Weight'],
        'Product_Sugar_Content': product_data['Product_Sugar_Content'],
        'Product_Allocated_Area': product_data['Product_Allocated_Area'],
        'Product_MRP': product_data['Product_MRP'],
        'Store_Size': product_data['Store_Size'],
        'Store_Location_City_Type': product_data['Store_Location_City_Type'],
        'Store_Type': product_data['Store_Type'],
        'Store_Age': product_data['Store_Age'],
        'Product_Id_char': product_data['Product_Id_char'],
        'Product_Type_Category': product_data['Product_Type_Category']
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/sales", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Product Sales (in dollars)']
        st.success(f"Predicted Product Sales (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/salesbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
