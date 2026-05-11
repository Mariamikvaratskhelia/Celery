from django.urls import path
from .views import StartEmailTaskView, start_delay_task

urlpatterns = [
    path('delay/', start_delay_task),
    path('email/', StartEmailTaskView.as_view()),
]
