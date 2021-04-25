from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import *
from .models import *
from rest_framework import permissions
from rest_framework.generics import DestroyAPIView
from .permissions import IsAdmin
from rest_framework import viewsets



class UsersListView(APIView):
    serializer_class = UserSerializer
    def post(self,request,*args,**wkargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)



    def get_queryset(self):
        users = User.objects.all()
        return users

class ObtainAuthTokenView(ObtainAuthToken):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token = Token.objects.get(user=user)
        return Response({
            'token':token.key
        })

class CategoryView(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductsView(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class OrderItemView(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()

class OrderAdminView(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
 

class ProductListView(APIView):
    serializer_class = ProductSerializer
    
    def get(self,request,*args,**kwargs):
        
        serializer = self.serializer_class(Product.objects.all(),many=True)
        return Response(serializer.data)
class ProductDetailView(APIView):
    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            try:
                product =Product.objects.get(id=pk)
                serializer = ProductSerializer(product,many=False)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response("product not found",status=status.HTTP_400_BAD_REQUEST)
        

class CategoryListView(APIView):
    serializer_class = CategorySerializer
    
    def get(self,request,*args,**kwargs):
        
        serializer = self.serializer_class(Category.objects.all(),many=True)
        return Response(serializer.data)
class CategoryDetailView(APIView):
    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            try:
                product =Category.objects.get(id=pk)
                serializer = ProductSerializer(product,many=False)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response("product not found",status=status.HTTP_400_BAD_REQUEST)


class OrderListView(APIView):
    serializer_class = OrderSerializer
    
    def get(self,request,*args,**kwargs):
        
        serializer = self.serializer_class(Order.objects.all(),many=True)
        return Response(serializer.data)
class OrderDetailView(APIView):
    def get(self,request,*args,**kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            try:
                product =Order.objects.get(id=pk)
                serializer = ProductSerializer(product,many=False)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response("product not found",status=status.HTTP_400_BAD_REQUEST)

class OrderCreateView(APIView):
    
    def post(self,request,*args,**kwargs):
        data = request.data
        new_order = Order.objects.create(country=data["country"])
        new_order.total = data["total"]
        new_order.adress = data["address"]
        new_order.phone_number = data["phone_number"]
        new_order.total = data["total"]
        new_order.email = data["email"]
      
        for i in data["items"]:
            item = Product.objects.get(id=i)
            new_order.items.add(item)
        new_order.save()

        serializer= OrderSerializer(new_order)
       
        return Response(serializer.data)
        
     
        
class GetUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(request,*args,**kwargs):
        user = request.user
        return Response({
            "id":user.id,
            "username":user.username
        })