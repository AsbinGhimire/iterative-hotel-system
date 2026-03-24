from django.urls import path
from . import views

urlpatterns = [
    # --- Main Navigation ---
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # --- Hotel Management ---
    path('hotels/', views.HotelListView.as_view(), name='hotel_list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel_detail'),
    path('hotels/add/', views.HotelCreateView.as_view(), name='hotel_add'),
    path('hotels/edit/<int:pk>/', views.HotelUpdateView.as_view(), name='hotel_edit'),
    path('hotels/delete/<int:pk>/', views.HotelDeleteView.as_view(), name='hotel_delete'),

    # --- Room Management ---
    path('rooms/', views.RoomListView.as_view(), name='room_list'),
    path('rooms/add/', views.RoomCreateView.as_view(), name='room_add'),
    path('rooms/edit/<int:pk>/', views.RoomUpdateView.as_view(), name='room_edit'),
    path('rooms/delete/<int:pk>/', views.RoomDeleteView.as_view(), name='room_delete'),

    # --- Booking & Billing Management ---
    path('bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('bookings/add/', views.BookingCreateView.as_view(), name='booking_add'),
    path('bookings/edit/<int:pk>/', views.BookingUpdateView.as_view(), name='booking_edit'),
    path('bookings/delete/<int:pk>/', views.BookingDeleteView.as_view(), name='booking_delete'),
    path('bookings/status/<int:pk>/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('bookings/<int:pk>/bill/', views.booking_bill, name='booking_bill'),

    # --- User Profile & Account Management ---
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
]
