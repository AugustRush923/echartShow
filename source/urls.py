from django.urls import path
from .views import SingleView, AllView

urlpatterns = [
    path('', AllView.as_view(), name='all'),
    path('<int:hscode>/<int:year>/', SingleView.as_view(), name='single'),

]
