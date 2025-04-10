from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    # path('workouts/', lambda request: render(request, 'workouts.html'), name='workouts'),
    path('diet/', views.diet_view, name='diet'),
    path('budget/', views.budget_view, name='budget'),
    # path('login/', lambda request: render(request, 'login.html'), name='login'),
    # path('signup/', lambda request: render(request, 'signup.html'), name='signup'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('workouts/', views.workouts_view, name='workouts'),
    path('profile_setup/', views.profile_setup_view, name='profile_setup'),  # Add this line
    # path('diet_plan/', views.diet_plan_view, name='diet_plan'),
   path('diet/', views.diet_view, name='diet'),
]
