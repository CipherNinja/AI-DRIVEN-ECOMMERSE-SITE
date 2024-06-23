# prediction.py
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np
from .models import AllOrderDetail, ShoppingCart, Our_Product

def predict_products(user_id):
   
    order_history = AllOrderDetail.objects.filter(user=user_id)
    cart_items = ShoppingCart.objects.filter(user=user_id)
    
    # Preprocess data
    ordered_products = []
    for order in order_history:
        ordered_products.append(order.product.product_name)
    cart_products = []
    for cart in cart_items:
        cart_products.append(cart.product.product_name)
    
    all_products = Our_Product.objects.values_list('product_name', flat=True)
    product_names = ordered_products + cart_products
    y = np.array([1] * len(ordered_products) + [0] * len(cart_products))
    
    
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(product_names)
    
    
    model = MultinomialNB()
    model.fit(X, y)
    
   
    all_product_names = vectorizer.transform(all_products)
    predictions = model.predict(all_product_names)
    
    
    recommended_products = []
    for i, product_name in enumerate(all_products):
        if predictions[i] == 1:
            recommended_products.append(product_name)
    
    return recommended_products
