from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)
api_base="https://1b29c55a.au-syd.apigw.appdomain.cloud/api"
def about(request):
     return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = api_base+"/dealership"
        dealerId=request.GET.get('dealerId')
        state=request.GET.get('state')
        # Get dealers from the URL
        if dealerId:
            dealerships = get_dealers_from_cf(url,dealerId=int(dealerId))
        elif state:
            dealerships = get_dealers_from_cf(url,state=state)
        else:
            dealerships = get_dealers_from_cf(url)
        return render(request, 'djangoapp/index.html', {'dealerships':dealerships})


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = api_base+"/review"
        reviews = get_dealer_reviews_from_cf(url, dealerId=dealer_id)
        return render(request, 'djangoapp/dealer_details.html', {"reviews":reviews,"dealer_id":dealer_id})

def add_review(request, dealer_id):
    if request.user.is_authenticated:
        new_review=dict()
        new_review["car_make"]="Volvo"
        new_review["car_model"]="V60cc"
        new_review["car_year"]=2020
        new_review["dealership"]=dealer_id
        new_review["id"]=1
        new_review["name"]="Smooth swede"
        new_review["purchase"]=True
        new_review["purchase_date"]="16/12/21"
        new_review["review"]="Enjoying the wilderness"

        
        review_post_url=api_base+"/review"
        post_response=post_request(review_post_url,{"review":new_review})
        return HttpResponse(post_response)
    else:
        print("Unauthenticated User Please Log in to Submit Review")

