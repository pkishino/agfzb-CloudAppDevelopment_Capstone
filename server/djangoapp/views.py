from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request, get_dealer_with_id_from_cf, get_dealer_with_state_from_cf, post_review, get_review_context
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)

def about(request):
     return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
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

def home(request):
    return render(request, 'djangoapp/index.html')

def get_dealerships(request):
    if request.method == "GET":
        dealerships = get_dealers_from_cf()
        return render(request, 'djangoapp/dealerships.html', {'dealerships':dealerships})


def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        reviews = get_dealer_reviews_from_cf(dealerId=dealer_id)
        dealer = get_dealer_with_id_from_cf(dealer_id)[0]
        return render(request, 'djangoapp/dealer_details.html', {"dealer_id":dealer_id,"reviews":reviews,"dealer":dealer})

def add_review(request, dealer_id):
    if request.method == "GET":
        return render(request, 'djangoapp/add_review.html',get_review_context(dealer_id))
    elif request.method == "POST":
        if request.user.is_authenticated:
            model= get_object_or_404(CarModel, id=request.POST['car'])
            review={
                'name':request.user.first_name+' '+request.user.last_name,
                'dealership': dealer_id,
                'review': request.review
            }
                # new_review=dict()
                # new_review["car_make"]="Volvo"
                # new_review["car_model"]="V60cc"
                # new_review["car_year"]=2020
                # new_review["dealership"]=dealer_id
                # new_review["id"]=1
                # new_review["name"]="Smooth swede"
                # new_review["purchase"]=True
                # new_review["purchase_date"]="16/12/21"
                # new_review["review"]="Enjoying the wilderness"
                # post_response=post_review({"review":new_review})
                # return HttpResponse(post_response)
                return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            context=get_review_context(dealer_id)
            context["message"]="Unauthenticated User Please Log in to Submit Review"
            return render(request, 'djangoapp/add_review.html', context)

