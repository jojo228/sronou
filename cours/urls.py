
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import HttpResponse
from cours.views import coursePage
from cours.views.checkout import checkout, verifyPayment
from cours.views.auth import LoginView, SignupView, signout
from cours.views.homepage import HomePageView
from cours.views.courses import MyCoursesList
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #HomePage urls
    path('', HomePageView.as_view, name='home'),

    #Authentication urls
    path('login', LoginView.as_view() , name = 'login'),
    path('signup', SignupView.as_view() , name = 'signup'),
    path('logout', signout , name = 'logout'),

    #Courses uls
    path('cours/<str:slug>', coursePage, name='details_cours'),
    path('check-out/<str:slug>', checkout , name = 'check-out'),
    path('verify_payment', verifyPayment , name = 'verify_payment'),
    path('my-courses', MyCoursesList.as_view() , name = 'my-courses'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
