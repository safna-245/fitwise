from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Foodlog(models.Model):

    MEAL_CHOICES = [
        ('BF', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('DINNER', 'Dinner'),
        ('SNACK', 'Snack'),
    ]

    title = models.CharField(max_length=100)

    calorie = models.PositiveIntegerField()

    meal_type = models.CharField(max_length=30,choices=MEAL_CHOICES)

    serving_size = models.CharField(max_length=100)

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='food_logs'
        )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title