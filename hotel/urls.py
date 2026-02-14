from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/add/', views.RoomCreateView.as_view(), name='room_add'),
    path('rooms/edit/<int:pk>/', views.RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/delete/<int:pk>/', views.RoomDeleteView.as_view(), name='room_delete'),
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/add/', views.BookingCreateView.as_view(), name='booking_add'),
    path('bookings/edit/<int:pk>/', views.BookingUpdateView.as_view(), name='booking_edit'),
    path('bookings/delete/<int:pk>/', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/add/', views.HotelCreateView.as_view(), name='hotel_add'),
    path('hotels/edit/<int:pk>/', views.HotelUpdateView.as_view(), name='hotel_edit'),
    path('hotels/delete/<int:pk>/', views.HotelDeleteView.as_view(), name='hotel_delete'),
]
