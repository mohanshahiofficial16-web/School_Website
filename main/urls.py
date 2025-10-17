from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import (
    AnnouncementListView, AnnouncementDetailView,
    StaffListView, StaffDetailView,
    EventListView, EventDetailView,
    NewsListView, NewsDetailView,
    GalleryListView, GalleryDetailView,
    ContactView, StudentPortalView, ParentPortalView,subject,academics_view, admission,admission_success
)

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About pages
    path('about/', views.about, name='about'),
    path('about/mission/', views.mission, name='mission'),
    path('about/history/', views.history, name='history'),
    
    # Announcements
    path('announcements/', AnnouncementListView.as_view(), name='announcements'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    
    # Staff directory
    path('staff/', StaffListView.as_view(), name='staff-list'),
    path('staff/<int:pk>/', StaffDetailView.as_view(), name='staff-detail'),
    
    # Academic information
    path('academics/', views.academics_view, name='academics'),
    path('academics/', views.academics_view, name='subjects'),  # 👈 alias
    path('academics/curriculum/', views.curriculum, name='curriculum'),
    path("academics/subject/<int:pk>/", views.subject, name="subject"),
    path('academics/admissions/apply/', views.admission, name='admissions'),
    path('academics/admissions/success/', views.admission_success, name='admission-success'),
    
  


    
    # Events calendar
    path('events/', EventListView.as_view(), name='events'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    
    # News
    path('news/', NewsListView.as_view(), name='news'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    
    # Gallery
    path('gallery/', GalleryListView.as_view(), name='gallery'),
    path('gallery/<int:pk>/', GalleryDetailView.as_view(), name='gallery-detail'),
    
    # Contact
    path('contact/', ContactView.as_view(), name='contact'),
    
    # Portals (protected views)
    path('portal/student/', StudentPortalView.as_view(), name='student-portal'),
    path('portal/parent/', ParentPortalView.as_view(), name='parent-portal'),
    
    # Utility pages
    path('calendar/', views.calendar, name='calendar'),
    path('resources/', views.resources, name='resources'),
    path('faq/', views.faq, name='faq'),


    path('register/', views.register, name='register'),
    path('register/student/', views.student_register, name='student_register'),
    path('register/parent/', views.parent_register, name='parent_register'),
    path('register/resend-otp/', views.resend_otp, name='resend_otp'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    path('facilities/', views.facilities, name='facilities'),
    path('programs/', views.programs, name='programs'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
         
    
]