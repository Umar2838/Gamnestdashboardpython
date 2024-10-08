
from django.contrib import admin
from django.urls import path
from myapp.views import login,index,venues,new_venue,edit_venue,games,tickets,units,new_headset,new_tablet,statistics,users,support,settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login,name="login"),
    path('index',index,name="index"),
    path('venues',venues,name="venues"),
    path('new_venue',new_venue,name="new_venue"),
    path('edit_venue',edit_venue,name="edit_venue"),
    path('games',games,name="games"),
    path('tickets',tickets,name="tickets"),
    path('units',units,name="units"),
    path('new_headset',new_headset,name="new_headset"),
    path('new_tablet',new_tablet,name="new_tablet"),
    path('statistics',statistics,name="statistics"),
    path('users',users,name="users"),
    path('support',support,name="support"),
    path('settings',settings,name="settings"),


]
