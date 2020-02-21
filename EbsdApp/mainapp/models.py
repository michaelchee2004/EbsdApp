from django.db import models
import pandas as pd

class Option(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Year(models.Model):
    year_value = models.IntegerField()

    def __str__(self):
        return str(self.year_value)


class Capital(models.Model):
    option = models.ForeignKey('Option', on_delete=models.CASCADE)
    year = models.ForeignKey('Year', on_delete=models.CASCADE)
    capital_value = models.FloatField()

    def __str__(self):
        return str(self.capital_value)


class Opex(models.Model):
    option=models.ForeignKey('Option', on_delete=models.CASCADE)
    year = models.ForeignKey('Year', on_delete=models.CASCADE)
    opex_value = models.FloatField()

    def __str__(self):
        return str(self.opex_value)


class Capacity(models.Model):
    option = models.ForeignKey('Option', on_delete=models.CASCADE)
    capacity_value = models.FloatField()

    def __str__(self):
        return str(self.capacity_value)


class Demand(models.Model):
    year = models.ForeignKey('Year', on_delete=models.CASCADE)
    demand_value = models.FloatField()

    def __str__(self):
        return str(self.demand_value)


class CsvPath(models.Model):
    path = models.CharField(max_length=200)

    def __str__(self):
        return str(self.path)


class Utilisation(models.Model):
    option = models.ForeignKey('Option', on_delete=models.CASCADE)
    year = models.ForeignKey('Year', on_delete=models.CASCADE)
    util_value = models.FloatField()

    def __str__(self):
        return str(self.util_value)



