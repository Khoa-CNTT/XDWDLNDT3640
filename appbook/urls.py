from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # View
    path('', views.view_home, name='view_home'),
    path('login/', views.login, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    # User------------------------------------------------------------------------------------------------------------------
    path('user/home/', views.user_home, name='user_home'),
    path("user/detail/<int:resort_id>/", views.resort_detail, name="resort_detail"),
    
    path("user/checkbook/", views.user_check_booking, name="user_check_booking"),
    path("user/cancel_booking/<str:payment_id>/", views.cancel_user_booking, name="cancel_user_booking"),


    path("api/get_available_rooms/", views.get_available_rooms, name="get_available_rooms"),
    path("user/search_home/", views.search_home, name="search_home"),
    
    path("user/edit/", views.edit_user, name="edit_user"),

    path("user/payment/<int:booking_id>/", views.user_payment, name="user_payment"),
    path("user/cancel_booking/<int:booking_id>/", views.user_cancel_booking, name="user_cancel_booking"),
    path("user/confirm_payment/<int:booking_id>/", views.confirm_payment, name="confirm_payment"),

    path("user/putbook/", views.putbook_view, name="putbook"),

    path("user/danang/", views.user_danang, name="user_danang"),
    path("user/hanoi/", views.user_hanoi, name="user_hanoi"),
    path("user/hcm/", views.user_hcm, name="user_hcm"),

    path("user/notification/", views.user_notification, name="user_notification"),
    path("user/detailresort/<int:manager_id>/", views.user_detail_resort, name="user_detail_resort"),


    path('toggle_favorite/<int:resort_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('user_like/', views.user_like, name='user_like'),



    # User chat
    path("chat/user/<int:manager_id>/", views.user_chat, name="user_chat"),
    path("chat/user/list/", views.user_chat_list, name="user_chat_list"),
    
   

    # Resort ----------------------------------------------------------------------------------------------
    path('resort/home/', views.resort_home, name='resort_home'),
    path('delete/<int:resort_id>/', views.delete_resort, name='delete_resort'),

    path('resort/postroom/', views.postroom, name='post_resort'),
    path('editroom/<int:resort_id>/', views.editroom, name='editroom'),
    path('editresort/', views.edit_resort_manager, name='edit_resort_manager'),
    path("resort/checkbook/", views.check_booking, name="check_booking"),

    path('cancel-booking/<str:payment_id>/', views.cancel_booking, name='cancel_booking'),
    path("resort/confirm_booking/<int:booking_id>/", views.confirm_booking, name="confirm_booking"),
    path("resort/onbook/", views.onbook_view, name="onbook"),

    path("resort/detail/<int:resort_id>/", views.resort_detail_admin, name="resort_detail_admin"),
    

    path("resort/statistical/", views.resort_statistical, name="resort_statistical"),

    
    
    # Quản lý resort chat
    path("chat/resort/list/", views.resort_chat_list, name="resort_chat_list"),
    path("chat/resort/detail/<int:user_id>/", views.resort_chat_detail, name="resort_chat_detail"),
    # gui hinh anh
    path("send_message/<int:receiver_id>/", views.send_message, name="send_message"),

    # chatbot
    path('chatbot/', views.chatbot_response, name='chatbot'),
    
]    