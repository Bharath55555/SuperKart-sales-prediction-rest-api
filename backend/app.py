
# Import necessary libraries
import joblib
import pandas as pd
from flask import Flask, request, jsonify


# Initialize the Flask application
product_sales_predictor_api = Flask("SuperKart Product Sales Prediction")


# Load the trained machine learning model
model = joblib.load("deployment_files/superkart_model.joblib")


# Home route
@product_sales_predictor_api.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to the SuperKart Product Sales Prediction API!"
    })


# Single Prediction Endpoint
@product_sales_predictor_api.route("/v1/product", methods=["POST"])
def predict_product_sales():

    # Get JSON data
    product_data = request.get_json()

    # Extract features
    sample = {
        "Product_Weight": product_data["Product_Weight"],
        "Product_Sugar_Content": product_data["Product_Sugar_Content"],
        "Product_Allocated_Area": product_data["Product_Allocated_Area"],
        "Product_MRP": product_data["Product_MRP"],
        "Store_Size": product_data["Store_Size"],
        "Store_Location_City_Type": product_data["Store_Location_City_Type"],
        "Store_Type": product_data["Store_Type"],
        "Product_Id_char": product_data["Product_Id_char"],
        "Store_Age_Years": product_data["Store_Age_Years"],
        "Product_Type_Category": product_data["Product_Type_Category"]
    }

    # Convert input to DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction
    predicted_sales = model.predict(input_data)[0]

    # Convert prediction to Python float
    predicted_sales = round(float(predicted_sales), 2)

    # Return prediction
    return jsonify({
        "Predicted_Product_Sales": predicted_sales
    })


# Batch Prediction Endpoint
@product_sales_predictor_api.route("/v1/productbatch", methods=["POST"])
def predict_product_sales_batch():

    # Check whether file is provided
    if "file" not in request.files:
        return jsonify({
            "error": "No file uploaded"
        }), 400

    file = request.files["file"]

    # Check whether a file was selected
    if file.filename == "":
        return jsonify({
            "error": "No file selected"
        }), 400

    try:

        # Read CSV
        input_data = pd.read_csv(file)

        # Make predictions
        predicted_sales_batch = model.predict(input_data)

        # Round predictions
        predicted_sales_batch = [
            round(float(sales), 2)
            for sales in predicted_sales_batch
        ]

        # Create output
        output_dict = {
            f"Row_{i}": sales
            for i, sales in enumerate(predicted_sales_batch)
        }

        return jsonify({
            "Predictions": output_dict
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# Run Flask application
if __name__ == "__main__":

    product_sales_predictor_api.run(
        host="0.0.0.0",
        port=7860,
        debug=True
    )
