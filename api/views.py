from django.shortcuts import render
from .models import Tasks
from .serializers import TaskSerializers
from rest_framework import mixins,generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from .tasks import send_email_task
from rest_framework import status
# Create your views here.


class TaskView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):

    serializer_class=TaskSerializers
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication
]


    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tasks.objects.all()
        if self.request.user.is_authenticated:
            return Tasks.objects.filter(user=self.request.user)
        return Tasks.objects.none()
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get(self,request):
        return self.list(request)
    def post(self,request):
       serializer=TaskSerializers(data=request.data)
       if serializer.is_valid():
           serializer.save(user=self.request.user)
           return Response({'message':'Task added successfully!'})
       return Response(serializer.errors)
       
        
    
class TaskDetailView(mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.UpdateModelMixin,generics.GenericAPIView):
    serializer_class=TaskSerializers
    queryset=Tasks.objects.all()
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication
]

    
    def get(self,request,pk):
        return self.retrieve(request,pk)
    def put(self,request,pk):
        return self.update(request,pk,partial=True)
    def delete(self,request,pk):
        return self.destroy(request,pk)    
    
class RegisterationView(APIView):
    def get(self,request):
        return Response({'message':'please register here '})
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User created successfully!'})    
        
class LoginView(APIView):
    def get(self,request):
        return Response({'message':'please login here'})
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)   
        if user :
            refresh=RefreshToken.for_user(user)     
            return Response({'refresh':str(refresh),'access':str(refresh.access_token),'message':'user logged in successfully'})
        return Response({'message':'Invalid credentials'},status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):    
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self,request):
        try:
         refresh_token=request.data.get('refresh')
         if refresh_token:
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'Logout successfully!'})
        except Exception as e:
         return Response({'message':'Something went wrong!'})
    
class ForgetView(APIView):
    def post(self,request):
        email=request.data.get('email')
        try:
            user=User.objects.get(email=email)
            if user is not None:
                uid=urlsafe_base64_encode(force_bytes(user.pk))    
                token=default_token_generator.make_token(user)
                link=f'http://127.0.0.1:8000/reset/{uid}/{token}/'
                send_email_task.delay(
                    'link to reset your password',
                    f'click this link to reset your pass:{link}',
                    user.email
                )
                return Response({'message':'reset link sent successfully!'})
        except Exception as e:
            return Response({'message':'Something went wrong'})     

        
