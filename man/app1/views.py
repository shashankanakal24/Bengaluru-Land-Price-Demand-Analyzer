from django.shortcuts import render ,redirect 
import pandas as pd
from django.http import JsonResponse
import pickle
import numpy as np
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Location, Prediction
from django.db.models import Count

# Load the data and model
data = pd.read_csv('E:/Mini Project/man/cleaned data/Cleaned_data.csv')
pipe = pickle.load(open("E:/Mini Project/man/RidgeModel.pkl", "rb"))

def prediction(request):
    locations = sorted(data['location'].unique())
    return render(request, 'prediction.html', {'locations': locations})


def landingpage(request):
    return render(request ,'index.html')

def aboutus(request):
    return render(request, 'aboutus.html')


def predict(request):
    if request.method == 'POST':
        location_name = request.POST.get('location')
        bhk = request.POST.get('bhk')
        bath = request.POST.get('bath')
        sqft = request.POST.get('total_sqft')
        
        # Ensure location exists in the database
        location, created = Location.objects.get_or_create(name=location_name)
        
        # Prepare data for prediction
        input_data = pd.DataFrame([[location.name, sqft, bath, bhk]], columns=['location', 'total_sqft', 'bath', 'bhk'])
        prediction_value = pipe.predict(input_data)[0] * 1e5
        
        # Save the prediction data to the database
        prediction = Prediction(
            location=location_name,
            bhk=bhk,
            bath=bath,
            sqft=sqft,
            prediction=np.round(prediction_value, 2)
        )
        prediction.save()
        
        # Return the prediction as a response
        return HttpResponse(str(np.round(prediction_value, 2))) 

def loginorsignup(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'signup':
            # Handle Sign Up
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            if User.objects.filter(username=name).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                user = User.objects.create_user(username=name, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('loginorsignup')
            
        elif form_type == 'login':
            # Handle Login
            email = request.POST.get('email')
            password = request.POST.get('password')
            # print(f"Attempting to authenticate user with email: {email} and password: {password}") 
            user = authenticate(request, username=email, password=password)  # Correct if username is email
            # print(f"Authentication result: {user}") 
            if user is not None:
                auth_login(request, user)
                return redirect('home')  # Redirect to home page on successful login
            else:
                messages.error(request, 'Invalid credentials.')
                
    return render(request, 'loginorsignup.html')

def home(request):
    return render(request, 'home.html')

def Analysis(request):
    # Query the Prediction model to get the count of predictions per location
    location_counts = Prediction.objects.values('location').annotate(count=Count('location')).order_by('-count')
    
    # Prepare data for the graph
    locations = [entry['location'] for entry in location_counts]
    counts = [entry['count'] for entry in location_counts]
    
    return render(request, 'Analysis.html', {
        'locations': locations,
        'counts': counts,
    })
    
    


  







