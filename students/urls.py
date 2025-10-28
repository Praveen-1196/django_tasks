from django.urls import path
from . import views

urlpatterns=[
    path('student/',views.student_list),
    path('students/create/',views.student_create),
    path('students/<int:pk>/update/',views.student_update),
    path('students/<int:pk>/delete/',views.student_delete)
]