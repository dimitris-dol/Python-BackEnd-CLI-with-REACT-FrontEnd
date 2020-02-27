from django.urls import include, path
from rest_framework import routers
from api import views
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

#router = routers.DefaultRouter()
#router.register(r'users',views.UserViewSet)

urlpatterns = [
    #path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    path('emergy/api/users/',views.user_list),
    path('energy/api/users/<int:pk>/',views.user_detail),
    #lists
    path('energy/api/ActualTotalLoad/',views.actualtotalload_list),
    path('energy/api/AggregatedGenerationPerType/',views.aggregatedgenerationpertype_list),


    path('energy/api/ActualTotalLoad/<str:areaname>/<str:resolutioncode>/<str:date>/<str:info>/',views.actual),
    #path('api/actualtotalloads/<str:areaname>/<str:resolutioncode>/<int:year>/<int:month>/<str:format>/',views.actualtotalload_detail1),
    #path('api/actualtotalloads/<str:areaname>/<str:resolutioncode>/<int:year>/<str:format',views.actualtotalload_detail),

    path('energy/api/import',views.upload),

    path('energy/api/AggregatedGenerationPerType/<str:areaname>/<str:productiontype>/<str:resolutioncode>/<str:date>/<str:info>/',views.aggre),
    #path('api/aggregatedgenerationpertypes/<str:areaname>/<str:productiontype>/<str:resolutioncode>/<int:year>/<int:month>/',views.aggregatedgenerationpertype_detail1),
    #path('api/aggregatedgenerationpertypes/<str:areaname>/<str:productiontype>/<str:resolutioncode>/<int:year>/',views.aggregatedgenerationpertype_detail),

    path('energy/api/DayAheadTotalLoadForecast/<str:areaname>/<str:resolutioncode>/<str:date>/<str:info>/',views.dayahead),
    #path('api/dayaheadtotalloadforecast/<str:areaname>/<str:resolutioncode>/<int:year>/<int:month>/',views.dayaheadtotalloadforecast_detail1),
    #path('api/dayaheadtotalloadforecast/<str:areaname>/<str:resolutioncode>/<int:year>/',views.dayaheadtotalloadforecast_detail),

    path('energy/api/ActualvsForecast/<str:areaname>/<str:resolutioncode>/<str:date>/<str:info>/',views.actualvs),
    #path('api/actualvsforecast/<str:areaname>/<str:resolutioncode>/<int:year>/<int:month>/',views.actualvsforecast_detail1),
    #path('api/actualvsforecast/<str:areaname>/<str:resolutioncode>/<int:year>/',views.actualvsforecast_detail),

    path('energy/api/HealthCheck',views.process_request),

    path('energy/api/Admin/users/<str:username>/',views.usss),

    #path('api/Login/',  LoginView.as_view(), name='login'),
    path('energy/api/Login/',  TemplateView.as_view(template_name = 'registration/login.html'),name="login"),
    #path('api/Login/',auth_views.logout, name='logout'),
    #path('energy/api/Login/',admin.site.urls),
    path('urlencoded',views.Login.as_view()),
    path('energy/api/Logout', views.Logout.as_view(),name='logout'),
    path('energy/api/Reset',views.reset),
    path('energy/api/Admin/newuser',views.newuser.as_view(),name='newuser'),
    path('energy/api/Admin/moduser',views.moduser.as_view(),name='moduser')

]
