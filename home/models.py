from django.db import models


class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.color_name


class Person(models.Model):
    name = models.CharField(max_length=100, unique=True)
    age = models.IntegerField()
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name="persons", null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name
