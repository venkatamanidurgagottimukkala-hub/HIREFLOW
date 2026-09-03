from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Job, Application


def home(request):
    jobs = Job.objects.all()

    keyword = request.GET.get('keyword', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')

    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(skills__icontains=keyword)
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if category:
     jobs = jobs.filter(
        Q(title__icontains=category) |
        Q(skills__icontains=category)
    )

    return render(
        request,
        'jobs/home.html',
        {
            'jobs': jobs,
            'keyword': keyword,
            'location': location
        }
    )


def job_detail(request, job_id):
    job = Job.objects.get(id=job_id)
    return render(request, 'jobs/job_detail.html', {'job': job})

@login_required
def apply(request, job_id):
    job = Job.objects.get(id=job_id)



    already_applied = Application.objects.filter(
        user=request.user,
        job=job
    ).exists()

    if already_applied:
        return render(
            request,
            'jobs/already_applied.html',
            {'job': job}
        )

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        resume = request.FILES.get('resume')

        Application.objects.create(
    user=request.user,
    job=job,
    name=name,
    email=email,
    phone=phone,
    resume=resume
)
        

        return render(request, 'jobs/success.html', {'job': job})

    return render(request, 'jobs/apply.html', {'job': job})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'jobs/register.html', {
                'error': 'Username already exists'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'jobs/register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        return render(request, 'jobs/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'jobs/login.html')


def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def my_applications(request):
    applications = Application.objects.filter(
        user=request.user
    ).order_by('-applied_at')

    return render(
        request,
        'jobs/my_applications.html',
        {'applications': applications}
    )