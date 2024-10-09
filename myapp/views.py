from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate,login as django_login
from django.contrib.auth.models import User
from .models import Role

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
                return JsonResponse({'success': True, 'message': 'Login successful'})
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
@login_required
def users(request):
    username = request.user.username
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse the incoming JSON data

            name = data.get('roleName')
            description = data.get('description')
            permissions = data.get('permissions')  # Permissions should be in JSON format

            # Check if all required fields are present
            if not name or not description or not permissions:
                return JsonResponse({'error': 'Role name, description, and permissions are required.'}, status=400)

            # Create a new Role instance
            role = Role(
                name=name,
                description=description,
                permissions=permissions  # Directly assign permissions here
            )
            role.save()  # Save the role to the database

            return JsonResponse({'message': 'Role created successfully!', 'role_id': role.id}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Catch any unexpected errors

    return render(request, 'users.html', {'username': username})

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


