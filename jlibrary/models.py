from django.db import models

# Create your models here.
class Author(models.Model):    
    full_name = models.TextField()
    country = models.CharField(max_length=2)
    birth_year = models.SmallIntegerField()

    def __str__(self):
        return self.full_name
    
class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.TextField()
    description = models.TextField()
    year_release = models.SmallIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    copy_count = models.SmallIntegerField(default=1)
    price = models.DecimalField(max_digits = 7, decimal_places=2)
    
    @staticmethod
    def author_info(obj):
        return f'{obj.author.full_name} [{obj.author.country}]'
        # return obj.author.full_name

    def __str__(self):
        return self.title