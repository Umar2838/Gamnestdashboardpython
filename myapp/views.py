from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate,login as django_login,logout
from django.contrib.auth.models import User
from .models import Role,Profile,Venues,Tickets,Headset,Tablet
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TicketSerializer
from rest_framework import generics


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


def index(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'index.html',{'username':username})

def venues(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            try:
                venueData = json.loads(request.body)
                # Handle Role Creation
                name = venueData.get('name')
                phone = venueData.get('phone')
                email = venueData.get('email')
                location = venueData.get('location')
                hours = venueData.get('hours')
                locationdefine = venueData.get('locationdefine')

                if not name or not phone or not email or not location or not hours or not locationdefine:
                    return JsonResponse({'error': 'Venue name, phone,emial,loaction and hours are required.'}, status=400)

                venue = Venues(name=name, phone = phone, email = email, location = location , hours = hours , locationdefine = locationdefine)
                venue.save()

                return JsonResponse({'message': 'Venue created successfully!', 'role_id': venue.id} ,status=200)
            except Venues.DoesNotExist:
                    return JsonResponse({'error': 'Venue not found.'}, status=400)
            
        venues = Venues.objects.all().order_by('id')
        venue_paginator = Paginator(venues, 10)
        venue_page_number = request.GET.get('page',1)
        venuepage_obj = venue_paginator.get_page(venue_page_number)   
    return render(request,'venues.html',{'username':username,'venues':venues,'venuepage_obj':venuepage_obj})
def new_venue(request):
    if request.user.is_authenticated:
        username = request.user.username
    return render(request,'new-venue.html',{'username':username})
def edit_venue(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'edit-venue.html',{'username':username})
def games(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'games.html',{'username':username})
def tickets(request):
    if request.user.is_authenticated:
        username = request.user.username
        if request.method == 'POST':
            try:
                ticketData = json.loads(request.body)
                # Handle Role Creation
                name = ticketData.get('name')
                description = ticketData.get('description')
                type = ticketData.get('type')
                duration = ticketData.get('duration')
                price = ticketData.get('price')

                if not name or not description or not type or not duration or not price:
                    return JsonResponse({'error': 'Ticket name, description,type,duration and price are required.'}, status=400)

                ticket = Tickets(name=name, description = description, type = type, duration = duration, price = price)
                ticket.save()

                return JsonResponse({'message': 'Tickets created successfully!', 'ticket_id': ticket.id} ,status=200)
            except Tickets.DoesNotExist:
                    return JsonResponse({'error': 'Tickets not found.'}, status=400)
            
        tickets = Tickets.objects.all().order_by('id')
        tickets_paginator = Paginator(tickets, 10)
        tickets_page_number = request.GET.get('page',1)
        ticketspage_obj = tickets_paginator.get_page(tickets_page_number)   
    return render(request,'tickets.html',{'username':username,'tickets':tickets,'ticketspage_obj':ticketspage_obj})

class TicketspurchaseView(generics.ListAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketSerializer
    
def getTickets(request):
    tickets = Tickets.objects.all()
    serializer = TicketSerializer(tickets,many=True)
    return Response(serializer.data)

def units(request):
    if request.user.is_authenticated:
        username = request.user.username  
        headsets = Headset.objects.all().order_by('id')
        headsets_paginator = Paginator(headsets, 10)
        headsets_page_number = request.GET.get('page',1)
        headsetspage_obj = headsets_paginator.get_page(headsets_page_number)   

        tablets = Tablet.objects.all().order_by('id')
        tablets_paginator = Paginator(tablets, 10)
        tablets_page_number = request.GET.get('page',1)
        tabletspage_obj = tablets_paginator.get_page(tablets_page_number)   
    return render(request,'units.html',{'username':username,'headsets':headsets,'headsetspage_obj':headsetspage_obj,'tablets':tablets,'tabletspage_obj':tabletspage_obj})

def newheadset(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            modelNo = data.get('modelNo')  
            serialNo = data.get('serialNo')  
            barcodeNo = data.get('barcodeNo')  
            assignedVenue = data.get('assignedVenue')

            # Ensure all fields are filled
            if not name or not modelNo or not serialNo or not barcodeNo or not assignedVenue:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Fetch assigned venue from the database
            try:
                assignedVenue = Venues.objects.get(id=assignedVenue)
            except Venues.DoesNotExist:
                return JsonResponse({'error': 'Assigned Venue not found.'}, status=404)

            # Create new Headset (make sure to assign the foreign key field `venue`)
            headsets = Headset(
                name=name,
                modelNo=modelNo,
                serialNo=serialNo,
                barcodeNo=int(barcodeNo),
                venue=assignedVenue 
            )
            headsets.save()

            return JsonResponse({'message': 'Headset created successfully!', 'headset_id': headsets.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    venues = Venues.objects.all()
    return render(request, 'new-headset.html', {'username': request.user.username, 'venues': venues})

def new_tablet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            name = data.get('name')
            modelNo = data.get('modelNo')  
            serialNo = data.get('serialNo')  
            barcodeNo = data.get('barcodeNo')  
            assignedVenue = data.get('assignedVenue')

            # Ensure all fields are filled
            if not name or not modelNo or not serialNo or not barcodeNo or not assignedVenue:
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Fetch assigned venue from the database
            try:
                assignedVenue = Venues.objects.get(id=assignedVenue)
            except Venues.DoesNotExist:
                return JsonResponse({'error': 'Assigned Venue not found.'}, status=404)
            tablets = Tablet(
                name=name,
                modelNo=modelNo,
                serialNo=serialNo,
                barcodeNo=int(barcodeNo),
                venue=assignedVenue 
            )
            tablets.save()

            return JsonResponse({'message': 'Tablet created successfully!', 'tablet_id': tablets.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

    venues = Venues.objects.all()
    return render(request, 'new-tablet.html', {'username': request.user.username, 'venues': venues})

def statistics(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'statistics.html',{'username':username})
# views.py


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

    user_list = User.objects.select_related('profile__role').all().order_by('id')
    user_paginator = Paginator(user_list, 10)
    user_page_number = request.GET.get('page',1)
    userpage_obj = user_paginator.get_page(user_page_number)

    roles = Role.objects.all().order_by('id')
    role_paginator = Paginator(roles, 10)
    role_page_number = request.GET.get('page',1)
    rolepage_obj = role_paginator.get_page(role_page_number)

    return render(request, 'users.html', {'username': username, 'roles': roles, 'page_obj': userpage_obj,'rolepage_obj':rolepage_obj})

def support(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = None    
    return render(request,'support.html',{'username':username}) 

from django.http import JsonResponse
from django.shortcuts import render
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # Optional if CSRF token isn't needed
import json


def supportTicketDetail(request):
    return render(request, 'support-ticket-detail.html')

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

def logoutbtn(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Successfully logged out.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)