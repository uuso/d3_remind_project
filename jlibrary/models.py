from django.db import models


class Author(models.Model):
    full_name = models.TextField()
    country = models.CharField(max_length=2)
    birth_year = models.SmallIntegerField()

    def inspired(self):
        """Method to show many-to-many relition usage."""
        result = ""
        for _, ins in enumerate(self.inspired_by.all()):
            result += f'{ins.author.full_name} with {ins.book}'
            if _ <= len(self.inspired_by.all())-2:
                result += ', '
        return result

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
    authors = models.ManyToManyField(
        Author,
        through='BookCreators',
        # it's necessary to keep these fields in the correct order
        through_fields=('book', 'author')
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True)
    copy_count = models.SmallIntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def authors_info(self):
        result = ""
        for _, author in enumerate(self.authors.all()):
            result += author.full_name
            if _ <= len(self.authors.all())-2:
                result += ', '
        return result

    def __str__(self):
        return f'"{self.title}" ({self.year_release})'


class BookCreators(models.Model):
    """Class to demonstrate many-to-many fields in django.
    # It allows books to be written by multiple authors."""
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    inspirer = models.ForeignKey(
        Author, on_delete=models.SET_NULL, related_name="inspired_by", blank=True, null=True)
