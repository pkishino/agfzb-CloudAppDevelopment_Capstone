from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30, default='car maker')
    description = models.CharField(max_length=1000)
    def __str__(self):
        return "Name:"+self.name+"\nDescription:"+self.description

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_model = models.CharField(null=False, max_length=30, default='car model')
    description = models.CharField(max_length=1000)
    car_year = models.DateField(null=True)
    dealer_id = models.IntegerField(default=1)
    SUV = 'SUV'
    WAGON = 'Wagon'
    SEDAN = 'Sedan'
    CONVERTIBLE = 'Convertible'
    car_types = [
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (SEDAN, 'Sedan'),
        (CONVERTIBLE, 'Convertible')
    ]
    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=car_types,
        default=SEDAN
    )
    def __str__(self):
        return "Maker:"+self.car_make.name+"\nmodel:"+self.car_model+" Year:"+str(self.car_year).split('-')[0]+\
            "\nDetails:\n   -"+self.description+"\n   -"+self.car_type+"\n Available at:"+str(self.dealer_id)+"(Dealer id)"

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, state,st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.state = state
        # Dealer state short
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self,dealership,name,purchase,review,purchase_date,car_make,car_model,car_year,id,sentiment='neutral'):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review: " + self.review
