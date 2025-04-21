from django.shortcuts import render, redirect
from django.contrib import messages
from .models import All_Users, Classroom_Students, Classroom_Requests, Classrooms, Announcements, Notices  # Import additional models
from django.contrib.auth import authenticate, login, logout

def signup(request):
    if request.method == 'POST':
        # Get data from the form
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if email or username already exists
        if All_Users.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use!')
            return redirect('signup')
        
        if All_Users.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken!')
            return redirect('signup')

        # Create a new user with role set as 'student' (password is hashed using set_password)
        user = All_Users.objects.create_user(  # Use create_user instead of create() to properly handle password hashing
            email=email,
            username=username,
            password=password,  # This will be hashed by the set_password method
            first_name=first_name,
            last_name=last_name,
            role='student',  # Default role set to 'student'
        )

        # Log the user in automatically after registration (optional)
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('index')  # Redirect to the login page

    return render(request, 'signup.html')

def index(request):
    if request.user.is_authenticated:
        # Redirect to the appropriate dashboard based on user role
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        elif request.user.role == 'faculty':
            return redirect('faculty_dashboard')
        else:  # Default to student dashboard
            return redirect('student_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username_email')  # Field is still named username_email in the form
        password = request.POST.get('password')

        # Authenticate the user using username and password
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            # User is authenticated, log them in
            login(request, user)
            # Redirect to the appropriate dashboard based on user role
            if user.role == 'admin':
                return redirect('admin_dashboard')
            elif user.role == 'faculty':
                return redirect('faculty_dashboard')
            else:  # Default to student dashboard
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid username or password!')
            return render(request, 'index.html')  # Render index.html with error message

    return render(request, 'index.html')  # Render the login page for GET requests

def home(request):
    return render(request, 'home.html')  # Render the 'home.html' template

def admin_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'admin':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('index')
    notices = Notices.objects.filter(admin_id=request.user)
    return render(request, 'admin_dashboard.html', {'notices': notices})

def faculty_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'faculty':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('index')
    classrooms = Classrooms.objects.filter(faculty_id=request.user)
    announcements = Announcements.objects.filter(faculty_id=request.user)
    return render(request, 'faculty_dashboard.html', {'classrooms': classrooms, 'announcements': announcements})

def student_dashboard(request):
    if not request.user.is_authenticated or request.user.role != 'student':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('index')
    enrolled_classrooms = Classroom_Students.objects.filter(student_id=request.user)
    pending_requests = Classroom_Requests.objects.filter(student_id=request.user, status='pending')
    return render(request, 'student_dashboard.html', {'enrolled_classrooms': enrolled_classrooms, 'pending_requests': pending_requests})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Notices

def notice_board(request, notice_id=None):
    # Handle deletion if notice_id is provided and request method is POST
    if notice_id and request.method == 'POST':
        notice = get_object_or_404(Notices, notice_id=notice_id)
        notice.delete()
        messages.success(request, 'Notice deleted successfully.')
        return redirect('notice_board')
    
    # Retrieve all notices, ordered by posted_at (newest first)
    notices = Notices.objects.all().order_by('-posted_at')
    return render(request, 'notice_board.html', {'notices': notices})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Notices
from django.contrib.auth.decorators import login_required

@login_required
def add_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        # Validate input
        if not title or not content:
            messages.error(request, 'Title and content are required.')
            return render(request, 'add_notice.html')
        
        # Create new notice
        try:
            Notices.objects.create(
                admin_id=request.user,  # Assuming All_Users is linked to the authenticated user
                title=title,
                content=content
            )
            # Instead of redirecting immediately, pass a success flag to the template
            return render(request, 'add_notice.html', {
                'success_message': 'Notice added successfully!'
            })
        except Exception as e:
            messages.error(request, f'Error adding notice: {str(e)}')
            return render(request, 'add_notice.html')
    
    return render(request, 'add_notice.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import All_Users

@login_required
def add_faculty(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to add faculty.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate input
        if not all([first_name, last_name, username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'add_faculty.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'add_faculty.html')
        
        # Check if username or email already exists
        if All_Users.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'add_faculty.html')
        
        if All_Users.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'add_faculty.html')
        
        # Create new faculty user
        try:
            user = All_Users.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='faculty'
            )
            messages.success(request, 'Faculty added successfully.')
            return redirect('faculty_list')
        except Exception as e:
            messages.error(request, f'Error adding faculty: {str(e)}')
            return render(request, 'add_faculty.html')
    
    return render(request, 'add_faculty.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import All_Users

@login_required
def faculty_list(request, user_id=None):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view or manage faculty.')
        return redirect('admin_dashboard')
    
    # Handle deletion if user_id is provided and request method is POST
    if user_id and request.method == 'POST':
        user = get_object_or_404(All_Users, id=user_id, role='faculty')
        user.delete()
        messages.success(request, 'Faculty deleted successfully.')
        return redirect('faculty_list')
    
    # Retrieve all faculty users
    faculty = All_Users.objects.filter(role='faculty').order_by('first_name')
    return render(request, 'faculty_list.html', {'faculty': faculty})

from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

def logout_view(request):
    # Log the user out
    logout(request)
    # Render the logout.html template
    response = render(request, 'logout.html')
    # Delete session cookies (sessionid is the default name for session cookie)
    response.delete_cookie('sessionid')
    # Optionally, delete any other cookies you want to clear (if set by the app)
    # response.delete_cookie('your_cookie_name')
    # Return the response which will clear cookies and render logout.html
    return response