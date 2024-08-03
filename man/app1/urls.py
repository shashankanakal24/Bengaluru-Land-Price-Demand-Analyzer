from django.urls import path
from .views import loginorsignup, home, prediction, predict , Analysis ,landingpage ,aboutus 

urlpatterns = [
    path('', landingpage , name='index'),
    path('loginorsignup/', loginorsignup, name='loginorsignup'),
    path('login', home , name='home'),
    path('aboutus/', aboutus, name='aboutus'),
    #  path('signup', loginorsignup, name='signup'),
    # path('login', loginorsignup, name='login'),
    #  path('signup', home, name='home'),
    path('prediction/', prediction, name='prediction'),
    path('predict/', predict, name='predict'),
    # path('prediction/', prediction, name='prediction'),
    path('Analysis/', Analysis, name='Analysis'),
    
]

