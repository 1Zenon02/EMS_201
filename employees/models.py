from datetime import timedelta
from django.db import models
from django.contrib.auth.models import  PermissionsMixin, BaseUserManager, AbstractBaseUser, Group, Permission


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Optional: set active by default
        extra_fields.setdefault('role', 'admin')

        if not email:
            raise ValueError("The Email field must be set")

        if not username:
            raise ValueError("The Username field must be set")

        # Call the create_user method to handle user creation
        return self.create_user(email=email, username=username, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=300)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default= False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')
    salary_rate = models.DecimalField(max_digits=6, decimal_places=2, default=20.00, help_text="Hourly rate in currency units")

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # List all required fields here

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Custom related name to avoid clashes
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Custom related name to avoid clashes
        blank=True,
    )

    def __str__(self):
        return self.username

    def is_admin_user(self):
        return self.role == 'admin'

    def is_employee_user(self):
        return self.role == 'employee'

class SignInOut(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendance')
    sign_in_time = models.DateTimeField()
    sign_out_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def duration(self):
        if self.sign_out_time:
            # Calculate duration in hours
            return (self.sign_out_time - self.sign_in_time).total_seconds() / 3600
        return 0.0  # Return 0 hours if not signed out

    def calculate_salary(self):
        hours_worked = self.duration() # Convert duration to hours
        salary_rate = self.user.salary_rate
        return round(hours_worked * float(salary_rate), 2)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    class Meta:
        verbose_name = "Sign-In/Out Record"
        verbose_name_plural = "Sign-In/Out Records"
        unique_together = ('user', 'date')

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateField()
    end = models.DateField()

    def __str__(self):
        return self.title

class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.title