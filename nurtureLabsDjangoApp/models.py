from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.user_id} {self.name} {self.email}"



class Advisor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    photo_url = models.URLField()

    def __str__(self):
        return f"{self.name} {self.photo_url}"


class Booking(models.Model):
    id = models.ForeignKey('nurtureLabsDjangoApp.Advisor', primary_key=True, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    user_id = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id} {self.date} {self.time}"
