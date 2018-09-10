from django.db import models


class Weightclass(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

class Fighter(models.Model):
    owner = models.ForeignKey(
        'auth.User',
        related_name='fighters',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, unique=True)
    birthplace = models.CharField(max_length=200)
    age = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    reach = models.IntegerField()
    wins = models.IntegerField()
    losses = models.IntegerField()
    draws = models.IntegerField()
    weightclass = models.ForeignKey(
        Weightclass,
        related_name='fighters',
        on_delete=models.CASCADE
    )
    latitude = models.FloatField(default=None, blank=True, null=True)
    longitude = models.FloatField(default=None, blank=True, null=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
