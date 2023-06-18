# Importing the path module from Django's urls library.
from django.urls import path


from .views import  convert_lead_to_student_view

# Creating URL patterns for our themes.
urlpatterns = [



    path('convert-lead-to-student/', convert_lead_to_student_view,
         name='convert-lead-to-student'),
]
