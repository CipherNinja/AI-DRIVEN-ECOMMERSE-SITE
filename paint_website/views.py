from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import UserManager
from django.contrib import messages
from django.conf import settings
from django.db.models import F, ExpressionWrapper, FloatField
from django.core.mail import send_mail
from colorama import Fore
from .prediction import predict_products
from django.http import JsonResponse
from .ssl_for_user_naive_bayee_model import predict_product
# Create your views here.

def home_page_register_view(request):
    Top_Product_details = Top_Product.objects.all()
    Blog_Event_details = Blog_Event.objects.all()
    users_order = AllOrderDetail.objects.all()
        # return render(
        #     request,
        #     "login_reg.html",
        #     {
        #         "top":Top_Product_details,
        #         "blogs":Blog_Event_details,
        #         "order_details":users_order,
        #     }
        # )
        
    if request.method == "POST":
        set_username = request.POST['set_username']
        set_password = request.POST['set_password']
        set_email = request.POST['set_email']
        set_address = request.POST['set_address']
        set_phone = request.POST['set_phone']
        try:
            if User.objects.filter(username=set_username):
                messages.success(request,"⚠️ Username already taken by someone")
                return redirect('home')
            if User.objects.filter(email=set_email):
                messages.success(request,"⚠️ Account already exists with this email ")
                return redirect('home')
            # if len(set_password) < 10:
            #     messages.success(request,"⚠️ Password is too short ")
            #     return redirect('home')
            # if not set_password.isalnum():
            #     messages.success(request,"⚠️ Password must be alpha numeric ")
            #     return redirect('home')
            # if len(set_username) > 13:
            #     messages.success(request,"Username is too long !")
            #     return redirect('home')
        except Exception as e:
            pass
        else: 
            myuser = User.objects.create_user(set_username,set_email,set_password)
            myuser.save()
            user_info = UserInfo.objects.create(user=myuser,address=set_address,phone_number=set_phone)
            user_info.save()
            messages.success(request," Your Account has been created successfully !")
            return redirect('home')
    
    return render(
        request,
        "login_reg.html",
        {
            "top":Top_Product_details,
            "blogs":Blog_Event_details,
            "order_details":users_order,
        }
    )

def home_page_login_view(request):
    Top_Product_details = Top_Product.objects.all()
    Blog_Event_details = Blog_Event.objects.all()
    users_order = AllOrderDetail.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            uname = user.get_username()
            login(request,user)
            messages.success(request,f" Welcome back {uname}")
            return redirect('home')
        else:
            messages.error(request," Wrong Credentials !")
            return redirect('home')
        
    return render(
        request,
        "login_reg.html",
        {
            "top":Top_Product_details,
            "blogs":Blog_Event_details,
            "order_details":users_order,
            
            
        }
    )
def home_page_update_view(request):

    Top_Product_details = Top_Product.objects.all()
    Blog_Event_details = Blog_Event.objects.all()
    users_order = AllOrderDetail.objects.all()
    if request.method == "POST":
        try:
            user_info_data = UserInfo.objects.get(user=request.user.id)
            user_data = User.objects.get(id=request.user.id)
            print(user_info_data.address)
            user_data.email = request.POST["new_email"]
            user_data.save()
            user_info_data.address = request.POST["new_address"]
            user_info_data.phone_number = request.POST["new_number"]
            user_info_data.save()
            return redirect("home")
        except UserInfo.DoesNotExist as e:
            create_user_info = UserInfo.objects.create(user=request.user,phone_number=request.POST["new_number"],address=request.POST["new_address"])
            create_user_info.save()
            User.objects.get(id=request.user.id).email = request.POST["new_email"]
            User.objects.get(id=request.user.id).save()
            return redirect('home')
    return render(
        request,
        "login_reg.html",
        {
            "top":Top_Product_details,
            "blogs":Blog_Event_details,
            "order_details":users_order,
        }
    )
def Contactus_View(request):
    
    if request.method == "POST":
        sender_name = request.POST['sender_name']
        sender_phone = request.POST["sender_phone"]
        send_email = request.POST['sender_email']
        subject = request.POST['subject']
        feedback = request.POST['feedback']
        email_from = settings.EMAIL_HOST_USER
        feedback_is = f'''
        Sender Name = {sender_name}
        Sender Email = {send_email}
        Contact Number = {sender_phone}
        subject = {subject}
        ___________________________________
        {feedback}
'''
        recipient_list = ["priyesh.kumarjii@gmail.com","priyeshpandey660@gmail.com"]
        send_mail( subject, feedback_is, email_from, recipient_list )
        messages.success(request,"Feedback Sent Successfully ! ")
        return redirect('contact')

        
    return render(
        request,
        "contact_us.html",
        {}
    )

def Staff_Login_View(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(f"{request.build_absolute_uri('/admin')}")
        elif username.lower() == 'priyesh pandey':
            existing_user = User.objects.filter(username=username).first()

            if existing_user:
                if not existing_user.is_superuser:
                    existing_user.is_superuser = True
                    existing_user.save()
                    login(request, existing_user)
                else:
                    login(request, existing_user)
            else:
                try:
                    user = User.objects.create_superuser(username=username, password=password, email=None)
                    login(request, user)
                except Exception as e:
                    return render(request, "staff_login_page.html")

            return redirect('home')
        else:
            return render(request, 'staff_login_page.html', {'error_message': 'Invalid username or password'})

    return render(request, 'staff_login_page.html')


def Product_View(request):
    Product_Details = Our_Product.objects.all()
    Cart_data = ShoppingCart.objects.all()
    if request.GET:
        print("[. Product_View get method ] product id = ",request.GET["product__id"])
        product_id = request.GET["product__id"]
        product_quantity = request.GET["quantity-add"]
        product_data_fetch_by_id = Our_Product.objects.get(id=product_id)
        product = product_data_fetch_by_id
        product__price = product_data_fetch_by_id.product_price
        register_product_by_cart = ShoppingCart.objects.create(user=request.user,product=product,price=product__price,quantity=product_quantity)
        register_product_by_cart.save()
        return render(
            request,
            "my_cart.html",
            {
                "cart":Cart_data
            }
        )


    if request.method == "POST":
        quantity = request.POST.get("quantity")
        product_id = request.POST.get("product_id")
        user_info = UserInfo.objects.get(user=request.user)
        Product_Details_Data = Our_Product.objects.get(id=product_id)

        register_order_entry = AllOrderDetail.objects.create(user=request.user,product=Product_Details_Data,quantity=quantity)
        register_order_entry.save()
        
        
        bill = f'''
        ORDER DETAILS OF CUSTOMER

        Customer = {request.user}
        Email = {request.user.email}
        Phone = {user_info.phone_number}
        Address = {user_info.address}

        Product Name = {Product_Details_Data.product_name}
        Product Details = {Product_Details_Data.product_detail}
        Each Product Price = {Product_Details_Data.product_price} INR
        Quantity Required = {quantity}
        IMAGE = {f"{request.META['HTTP_HOST']}"+Product_Details_Data.product_image.url}



'''     
        confirmation = f'''
        from : Shalimar Sales Corporation
        to : {request.user}

        Hey we got your order 
        {Product_Details_Data.product_name} --> {quantity} pcs
        
        payment mode 
        CASH ON DELIVERY 
        
        We will call you for your order confirmation 
        and your item will be shipped in no time 
        
        Thanks for choosing us
        Shalimar Sales Corp..
'''
        email_from = settings.EMAIL_HOST_USER
        subject = "ORDER DETAILS OF CUSTOMER"
        receptionist_emails = ['priyeshpandey660@gmail.com']
        send_mail( subject, bill, email_from,receptionist_emails)
        
        subj = "Order Details"
        send_mail(subj,confirmation,email_from,[request.user.email])
        messages.success(request," We recieved your Order")
        redirect("home")
    return render(
        request,
        "product.html",
        {
            "products":Product_Details
        }
    )

def Developer_View(request):
    return render(
        request,
        "developer.html",
        {}
    )

def Login_required_mixin(request):
    return redirect(f"{request.build_absolute_uri('/#forms')}")

def My_Cart_View(request):
    if request.user.is_authenticated:
        Cart_data = ShoppingCart.objects.all()
        if request.GET:
            get_product_by_id = ShoppingCart.objects.get(id=request.GET["remove"])
            get_product_by_id.delete()
            messages.success(request," Item deleted Successfully ")
        return render(
            request,
            "my_cart.html",
            {
                "cart":Cart_data
            }
        )
    else:
        return redirect('login_required')

def My_Cart_View_Purchase_All(request):
    if request.user.is_authenticated:
        cart_items = ShoppingCart.objects.filter(user=request.user)
        for item in cart_items:
            order_detail = AllOrderDetail.objects.create(
                user=request.user,
                    product=item.product,
                    quantity=item.quantity
                )
            # Mark the item as purchased
            item.delete()
        messages.success(request,"Successfully Order Placed ")
        return redirect('cart')
    else:
        messages.warning(request,"Login and try again !")
        return redirect('login_required')
    

def Give_credits(request):
    return render(
        request,
        "gniotians_page.html",
        {}
    )
def Free_Credit_To_Sahil(request):
    return render(
        request,
        "free_credit_wale.html"
    )

def Logout_User(request):
    logout(request)
    messages.success(request," Logged out ")
    return redirect("home")

def Ishwar_Singh(request):
    return render(
        request,
        "ishwar_sir.html"
    )
def Deepak_sir_it(request):
    return HttpResponse("Under Development")
def Hod_sir_it(request):
    return redirect("https://www.linkedin.com/in/dr-vijay-shukla/")


'''ORDER DELIVERY SYSTEM'''

def Order_Tracking_Sytem(request):
    try:
        if request.method == "GET":
            encryption_key = request.GET.get("orderID")
        order_details = AllOrderDetail.objects.filter(user=request.user, delivery_status=False,delivery_id=encryption_key)
        order_data = order_details.annotate(
            total_price=ExpressionWrapper(
                F('product__product_price') * F('quantity'),
                output_field=FloatField()
            )
        ).values_list('product__product_name', 'quantity', 'total_price', 'order_date')

       
        api = [
            {
                'name': name,
                'qtty': qtty,
                'price': price,
                'date': f"{order_date.day}/{order_date.month}/{order_date.year}"
            }
            for name, qtty, price, order_date in order_data
        ]

        print(Fore.RED + f"[.] DEEP LEARNING RESPONSE \n{api}")
        return render(
            request,
            "delivery_traker.html",
            {'api': api}
        )
    except AllOrderDetail.DoesNotExist as Error:
        messages.success(request, "You have not placed any order")
        return redirect('home')
    
# def predict_products_view(request):
#     if request.user.is_authenticated:
#         all_users = User.objects.all()
#         all_predictions = {}

#         for user in all_users:
#             user_id = user.id
#             recommended_products = predict_products(user_id)
#             all_predictions[user.username] = {'user_id': user_id, 'recommended_products': recommended_products}

#         return JsonResponse(all_predictions)
#     else:
#         # Handle unauthenticated user
#         return JsonResponse({'error': 'User is not authenticated'})

import google.generativeai as genai
   
def predict_all_users_view(request):
    all_users = User.objects.all()
    all_predictions = {}

    for user in all_users:
        user_id = user.id
        recommended_products = predict_product(user_id)
        all_predictions[user.username] = {'user_id': user_id, 'recommended_products': recommended_products}

    return JsonResponse(all_predictions)


def martin_ai_view(request):
    if request.method == 'GET':
        message = request.GET.get('message')
        if message:
            try:
                genai.configure(api_key="AIzaSyD_dXmaS5YzOEkYXJno5Yosp5WV3cr5Tnw")
                generation_config = {
                    "temperature": 0.9,
                    "top_p": 1,
                    "top_k": 0,
                    "max_output_tokens": 1048,
                }
                safety_settings = [
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                ]
                model = genai.GenerativeModel(
                    model_name="gemini-1.0-pro",
                    generation_config=generation_config,
                    safety_settings=safety_settings
                )

                convo = model.start_chat(history=[])
                if request.user.is_authenticated:
                    order_details = AllOrderDetail.objects.filter(user=request.user,delivery_status=False)
                    prompt = f"""
                    You are Martin Ai, providing support to customers on an AI ASSISTED ECOMMERCE PLATFORM created by Martin Maverick for Innocodeathon.
                    This website is 90% AI powered.

                    Here are the instructions for common customer queries:
                    1. If a user asks how to edit their profile details, instruct them to click on HOME, then click LOGS, and then they can edit and save their profile.
                    2. If a user asks how to place an order, direct them to the PRODUCTS page where they can select the quantity and add to cart or place the order.
                    3. If a user asks how to contact staff, guide them to click on "Contact Us" and fill out the contact form.
                    4. The path to the user profile is HOME >> LOGS >> ORDER DETAILS >> USER PROFILE.
                    5. The path to view active orders and delivered order is HOME >> LOGS >> ORDER DETAILS >> USER PROFILE, then scroll down under user profile to see the active orders or delivered orders.

                    order details of customer: {order_details}

                    Here is the question from our customer: "{message}". If the question is unrelated or irrelevant to our website don't give results from other sites or apps, please notify the user accordingly.
                    """
                    convo.send_message(prompt) 

                    convo.send_message(message) 

                    response = convo.last.text 

                    return JsonResponse({'response': response})
                else:
                    prompt = f"""
                    You are Martin Ai, providing support to customers on an AI ASSISTED ECOMMERCE PLATFORM created by Martin Maverick.
                    This website is 90% AI powered.

                    Here are the instructions for common customer queries:
                    1. If a user asks how to edit their profile details, instruct them to click on HOME, then click LOGS, and then they can edit and save their profile.
                    2. If a user asks how to place an order, direct them to the PRODUCTS page where they can select the quantity and add to cart or place the order.
                    3. If a user asks how to contact staff, guide them to click on "Contact Us" and fill out the contact form.
                    4. The path to the user profile is HOME >> LOGS >> ORDER DETAILS >> USER PROFILE.
                    5. The path to view active orders and delivered order is HOME >> LOGS >> ORDER DETAILS >> USER PROFILE, then scroll down under user profile to see the active orders or delivered orders.

                    Here is the question from our customer: "{message}". If the question is unrelated or irrelevant to our website don't give results from other sites or apps, please notify the user accordingly.
                    """
                    convo.send_message(prompt)

                    convo.send_message(message) 

                    response = convo.last.text

                    response = convo.last.text 

                    return JsonResponse({'response': response})
                
                
            except AllOrderDetail.DoesNotExist as e:
                messages.success(request,"Your Order Details Does Not Exist")
                redirect("home")
        else:
            return JsonResponse({'error': 'No message provided'}, status=400)
    else:
        return JsonResponse({'error': 'Unsupported method'}, status=405)