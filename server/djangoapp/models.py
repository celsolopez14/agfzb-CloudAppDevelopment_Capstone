from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    car_name = models.CharField(null=False, max_length=20, primary_key=True)
    car_description = models.TextField()

    def __str__(self):
        return self.car_name + " " + self.car_description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    RANDOM = "random car"

    CAR_TYPE_CHOICES = [
        (SEDAN,"Sedan"),
        (SUV,"SUV"),
        (WAGON,"Wagon"),
        (RANDOM,"Random car"),
    ]
    car_make = models.ForeignKey(CarMake,null=True,on_delete=models.CASCADE)
    car_name = models.CharField(null=False, max_length=20, primary_key=True)
    dealerId = models.IntegerField()
    car_type = models.CharField(null=False,choices=CAR_TYPE_CHOICES, default=RANDOM, max_length=20)
    car_year = models.DateField(null=True)

    def __str__(self):
        return self.car_name + " " + self.dealerId + " " + self.car_type + " " + self.car_year


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
