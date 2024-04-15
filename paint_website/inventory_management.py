# predictions.py

from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import pandas as pd
from .models import Our_Product, AllOrderDetail

def preprocess_data():
    # Retrieve order data
    orders = AllOrderDetail.objects.all()

    # Create dataframe
    data = []
    for order in orders:
        data.append({
            'product_name': order.product.product_name,
            'quantity': order.quantity
        })
    df = pd.DataFrame(data)

    # Aggregate data by product
    product_quantities = df.groupby('product_name').sum().reset_index()

    return product_quantities

def predict_high_demand_products():
    # Preprocess data
    product_quantities = preprocess_data()

    # Split data into features and target
    X = product_quantities[['product_name']]
    y = product_quantities['quantity']

    # Transform product names to numerical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('product_name', CountVectorizer(), ['product_name'])
        ]
    )

    # Define regression model
    model = make_pipeline(preprocessor, LinearRegression())

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    model.fit(X_train, y_train)

    # Predict quantities for test data
    y_pred = model.predict(X_test)

    # Calculate MSE
    mse = mean_squared_error(y_test, y_pred)

    # Combine product names and predicted quantities
    predicted_products = pd.DataFrame({'product_name': X_test['product_name'], 'predicted_quantity': y_pred})

    # Sort products by predicted quantities
    sorted_products = predicted_products.sort_values(by='predicted_quantity', ascending=False)

    return sorted_products, mse
