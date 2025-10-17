from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import os
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
import re
import random
import uuid
from datetime import timedelta


class Student(models.Model):
    FACULTY_CHOICES = [
        ('science', 'Science'),
        ('management', 'Management'),
        ('humanities', 'Humanities'),
    ]

    DEPARTMENT_CHOICES = [
        ('physics', 'Physics'),
        ('chemistry', 'Chemistry'),
        ('computer', 'Computer Science'),
        ('accounting', 'Accounting'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField(default="Unknown")
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    student_id = models.CharField(max_length=50, unique=True)
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    enrollment_date = models.DateField()
    photo = models.ImageField(upload_to="students/photos/", null=True, blank=True)
    id_document = models.FileField(upload_to="students/id_docs/", null=True, blank=True)
    admission_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    class_level = models.ForeignKey('ClassLevel', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class SchoolInfo(models.Model):
    """Basic school information that appears across the site"""
    name = models.CharField(max_length=200)
    motto = models.CharField(max_length=200, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='school/logo/')
    hero_image = models.ImageField(
        upload_to='school/hero/',  # Folder for hero images
        blank=True,                # Optional
        null=True                  # Optional
    )
    established_date = models.DateField()
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "School Information"

class Announcement(models.Model):
    AUDIENCE_CHOICES = [
        ('all', 'Everyone'),
        ('students', 'Students'),
        ('parents', 'Parents'),
        ('staff', 'Staff'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now_add=True)
    important = models.BooleanField(default=False)
    target_audience = models.CharField(
        max_length=10,
        choices=AUDIENCE_CHOICES,
        default='all'
    )
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('announcement-detail', kwargs={'pk': self.pk})


class AnnouncementAttachment(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='announcements/attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def filename(self):
        return os.path.basename(self.file.name)
    
    @property
    def get_file_type_icon(self):
        ext = os.path.splitext(self.file.name)[1].lower()
        if ext in ['.pdf']:
            return 'pdf'
        elif ext in ['.doc', '.docx']:
            return 'word'
        elif ext in ['.xls', '.xlsx']:
            return 'excel'
        elif ext in ['.ppt', '.pptx']:
            return 'powerpoint'
        elif ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'image'
        else:
            return 'alt'
class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='staff/photos/')
    position = models.CharField(max_length=100)
    department = models.CharField(
        max_length=50,
        choices=[
            ('administration', 'Administration'),
            ('teaching', 'Teaching Staff'),
            ('support', 'Support Staff')
        ]
    )
    join_date = models.DateField()
    is_teaching = models.BooleanField(default=False)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.full_name} ({self.position})"
    



class ClassLevel(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Student(models.Model):
    FACULTY_CHOICES = [
        ('science', 'Science'),
        ('arts', 'Arts'),
        ('engineering', 'Engineering'),
        # Add more choices as needed
    ]
    
    DEPARTMENT_CHOICES = [
        ('computer_science', 'Computer Science'),
        ('mathematics', 'Mathematics'),
        ('physics', 'Physics'),
        # Add more choices as needed
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=17)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    student_id = models.CharField(max_length=20, unique=True)
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    enrollment_date = models.DateField()
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    id_document = models.FileField(upload_to='id_documents/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

class Parent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=17)
    email = models.EmailField()
    address = models.TextField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class OTP(models.Model):
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_expired(self):
        expiration_time = self.created_at + timezone.timedelta(minutes=10)
        return timezone.now() > expiration_time
    
    @classmethod
    def generate_otp(cls, email=None, phone_number=None):
        # Delete any existing OTPs for this email/phone
        cls.objects.filter(email=email, phone_number=phone_number, is_verified=False).delete()
        
        # Generate a 6-digit OTP
        otp_code = str(uuid.uuid4().int)[:6]
        
        # Create and return the OTP object
        return cls.objects.create(
            email=email,
            phone_number=phone_number,
            otp_code=otp_code
        )
class Class(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Grade 10A"
    class_teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    academic_year = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(
        max_length=20,
        choices=[
            ('academic', 'Academic'),
            ('sports', 'Sports'),
            ('cultural', 'Cultural'),
            ('holiday', 'Holiday')
        ]
    )
    participants = models.ManyToManyField(Student, blank=True)
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

from django.db import models
from django.urls import reverse

from django.db import models
from django.urls import reverse
from django.utils import timezone
import os



class Gallery(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='gallery/covers/')
    date_created = models.DateTimeField(auto_now_add=True)  # ✅ fix
    event = models.ForeignKey('Event', on_delete=models.SET_NULL, null=True, blank=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('gallery-detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name_plural = "Galleries"
        ordering = ['-date_created']


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/images/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)  # ✅ fix
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    @property
    def filename(self):
        return os.path.basename(self.image.name)
    
    @property
    def get_file_type_icon(self):
        ext = os.path.splitext(self.image.name)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.gif']:
            return 'image'
        return 'file'



class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(Staff, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='news/images/')
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news-detail', kwargs={'pk': self.pk})

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
    





class OTP(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)

    @classmethod
    def generate_otp(cls, email=None, phone_number=None):
        otp_code = str(random.randint(100000, 999999))
        otp = cls.objects.create(email=email, phone_number=phone_number, otp_code=otp_code)
        return otp




class Admission(models.Model):
    """
    Model to store admission applications.
    """
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )

    # Personal Information
    applicant_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    applying_for_grade = models.CharField(max_length=50)

    # Parent/Guardian Information
    parent_guardian_name = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    
    # Educational Background
    previous_school = models.CharField(max_length=200)
    previous_report_card = models.FileField(upload_to='admission_documents/')
    
    # Other details
    application_essay = models.TextField(blank=True, null=True)
    date_submitted = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Optional: Link to a user if they are logged in
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Admission Application for {self.applicant_name}"


class Notice (models.Model):
    title = models.CharField(max_length=150)
    paragraph = models.CharField(max_length=1000)
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Facility(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='facility_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.ImageField(upload_to='program_icons/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title