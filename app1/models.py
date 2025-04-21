from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone


# Custom User Model
class All_Users(AbstractUser):
    USER_ROLES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=USER_ROLES, default='student')  # Role: student, faculty, or admin
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



# Classroom model
class Classrooms(models.Model):
    classroom_id = models.AutoField(primary_key=True)  # Primary Key, Auto-incremented Integer
    faculty_id = models.ForeignKey(All_Users, on_delete=models.CASCADE, related_name='created_classrooms')  # Faculty who created the classroom
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Optional description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for classroom creation

    def __str__(self):
        return self.name

# Classroom_Students model (composite primary key)
class Classroom_Students(models.Model):
    classroom_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    student_id = models.ForeignKey(All_Users, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when student joined the classroom

    class Meta:
        unique_together = ('classroom_id', 'student_id')  # Composite primary key

    def __str__(self):
        return f"{self.student_id.username} in {self.classroom_id.name}"

# Classroom_Requests model
class Classroom_Requests(models.Model):
    REQUEST_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    request_id = models.AutoField(primary_key=True)  # Primary Key, Auto-incremented Integer
    classroom_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    student_id = models.ForeignKey(All_Users, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the request was made

    def __str__(self):
        return f"Request by {self.student_id.username} for {self.classroom_id.name}"

# Announcements model
class Announcements(models.Model):
    announcement_id = models.AutoField(primary_key=True)  # Primary Key, Auto-incremented Integer
    classroom_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    faculty_id = models.ForeignKey(All_Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the announcement was posted

    def __str__(self):
        return self.title

# Resources model
class Resources(models.Model):
    resource_id = models.AutoField(primary_key=True)  # Primary Key, Auto-incremented Integer
    classroom_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    faculty_id = models.ForeignKey(All_Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file_url = models.CharField(max_length=1024)
    description = models.TextField(blank=True, null=True)  # Optional resource description
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the resource was uploaded

    def __str__(self):
        return self.title

# Notices model
class Notices(models.Model):
    notice_id = models.AutoField(primary_key=True)  # Primary Key, Auto-incremented Integer
    admin_id = models.ForeignKey(All_Users, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    posted_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the notice was posted

    def __str__(self):
        return self.title

# Attendance model
class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]
    attendance_id = models.AutoField(primary_key=True)  # Primary Key, Auto-incremented Integer
    classroom_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    student_id = models.ForeignKey(All_Users, on_delete=models.CASCADE)
    session_date = models.DateField()
    midday_status = models.CharField(max_length=10, choices=ATTENDANCE_STATUS)  # Attendance status for the session

    def __str__(self):
        return f"{self.student_id.username} - {self.session_date}"
