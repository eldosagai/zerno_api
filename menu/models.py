from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=300)
    
    def __str__(self) -> str:
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=300, unique=True)
    price = models.PositiveBigIntegerField(default=0)
    rating = models.FloatField(default=0.0)
    number_of_ratings = models.PositiveBigIntegerField(default=0)
    description = models.TextField()
    image = models.ImageField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='meals')

    def __str__(self) -> str:
        return self.name
    
    def change_rating(self, new_rating):
        self.number_of_ratings += 1
        self.rating = (self.rating * (self.number_of_ratings - 1) + new_rating) / self.number_of_ratings
        self.save(update_fields=['rating', 'number_of_ratings'])