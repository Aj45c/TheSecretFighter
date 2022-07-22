from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=50)
    release = models.DateField()
    publisher = models.CharField(max_length=150)
    num_of_chars = models.IntegerField()
    crit_rating = models.IntegerField()
    description =models.CharField(max_length=1000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'game_id': self.id})
#================================================================
class Photo(models.Model):
  url = models.CharField(max_length=200)
  game = models.ForeignKey(Game, on_delete=models.CASCADE)

  def __str__(self):
    return f"Photo for game_id: {self.game_id} @{self.url}"