from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client


from .forms import (
    UserRegistrationForm, UserRegistrationForm,
    ParentRegistrationForm, StudentRegistrationForm, ContactForm,AdmissionForm
)
from .models import (
    Announcement, Staff, Student, Event, 
    News, Gallery, GalleryImage, ContactMessage,
    SchoolInfo, Parent, Class, Subject, OTP,Program,Facility,Notice
)


# ---------------------------
# Home Page Views
# ---------------------------
def home(request):
    school_info = SchoolInfo.objects.first()
    announcements = Announcement.objects.filter(important=True).order_by('-date_posted')[:3]
    upcoming_events = Event.objects.filter(start_date__gte=timezone.now()).order_by('start_date')[:3]
    latest_news = News.objects.filter(is_published=True).order_by('-date_posted')[:3]
    
    context = {
        'school_info': school_info,
        'announcements': announcements,
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
    }
    return render(request, 'main/home.html', context)


# ---------------------------
# About Views
# ---------------------------
def about(request):
    school_info = SchoolInfo.objects.first()
    staff_count = Staff.objects.count()
    return render(request, 'about/about.html', {
        'school_info': school_info,
        'staff_count': staff_count,
    })

def mission(request):
    return render(request, 'about/mission.html', {
        'school_info': SchoolInfo.objects.first()
    })

def history(request):
    return render(request, 'about/history.html', {
        'school_info': SchoolInfo.objects.first()
    })


# ---------------------------
# Announcement Views
# ---------------------------
class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/list.html'
    context_object_name = 'announcements'
    ordering = ['-date_posted']
    paginate_by = 10

class AnnouncementDetailView(DetailView):
    model = Announcement
    template_name = 'announcements/detail.html'
    context_object_name = 'announcement'


# ---------------------------
# Staff Views
# ---------------------------
class StaffListView(ListView):
    model = Staff
    template_name = 'about/staff.html'
    context_object_name = 'staff_members'
    paginate_by = 12

    def get_queryset(self):
        department = self.request.GET.get('department')
        return Staff.objects.filter(department=department) if department else Staff.objects.all()

class StaffDetailView(DetailView):
    model = Staff
    template_name = 'main/staff/detail.html'
    context_object_name = 'staff'


# ---------------------------
# Academics
# ---------------------------
def academics_view(request):
    return render(request, "academics/academics.html", {
        "school_info": SchoolInfo.objects.first(),
        "classes": Class.objects.all(),
        "subjects": Subject.objects.all(),
    })

def curriculum(request):
    return render(request, 'academics/curriculum.html')

def subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, "academics/subject_detail.html", {"subject": subject})


# ---------------------------
# Event Views
# ---------------------------
class EventListView(ListView):
    model = Event
    template_name = 'events/list.html'
    context_object_name = 'events'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        event_type = self.request.GET.get('type')
        month = self.request.GET.get('month')
        timeframe = self.request.GET.get('timeframe', 'upcoming')

        if event_type:
            queryset = queryset.filter(event_type=event_type)
        if month:
            queryset = queryset.filter(start_date__month=month)
        if timeframe == 'upcoming':
            queryset = queryset.filter(start_date__gte=timezone.now())
        elif timeframe == 'past':
            queryset = queryset.filter(start_date__lt=timezone.now())

        return queryset.order_by('start_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        months = Event.objects.dates('start_date', 'month')
        context.update({
            'current_type': self.request.GET.get('type'),
            'current_month': self.request.GET.get('month'),
            'current_timeframe': self.request.GET.get('timeframe', 'upcoming'),
            'months': [{'num': date.month, 'name': date.strftime('%B')} for date in months],
        })
        return context

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_events'] = Event.objects.filter(
            event_type=self.object.event_type
        ).exclude(pk=self.object.pk)[:3]
        return context


# ---------------------------
# News Views
# ---------------------------
class NewsListView(ListView):
    model = News
    template_name = 'news/list.html'
    context_object_name = 'news_list'
    ordering = ['-date_posted']
    paginate_by = 5

class NewsDetailView(DetailView):
    model = News
    template_name = 'news/detail.html'
    context_object_name = 'news'


# ---------------------------
# Gallery Views
# ---------------------------
class GalleryListView(ListView):
    model = Gallery
    template_name = 'gallery/list.html'
    context_object_name = 'galleries'
    paginate_by = 12
    
    def get_queryset(self):
        return Gallery.objects.filter(is_published=True).order_by('-date_created')

class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'gallery/detail.html'
    context_object_name = 'gallery'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_galleries'] = Gallery.objects.filter(
            is_published=True
        ).exclude(pk=self.object.pk)[:4]
        return context


# ---------------------------
# Contact
# ---------------------------
class ContactView(CreateView):
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Your message has been sent successfully!')
        return response

def contact_success(request):
    return render(request, 'contact/success.html')


# ---------------------------
# Portals
# ---------------------------
class StudentPortalView(LoginRequiredMixin, TemplateView):
    template_name = 'portals/student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['student'] = Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            pass
        return context

class ParentPortalView(LoginRequiredMixin, TemplateView):
    template_name = 'portals/parent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            parent = Parent.objects.get(user=self.request.user)
            context['parent'] = parent
            context['children'] = [parent.student]  # ✅ fixed
        except Parent.DoesNotExist:
            pass
        return context
    

def Notice(request):
    
    messages = Notice.objects.first()
    context = {
        'messages' :messages
    }

    return render(request, "main/base.html",context)

# ---------------------------
# Utility Views
# ---------------------------
def calendar(request):
    return render(request, 'utilities/calendar.html', {
        'events': Event.objects.all().order_by('start_date')
    })

def resources(request):
    return render(request, 'utilities/resources.html')

def faq(request):
    return render(request, 'utilities/faq.html')

def privacy(request):
    return render(request, 'utilities/privacy.html', {
        'school_info': SchoolInfo.objects.first()
    })

def terms(request):
    return render(request, 'utilities/terms.html', {
        'school_info': SchoolInfo.objects.first()
    })

def sitemap(request):
    return render(request, 'utilities/sitemap.html', {'school_info': SchoolInfo.objects.first()})

def accessibility(request):
    return render(request, 'utilities/accessibility.html', {'school_info': SchoolInfo.objects.first()})

# About / Facilities page
def facilities(request):
    return render(request, 'about/facilities.html', {
        'school_info': SchoolInfo.objects.first(),
        'facilities': Facility.objects.all()
    })

# Academics / Special Programs page
def programs(request):
    return render(request, 'academics/programs.html', {
        'school_info': SchoolInfo.objects.first(),
        'programs': Program.objects.all()
    })




# Academics / Admissions page
def admission(request):
    """
    Handles the admission application process.
    """
    if request.method == 'POST':
        form = AdmissionForm(request.POST, request.FILES)
        if form.is_valid():
            admission = form.save(commit=False)
            # You can set the user if they are logged in, or leave it anonymous
            if request.user.is_authenticated:
                admission.user = request.user
            admission.save()
            messages.success(request, 'Your admission application has been submitted successfully!')
            return redirect('admission-success') # Redirect to a success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdmissionForm()

    return render(request, 'academics/admissions.html', {
        'form': form,
        'school_info': SchoolInfo.objects.first(),
    })

def admission_success(request):
    """
    A simple view to display a success message after submitting an application.
    """
    return render(request, 'academics/admission_success.html', {
        'school_info': SchoolInfo.objects.first(),
    })


# ---------------------------
# Registration (with OTP for Parent)
# ---------------------------
def register(request):
    return render(request, 'registration/register.html')


def send_otp_email(email, otp_code):
    subject = 'Your OTP Code for Registration'
    message = f'Your OTP code is: {otp_code}. It will expire in 10 minutes.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)


# ---------------------------
# Send OTP via WhatsApp
# ---------------------------
def send_otp_whatsapp(phone_number, otp_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP code is: {otp_code}. It will expire in 10 minutes.",
        from_=settings.TWILIO_WHATSAPP_NUMBER,  # Twilio sandbox WhatsApp number
        to=f"whatsapp:{phone_number}"
    )
    return message.sid


# ---------------------------
# Send OTP via SMS
# ---------------------------
def send_otp_sms(phone_number, otp_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP code is: {otp_code}. It will expire in 10 minutes.",
        from_=settings.TWILIO_PHONE_NUMBER,  # Twilio SMS-enabled number
        to=phone_number
    )
    return message.sid


# ---------------------------
# Student Register
# ---------------------------
def student_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        student_form = StudentRegistrationForm(request.POST, request.FILES)
        
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            
            login(request, user)
            messages.success(request, 'Student registration successful!')
            return redirect('register')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegistrationForm()
        student_form = StudentRegistrationForm()
    
    return render(request, 'registration/student_register.html', {
        'user_form': user_form,
        'student_form': student_form
    })


# ---------------------------
# Parent Register
# ---------------------------
def parent_register(request):
    if request.method == 'POST':
        if 'verify_otp' in request.POST:
            # OTP verification step
            email = request.session.get('registration_email')
            phone_number = request.session.get('registration_phone')
            country_code = request.session.get('registration_country_code')
            otp_code = request.POST.get('otp_code')

            try:
                otp = OTP.objects.get(
                    email=email,
                    phone_number=phone_number,
                    otp_code=otp_code,
                    is_verified=False
                )
                if otp.is_expired():
                    messages.error(request, 'OTP has expired. Please request a new one.')
                else:
                    otp.is_verified = True
                    otp.save()

                    user_form = UserRegistrationForm(request.session.get('user_form_data'))
                    parent_form = ParentRegistrationForm(request.session.get('parent_form_data'))

                    if user_form.is_valid() and parent_form.is_valid():
                        user = user_form.save()
                        parent = parent_form.save(commit=False)
                        parent.user = user
                        parent.save()
                        login(request, user)
                        messages.success(request, 'Parent registration successful!')
                        return redirect('home')
            except OTP.DoesNotExist:
                messages.error(request, 'Invalid OTP code.')

            return render(request, 'registration/verify_otp.html', {
                'email': email,
                'phone': phone_number,
                'country_code': country_code
            })

        else:
            # First step: submit forms
            user_form = UserRegistrationForm(request.POST)
            parent_form = ParentRegistrationForm(request.POST)

            if user_form.is_valid() and parent_form.is_valid():
                email = user_form.cleaned_data.get('email')
                phone_number = parent_form.cleaned_data.get('phone_number')
                country_code = request.POST.get('country_code', '')
                
                # Combine country code with phone number for full international format
                full_phone_number = f"{country_code}{phone_number}" if phone_number else None

                # Save form data into session
                request.session['user_form_data'] = request.POST.dict()
                request.session['parent_form_data'] = request.POST.dict()
                request.session['registration_email'] = email
                request.session['registration_phone'] = full_phone_number
                request.session['registration_country_code'] = country_code

                otp = OTP.generate_otp(email=email, phone_number=full_phone_number)

                # Send OTP via email
                send_otp_email(email, otp.otp_code)

                # Send OTP via WhatsApp and SMS if phone number provided
                if full_phone_number:
                    try:
                        send_otp_whatsapp(full_phone_number, otp.otp_code)
                    except Exception as e:
                        messages.warning(request, f'WhatsApp OTP failed: {str(e)}')
                    
                    try:
                        send_otp_sms(full_phone_number, otp.otp_code)
                    except Exception as e:
                        messages.warning(request, f'SMS OTP failed: {str(e)}')

                messages.info(request, f'An OTP has been sent to {email} and phone number {full_phone_number}.')
                return render(request, 'registration/verify_otp.html', {
                    'email': email,
                    'phone': full_phone_number,
                    'country_code': country_code
                })
    else:
        user_form = UserRegistrationForm()
        parent_form = ParentRegistrationForm()
    
    return render(request, 'registration/parent_register.html', {
        'user_form': user_form,
        'parent_form': parent_form
    })


# ---------------------------
# Resend OTP
# ---------------------------
def resend_otp(request):
    email = request.session.get('registration_email')
    phone_number = request.session.get('registration_phone')
    country_code = request.session.get('registration_country_code')

    if email or phone_number:
        otp = OTP.generate_otp(email=email, phone_number=phone_number)

        if email:
            send_otp_email(email, otp.otp_code)
        if phone_number:
            try:
                send_otp_whatsapp(phone_number, otp.otp_code)
            except Exception as e:
                messages.warning(request, f'WhatsApp OTP failed: {str(e)}')
            
            try:
                send_otp_sms(phone_number, otp.otp_code)
            except Exception as e:
                messages.warning(request, f'SMS OTP failed: {str(e)}')

        messages.info(request, f'A new OTP has been sent to {email} and phone number {phone_number}.')
    else:
        messages.error(request, 'Session expired. Please start registration again.')

    return render(request, 'registration/verify_otp.html', {
        'email': email,
        'phone': phone_number,
        'country_code': country_code
    })

