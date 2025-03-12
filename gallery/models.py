from django.db import models

class CustomForm(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField()
    datetime = models.DateTimeField()

    def __str__(self):
        return self.name

class videoform(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    video = models.FileField()
    datetime = models.DateTimeField()

    def __str__(self):
        return self.name