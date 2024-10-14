
from django.contrib import admin
from django.urls import path
from myapp.views import login,index,venues,new_venue,edit_venue,games,tickets,units,newheadset,new_tablet,statistics,users,support,supportTicketDetail,settings,logoutbtn

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
    path('newheadset',newheadset,name="newheadset"),
    path('new_tablet',new_tablet,name="new_tablet"),
    path('statistics',statistics,name="statistics"),
    path('users',users,name="users"),
    path('support',support,name="support"),
    path('support-ticket-detail',supportTicketDetail,name="supportTicketDetail"),
    path('settings',settings,name="settings"),
    path('logout',logoutbtn,name='logout')


]
