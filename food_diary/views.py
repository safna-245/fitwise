from django.shortcuts import render,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions

from food_diary.serializers import UserSerializer,FoodlogSerializer
from food_diary.models import Foodlog
from food_diary.permissions import IsOwner
from food_diary.ai_service import get_diet_plan

from datetime import datetime
# Create your views here.
class SignUpView(APIView):

    def post(self,request):

        form_data = request.data

        serializer_instance = UserSerializer(data=form_data)

        if serializer_instance.is_valid():

            cleaned_data = serializer_instance._validated_data

            instance = User.objects.create_user(**cleaned_data)

            serializer_instance = UserSerializer(instance)

            return Response(data=serializer_instance.data)

        else:

            return Response(data=serializer_instance.errors)

class GetMeView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        auth_user = request.user

        instance = User.objects.get(username=auth_user)

        serializer_instance = UserSerializer(instance)

        return Response(data=serializer_instance.data)

class FoodlogListCreateView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):

        instance = Foodlog.objects.filter(owner=request.user)

        serializer_instance = FoodlogSerializer(instance,many=True)

        return Response(data=serializer_instance.data)

    def post(self,request):

        form_data = request.data

        serializer_instance = FoodlogSerializer(data=form_data)

        if serializer_instance.is_valid():

            serializer_instance.save(owner=request.user)

            return Response(data=serializer_instance.data)
        
        else:

            return Response(data=serializer_instance.errors)

class FoodlogRetrieveUpdateDeleteView(APIView):

        authentication_classes = [authentication.TokenAuthentication]
    
        # permission_classes = [permissions.IsAuthenticated]

        permission_classes = [IsOwner]
        
        def get(self,request,pk=None):

            instance = get_object_or_404(Foodlog,id=pk)

            self.check_object_permissions(request,instance)

            serializer_instance = FoodlogSerializer(instance)

            return Response(data=serializer_instance.data)

        def put(self,request,pk=None):

            instance = get_object_or_404(Foodlog,id=pk)

            self.check_object_permissions(request,instance)
            
            form_data = request.data
    
            serializer_instance = FoodlogSerializer(data=form_data,instance=instance)
    
            if serializer_instance.is_valid():
    
                serializer_instance.save()
    
                return Response(data=serializer_instance.data)
            
            else:
    
                return Response(data=serializer_instance.errors)

        def delete(self,request,pk=None):

            instance = get_object_or_404(Foodlog,id=pk)

            self.check_object_permissions(request,instance)
            
            instance.delete()

            return Response({"message":"deleted.."})

class FoodlogSummaryView(APIView):

    authentication_classes = [authentication.TokenAuthentication]

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        response_data={
            "total_calorie":0
        }

        cur_date = datetime.now().date()

        cur_month = datetime.now().month

        cur_year = datetime.now().year
        #monthly calorie

        monthly_calorie = Foodlog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year = cur_year)

        if monthly_calorie:

            monthly_total = monthly_calorie.values("calorie").aggregate(total=Sum("calorie")).get("total")

            response_data["monthly_calorie"] = monthly_total
        
        #today calorie
        today_calorie = Foodlog.objects.filter(owner=request.user,created_at__date=cur_date)

        if today_calorie:

            total_calorie = today_calorie.values("calorie").aggregate(total=Sum("calorie")).get("total")

            meal_type__summary = today_calorie.values("meal_type").annotate(total=Sum("calorie"))

            response_data["total_calorie"]=total_calorie

            response_data["category_summary"] = meal_type__summary

        return Response(data=response_data)

class DietPlanView(APIView):

       authentication_classes =[authentication.TokenAuthentication]

       permission_classes = [permissions.IsAuthenticated]

       def get(Self,request):

           response_data = {
               "monthly_total_calorie":0
           }

           cur_month = datetime.now().month

           cur_year = datetime.now().year

           monthly_calorie = Foodlog.objects.filter(owner=request.user,created_at__month=cur_month,created_at__year = cur_year)

           if monthly_calorie:

               monthly_total_calorie = monthly_calorie.values("calorie").aggregate(total=Sum("calorie")).get("total")

               response_data["monthly_total_calorie"]=monthly_total_calorie

               meal_type_summary = monthly_calorie.values("meal_type").annotate(total=Sum("calorie"))

               response_data["meal_type_summary"] = meal_type_summary

               diet_plan = get_diet_plan(response_data)

               response_data["plan"] = diet_plan

           return Response(data=response_data)









    





        
