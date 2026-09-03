from django.db import models
from django.contrib.auth.models import User


# Job Model
class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.CharField(max_length=300)

    def __str__(self):
        return self.title


# Application Model
class Application(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )
    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
    max_length=20,
    choices=[
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
    ],
    default='Submitted'
)

    def __str__(self):
        return f"{self.name} - {self.job.title}"