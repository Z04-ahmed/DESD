from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class Student(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True, default="noemail@example.com")  # Default email for existing rows
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hash the password before saving (if not already hashed)
        if not self.pk or not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(Student, self).save(*args, **kwargs)

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    campus_involvement = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    
    
class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name='created_communities', on_delete=models.CASCADE)
    leader = models.ForeignKey(User, related_name='leading_communities', on_delete=models.SET_NULL, null=True, blank=True)
    members = models.ManyToManyField(User, related_name='joined_communities')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name