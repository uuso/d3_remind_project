from django.db import models


class Author(models.Model):
    full_name = models.TextField()
    country = models.CharField(max_length=2)
    birth_year = models.SmallIntegerField()

    def __str__(self):
        return self.full_name


class Publisher(models.Model):
    title = models.TextField()
    city = models.TextField()
    country = models.CharField(max_length=2)

    def __str__(self):
        return f'{self.title} ({self.city}, {self.country})'


class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.TextField()
    description = models.TextField()
    year_release = models.SmallIntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True)
    copy_count = models.SmallIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    # @staticmethod
    def author_info(self):
        return f'{self.author.full_name} [{self.author.country}]'
        # return obj.author.full_name

    def __str__(self):
        return f'"{self.title}", {self.author} ({self.year_release})'
