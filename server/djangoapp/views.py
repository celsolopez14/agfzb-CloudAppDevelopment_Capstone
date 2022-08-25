from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, DealerReview
from .restapis import get_dealers_from_cf, get_dealers_by_state_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_by_id_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)  



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)  


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = 'Invalid username or password'
            return render(request, 'djangoapp/registration.html', context)
    else:
        return render(request, 'djangoapp/registration.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':

        username = request.POST['Username']
        password = request.POST['Password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False

        try:
            User.objects.get(username = username)
            user_exist = True

        except:
            logger.debug("{} is a new user".format(username))
        
        if not user_exist:
            user = User.objects.create(username=username, password= password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect('djangoapp:index')

        else:
            context['message'] = 'User already exists.'
            return render(request, 'djangoapp/registration.html', context)

        

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://c9f5dd50.us-east.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)
    
# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://c9f5dd50.us-east.apigw.appdomain.cloud/api/review"
        reviews = get_dealer_reviews_from_cf(url, dealerId = dealer_id)
        context["reviews"] = reviews
        context["dealerId"] = dealer_id
    return render(request, 'djangoapp/dealer_details.html', context)
        

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
def add_review(request, dealer_id):
    context = {}
    if request.method == 'GET':
        cars = CarModel.objects.filter(dealerId=dealer_id)
        url = "https://c9f5dd50.us-east.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf(url,dealer_id)
        context["cars"] = cars
        context["dealerId"] = dealer_id
        context["dealer_name"] = dealer.full_name
    
        return render(request, 'djangoapp/add_review.html',context)

    if request.method == 'POST':
        if request.user.is_authenticated:
            review = dict()
            #review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["review"] = request.POST.get('review')
            review["id"] = DealerReview.objects.all().count()+1
            review["name"] = request.user.get_full_name()
            if request.POST.get('purchasecheck') == 'on':
                 review["purchase"] = 'true'
                 review["purchase_date"] = request.POST.get('purchasedate')
            else:
                 review["purchase"] = 'false'
                 review["purchase_date"] = 'none'
            review["car_make"] = CarModel.objects.get(car_name=request.POST.get('car')).car_make.car_name
            review["car_model"] = CarModel.objects.get(car_name=request.POST.get('car')).car_type
            review["car_year"] = CarModel.objects.get(car_name=request.POST.get('car')).car_year.strftime("%Y")
            review["time"] = datetime.utcnow().isoformat()

            json_payload = dict()
            json_payload["review"] = review
            print(json_payload)
            response = post_request("https://c9f5dd50.us-east.apigw.appdomain.cloud/api/review", json_payload,
            dealerId = dealer_id)
            
            return redirect('djangoapp:dealer_details', dealer_id=dealer_id)
        else:
            context['message'] = 'Must be logged in to make a review.'
            return render(request, 'djangoapp/registration.html', context)

    return render(request, 'djangoapp/registration.html', context)


