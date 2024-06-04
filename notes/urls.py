from django.urls import path
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.login_page,name="login"),
    path('home/',views.home,name="home"),
    path('create-note/',views.createNotes,name="createNotes"),
    path('display-notes/',views.displayNotes,name="displayNotes"),
    path('test/', TemplateView.as_view(template_name='notes/test.html'), name='test'),
    path('update-notes/',views.updateNotes,name="updateNotes"),
    path('change-notes/',views.changeNotes,name="changeNotes"),
]