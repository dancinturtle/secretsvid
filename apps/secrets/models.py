from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def register(self, postedName):
        if len(postedName) < 1:
            return(False, "Username cannot be empty")
        try:
            self.get(username=postedName)
            return(False, "Username already exists")
        except:
            newuser = self.create(username=postedName)
            return(True, newuser)
    def login(self, postedName):
        try:
            founduser = self.get(username=postedName)
            return(True, founduser)
        except:
            return(False, "Username was not found in our database")

class SecretManager(models.Manager):
    def validate(self, postedSecret, userid):
        # all posted secrets should have more than 3 characters
        if len(postedSecret)<4:
            return(False, "Secrets must be at least four characters long")
        try:
            currentuser = User.objects.get(id=userid)
            self.create(secret=postedSecret, author=currentuser)
            return(True, "Your secret is safe with us")
        except:
            return(False, "We could not create this secret")
    def newlike(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "This secret is not found in our database")
        user = User.objects.get(id=userid)
        if secret.author == user:
            return(False, "Shame on you, you shouldn't like your own secrets")
        secret.likers.add(user)
        return(True, "You liked this secret!")
    def deleteLike(self, secretid, userid):
        try:
            secret = self.get(id=secretid)
        except:
            return(False, "This secret is not found in our database")
        user = User.objects.get(id=userid)
        if secret.author != user:
            return(False, "Shame on you, you shouldn't delete secrets that aren't your own")
        secret.delete()
        return(True, "Secret deleted")


class User(models.Model):
    username = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Secret(models.Model):
    secret = models.CharField(max_length=400)
    author = models.ForeignKey(User)
    likers = models.ManyToManyField(User, related_name="likedsecrets")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = SecretManager()
