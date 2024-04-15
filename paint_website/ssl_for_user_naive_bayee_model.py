import psutil
import platform

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from .models import AllOrderDetail, ShoppingCart, Our_Product

def get_cpu_usage():
    return psutil.cpu_percent()

def get_memory_usage():
    return psutil.virtual_memory().percent

def get_system_info():
    return platform.system(), platform.release()

def preprocess_data(user_id):
    order_history = AllOrderDetail.objects.filter(user_id=user_id)
    cart_items = ShoppingCart.objects.filter(user_id=user_id)
    
    # Preprocess data
    ordered_products = [order.product.product_name for order in order_history]
    cart_products = [cart.product.product_name for cart in cart_items]
    
    return ordered_products, cart_products

def predict_product(user_id):
    
    ordered_products, cart_products = preprocess_data(user_id)
    
    product_names = ordered_products + cart_products
    
    if not product_names:
        return [], 0
    
    all_products = Our_Product.objects.values_list('product_name', flat=True)
    

    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(product_names)
    
    model = MultinomialNB()
    model.fit(X, [1] * len(ordered_products) + [0] * len(cart_products))
    
    all_product_names = vectorizer.transform(all_products)
    predictions = model.predict(all_product_names)
    
    recommended_products = [product_name for product_name, prediction in zip(all_products, predictions) if prediction == 1]
    
    data_loss = int((1 - len(recommended_products) / len(all_products)) * 100)
    
    
    print("Matrix Format:")
    print("              ", end="")
    for product_name in all_products:
        print("{:<10}".format(product_name), end="")
    print()
    for i, prediction in enumerate(predictions):
        print("User {}: ".format(user_id), end="")
        for j, product_name in enumerate(all_products):
            if prediction == 1:
                print("{:<10}".format("1"), end="")
            else:
                print("{:<10}".format("0"), end="")
        print()
    
    print("Data Loss: {}%".format(data_loss))
    
    # Computer speed status
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    system_info = get_system_info()
    
    print("\nComputer Speed Status:")
    print("CPU Usage: {}%".format(cpu_usage))
    print("Memory Usage: {}%".format(memory_usage))
    print("System Info: {}".format(system_info))
    
    return recommended_products, data_loss

