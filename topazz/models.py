from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    ROLES = (
        ("electrician", "Electrician"),
        ("plumber", "Plumber"),
        ("carpenter", "Carpenter"),
        ("welder", "Welder"),
        ("mechanic", "Mechanic"),

    )

    role = models.CharField(max_length=12, choices=ROLES)
    image = models.ImageField(upload_to='team/images/', default='default.png')

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=6)
    email = models.EmailField()
    phone_no = models.IntegerField()
    services = models.CharField(max_length=150)

    def __str__(self):
        return self.name
