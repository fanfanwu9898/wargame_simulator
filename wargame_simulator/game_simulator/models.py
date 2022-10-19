from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    number_of_wins = models.IntegerField()

class Game(models.Model):
    player_name_x = models.CharField(max_length=50)
    player_name_y = models.CharField(max_length=50)
    winner = models.CharField(max_length=50)
    number_of_rounds = models.IntegerField()
    number_of_war_rounds = models.IntegerField()
    game_id = models.IntegerField()

class Round(models.Model):
    game_id = models.IntegerField()
    player_x_deck = models.TextField()
    player_y_deck = models.TextField()
    war_round = models.BooleanField()