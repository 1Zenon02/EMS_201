from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import *


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Redirect based on user role
                if user.is_staff:  # Assuming admin users have is_staff set to True
                    return redirect('admin_dashboard')  # Replace with your admin dashboard URL
                else:
                    return redirect('employee_dashboard')  # Replace with your employee dashboard URL

            else:
                return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def admin_dashboard(request):
    employees = CustomUser.objects.filter(role='employee')# Fetch all users with employee role from the database
    print(f"Employees: {employees}")
    return render(request, 'dashboard/admin_dashboard.html', {'employees': employees})

def employee_dashboard(request):
    return render(request, 'dashboard/employee_dashboard.html', {})
def logout_view(request):
    logout(request)
    return redirect('index')

def calendar_view(request):
    tasks = Task.objects.filter(user=request.user)  # Fetch all tasks from the database
    print(f"Tasks fetched: {tasks}")
    return render(request, 'calendar/calendar.html', {'tasks': tasks})

def add_task(request):
    tasks = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Automatically assign the logged-in user
            task.save()
            return redirect('calendar')
    else:
        form = TaskForm()
        context = {
            'tasks': tasks,  # Pass the tasks to the template
            'form': form
        }
    return render(request, 'calendar/add_task.html', {'form': form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('view_task')
    else:
        form = TaskForm(instance=task)

    return render(request, 'calendar/edit_task.html', {'form': form})

def view_task(request):
    tasks = Task.objects.filter(user=request.user)  # F
    return render(request, 'calendar/view_task.html', {'tasks': tasks})

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task has been deleted successfully.')
        return redirect('view_task')  # Redirect to the task list view
    return render(request, 'calendar/delete_task.html', {'task': task})

def custom_logout(request):
    logout(request)
    return redirect('index')

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            today = timezone.now().date()
            # Check if a sign-in record exists for today
            if SignInOut.objects.filter(user=request.user, date=today).exists():
                return redirect('salary_record')  # Redirect to user's profile page if record exists

            # Retrieve the salary rate from the user's profile
            salary_rate = request.user.salary_rate  # Adjust this if salary_rate is in another related model

            # Create a new sign-in record
            SignInOut.objects.create(
                user=request.user,
                sign_in_time=timezone.now(),
                salary_rate=salary_rate  # Use the retrieved salary rate
            )
            return redirect('salary_record')  # Redirect to attendance list or another page
    else:
        form = SignInForm()

    return render(request, 'employees/sign_in.html', {'form': form})


def sign_out_view(request):
    if request.method == 'POST':
        form = SignOutForm(request.POST)
        if form.is_valid():
            # Check for the latest sign-in record without a sign-out time
            today = timezone.now().date()
            try:
                attendance_record = SignInOut.objects.get(user=request.user, date=today)

                # Check if sign_out_time is not empty
                if attendance_record.sign_out_time:
                    return redirect('salary_record')  # Redirect if already signed out

                # Otherwise, set sign_out_time and save
                attendance_record.sign_out_time = timezone.now()
                attendance_record.save()
                return redirect('salary_record')  # Redirect to attendance list or other page
            except SignInOut.DoesNotExist:
                # Handle case where no matching record is found
                return render(request, 'employees/sign_out.html', {
                    'form': form,
                    'error': 'You must sign in before signing out today.'
                })
    else:
        form = SignOutForm()

    return render(request, 'employees/sign_out.html', {'form': form})

def attendance_report(request):
    # Get all sign-in/out records for the logged-in user
    attendance_records = SignInOut.objects.filter(user=request.user).order_by('-date')

    context = {
        'attendance_records': attendance_records
    }
    return render(request, 'employees/attendance_report.html', context)

@login_required
def attendance_overview_view(request):
    # Check if the user is an admin
    if request.user.role != 'admin':
        return render(request, '403.html')
    # Retrieve all sign-in/out records
    attendance_records = SignInOut.objects.all()

    return render(request, 'employees/attendance_overview.html', {'attendance_records': attendance_records})


@login_required
def edit_employee_view(request, user_id):
    # Ensure the user is an admin
    if request.user.role != 'admin':
        return render(request, '403.html')

    # Fetch the employee/user based on the user_id
    employee = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to the admin dashboard after saving
    else:
        form = CustomUserForm(instance=employee)

    return render(request, 'employees/edit_employee.html', {
        'form': form,
        'employee': employee
    })