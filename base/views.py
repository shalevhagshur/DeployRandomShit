from datetime import timezone
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from base.models import Product,Categories
from .Serializer import ProductSerializer,CategoriesSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status
from .models import Orders 
from .Serializer import OrdersSerializer
from rest_framework.views import APIView



class CreateOrderView(APIView):
    def post(self, request, format=None):
        data = request.data  # The JSON data

        try:
            for item in data:
                serializer = OrdersSerializer(data=item)
                if serializer.is_valid():
                    serializer.save(username=request.user)  # Set the username based on the logged-in user
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return Response("Orders created successfully", status=status.HTTP_201_CREATED)


def index(req):
    return Response('hello', safe=False)

def myCategories(req):
    all_categories = CategoriesSerializer(Categories.objects.all(), many=True).data
    return Response(all_categories)


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)  # Serialize the data
    return render(request, '/Front/index.html', {'products': serializer.data})


@api_view(['POST'])
def register(req):
    user= User.objects.create_user(
         username=req.data['username'],
         email=req.data['email'],
         password=req.data['password']
    )
    user.is_active = True
    user.is_staff = False
    user.save()
    return Response("new user registered")     

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
	return Response("im protected")





from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return render(request, '/Front/login.html')  # Render the login template

    return Response("Invalid credentials", status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
#@permission_classes([IsAuthenticated])
def create_order(request):
    cart = request.data  # Assuming you pass the cart data in the request

    # Calculate the total price of the products in the cart
    total_price = sum(item['price'] * item['amount'] for item in cart)

    # Create a new order
    order = Orders.objects.create(amount=len(cart), total=total_price, orderdate=timezone.now())

    # Add products to the order
    for item in cart:
        product = Product.objects.get(id=item['id'])
        quantity = item['amount']
        price = item['price']
        image = product.image.url  # Assuming your Orders model has an 'image' field
        category = product.category  # Assuming your Orders model has a 'category' field

        Orders.objects.create(order=order, product=product, amount=quantity, price=price, image=image, category=category)

    return Response("Purchase successful", status=status.HTTP_201_CREATED)

@api_view(['GET'])
def user_info(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        user = request.user
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            # Add more fields as needed
        }
        return JsonResponse(user_info)
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)