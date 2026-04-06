from django.urls import path
from .views import home, generate_pdf_view

urlpatterns = [
    path("", home, name="home"),
    path("pdf-course/", generate_pdf_view, name="generate_pdf"),
]