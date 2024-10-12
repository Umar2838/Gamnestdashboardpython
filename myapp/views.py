from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate,login as django_login,logout
from django.contrib.auth.models import User
from .models import Role,Profile
from django.core.paginator import Paginator


def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log in the user
                django_login(request, user)

                # Retrieve the user's role and permissions
                profile = Profile.objects.get(user=user)
                role = profile.role
                permissions = role.get_permissions() if role else {}
                # Respond with success, including the permissions and role information
                return JsonResponse({
                    'success': True, 
                    'message': 'Login successful', 
                    'permissions': permissions, 
                    'role': role.name if role else 'No role'
                })
            
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format'})
    return render(request, 'login.html')


@login_required
def index(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'index.html',{'username':username})

@login_required
def venues(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'venues.html',{'username':username})
@login_required
def new_venue(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'new-venue.html',{'username':username})
@login_required
def edit_venue(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'edit-venue.html',{'username':username})
@login_required
def games(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'games.html',{'username':username})
@login_required
def tickets(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'tickets.html',{'username':username})
@login_required
def units(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'units.html',{'username':username})
@login_required
def new_headset(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'new-headset.html',{'username':username})
@login_required
def new_tablet(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'new-tablet.html',{'username':username})
@login_required
def statistics(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'statistics.html',{'username':username})
# views.py

@login_required
def users(request):
    username = request.user.username

    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Check if it's a role creation request
            if 'roleName' in data:
                # Handle Role Creation
                name = data.get('roleName')
                description = data.get('description')
                permissions = data.get('permissions')

                if not name or not description or not permissions:
                    return JsonResponse({'error': 'Role name, description, and permissions are required.'}, status=400)

                role = Role(name=name, description=description, permissions=permissions)
                role.save()

                return JsonResponse({'message': 'Role created successfully!', 'role_id': role.id}, status=201)

            # Check if it's a user creation request
            elif 'newusername' in data:
                # Handle User Creation
                username = data.get('newusername')
                email = data.get('useremail')
                password = data.get('userpassword')
                role_id = data.get('userrole')

                if not username or not email or not role_id:
                    return JsonResponse({'error': 'All fields are required for user creation.'}, status=400)

                # Check if email already exists
                if User.objects.filter(email=email).exists():
                    return JsonResponse({'error': 'Email already exists.'}, status=400)

                # Create the user
                user = User.objects.create_user(username=username, email=email , password=password)
                user.save()

                # Get the role
                try:
                    role = Role.objects.get(id=role_id)
                except Role.DoesNotExist:
                    return JsonResponse({'error': 'Role not found.'}, status=400)

                # Create the profile and assign the role
                profile = Profile.objects.create(user=user, role=role)

                return JsonResponse({'message': 'User created successfully!'}, status=201)
            else:
                return JsonResponse({'error': 'Invalid data for creating role or user.'}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    roles = Role.objects.all()
    user_list = User.objects.select_related('profile__role').all()
    user_paginator = Paginator(user_list, 5)
    user_page_number = request.GET.get('page',1)
    userpage_obj = user_paginator.get_page(user_page_number)

    role_paginator = Paginator(roles, 5)
    role_page_number = request.GET.get('page',1)
    rolepage_obj = role_paginator.get_page(role_page_number)

    return render(request, 'users.html', {'username': username, 'roles': roles, 'page_obj': userpage_obj,'rolepage_obj':rolepage_obj})

@login_required
def support(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'support.html',{'username':username}) 

@login_required
def settings(request):
    # Initialize variables
    username = request.user.username
    email = request.user.email
    
    errormessage = ""
    successmessage = ""

    # Handle POST request
    if request.method == 'POST':
        user = request.user
        try:
            data = json.loads(request.body)
            new_username = data.get('newusername')
            new_email = data.get('newemail')

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON data'}, status=400)

        # Update username if different and available
        if new_username and new_username != user.username:
            if User.objects.filter(username=new_username).exists():
                errormessage = "This username is already taken."
            else:
                user.username = new_username

        # Update email if different and available
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exists():
                errormessage = "This email is already in use."
            else:
                user.email = new_email

        # If there are no errors, save the user and return success
        if not errormessage:
            user.save()
            successmessage = "Profile updated successfully"
            return JsonResponse({'success': True, 'message': successmessage})

        # Return any error messages if updating failed
        return JsonResponse({'success': False, 'message': errormessage})

    # Render the settings page with user info
    return render(request, 'settings.html', {'username': username, 'email': email, 'errormessage': errormessage, 'successmessage': successmessage})

@login_required
def logoutbtn(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Successfully logged out.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)