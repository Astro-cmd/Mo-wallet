from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'goals'

router = DefaultRouter()
router.register(r'api/goals', views.SavingsGoalViewSet, basename='goal-api')

urlpatterns = [
    path('', views.goals_list, name='list'),
    path('create/', views.create_goal, name='create'),
    path('<int:goal_id>/edit/', views.edit_goal, name='edit'),
    path('<int:goal_id>/delete/', views.delete_goal, name='delete'),
    path('add-contribution/', views.add_contribution, name='add_contribution'),
    path('', include(router.urls)),
]
