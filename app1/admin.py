from django.contrib import admin
from .models import All_Users, Classrooms, Classroom_Students, Classroom_Requests, Announcements, Resources, Notices, Attendance

# Register All_Users model
@admin.register(All_Users)
class AllUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name', 'role', 'password', 'date_joined', 'last_login', 'is_active')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('role', 'is_active', 'date_joined')  # Filter by role, active status, and creation date
# Register Classrooms model
@admin.register(Classrooms)
class ClassroomsAdmin(admin.ModelAdmin):
    list_display = ('classroom_id', 'faculty_id', 'name', 'created_at')
    search_fields = ('name', 'faculty_id__username')  # Search by classroom name or faculty username
    list_filter = ('faculty_id',)  # Filter by faculty

# Register Classroom_Students model
@admin.register(Classroom_Students)
class ClassroomStudentsAdmin(admin.ModelAdmin):
    list_display = ('classroom_id', 'student_id', 'joined_at')
    search_fields = ('classroom_id__name', 'student_id__username')
    list_filter = ('classroom_id',)  # Filter by classroom

# Register Classroom_Requests model
@admin.register(Classroom_Requests)
class ClassroomRequestsAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'classroom_id', 'student_id', 'status', 'requested_at')
    search_fields = ('classroom_id__name', 'student_id__username')
    list_filter = ('status', 'requested_at')  # Filter by request status and requested date

# Register Announcements model
@admin.register(Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ('announcement_id', 'classroom_id', 'faculty_id', 'title', 'posted_at')
    search_fields = ('title', 'classroom_id__name', 'faculty_id__username')
    list_filter = ('classroom_id', 'posted_at')  # Filter by classroom and post date

# Register Resources model
@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('resource_id', 'classroom_id', 'faculty_id', 'title', 'uploaded_at')
    search_fields = ('title', 'classroom_id__name', 'faculty_id__username')
    list_filter = ('classroom_id', 'uploaded_at')  # Filter by classroom and upload date

# Register Notices model
@admin.register(Notices)
class NoticesAdmin(admin.ModelAdmin):
    list_display = ('notice_id', 'admin_id', 'title', 'posted_at')
    search_fields = ('title', 'admin_id__username')
    list_filter = ('admin_id', 'posted_at')  # Filter by admin and post date

# Register Attendance model
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('attendance_id', 'classroom_id', 'student_id', 'session_date', 'midday_status')
    search_fields = ('classroom_id__name', 'student_id__username')
    list_filter = ('session_date', 'midday_status')  # Filter by session date or attendance status
