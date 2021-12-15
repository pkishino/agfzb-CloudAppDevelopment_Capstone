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

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
