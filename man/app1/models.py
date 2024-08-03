from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Prediction(models.Model):
    location = models.CharField(max_length=255)
    bhk = models.IntegerField()
    bath = models.DecimalField(max_digits=5, decimal_places=2)
    sqft = models.DecimalField(max_digits=10, decimal_places=2)
    prediction = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.prediction}"