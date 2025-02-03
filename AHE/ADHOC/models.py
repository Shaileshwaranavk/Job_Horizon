from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    company_size = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    password = models.CharField(max_length=255)  # Store hashed passwords
    gender_choices = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=gender_choices)
    experience = models.TextField(blank=True, null=True)
    domains = models.CharField(max_length=255, blank=True, null=True)
    expected_pay = models.CharField(max_length=100, blank=True, null=True)
    projects = models.TextField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.name

class OrganizationProfile(models.Model):
    organization_name = models.CharField(max_length=255)
    manager_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    company_size = models.CharField(max_length=100)
    company_description = models.TextField()
    company_type = models.CharField(max_length=100)
    password=models.CharField(max_length=100,default='1234')

    def __str__(self):
        return self.organization_name


class JobOpening(models.Model):
    organization = models.ForeignKey(OrganizationProfile, related_name='job_openings', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    required_skills = models.CharField(max_length=255)
    pay = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.job_title