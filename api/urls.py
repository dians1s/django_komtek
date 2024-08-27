from django.urls import path
from .views import refbooks_list, guide_elements, check_element

urlpatterns = [
    path('refbooks/', refbooks_list, name='refbooks_list'),
    path('refbooks/<int:id>/elements/', guide_elements, name='guide_elements'),
    path('refbooks/<int:id>/check_element/',
         check_element, name='check_element')
]
