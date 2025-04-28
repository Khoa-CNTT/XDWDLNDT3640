import string
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
import random
from django.db.models import Sum
from datetime import timedelta
from django.db.models import Count
from datetime import datetime
from decimal import Decimal

# Form đăng ký người dùng
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


# Hồ sơ người dùng
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('T', 'Trai'),
        ('G', 'Gái'),
        ('B', 'Chưa Xác Định'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    is_manager = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# Phân loại resort
class Classify(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Nhà quản lý resort
class ResortManager(models.Model):
    ADDRESS_CHOICES = [
        ("Đà Nẵng", "Đà Nẵng"),
        ("Hà Nội", "Hà Nội"),
        ("HCM", "TP Hồ Chí Minh")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=50, choices=ADDRESS_CHOICES)  # Chuyển thành lựa chọn cố định
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)  # Thêm trường mã QR

    def __str__(self):
        return f"QL Resort: {self.name}"

class ResortManagerImage(models.Model):
    manager = models.ForeignKey(ResortManager, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='manager_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ảnh cho: {self.manager.name}"


# Resort
class Resort(models.Model):
    manager = models.ForeignKey(ResortManager, on_delete=models.CASCADE, related_name='resorts')
    name = models.CharField(max_length=100)
    description = models.TextField()
    max_rooms = models.PositiveIntegerField(default=1)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.JSONField(default=dict)  # Lưu số phòng theo từng ngày
    room_type_capacity = models.PositiveIntegerField(default=2)  # Số người mỗi phòng có thể chứa
    is_hidden = models.BooleanField(default=False)  # Thêm trường để ẩn resort
    liked_users = models.ManyToManyField(User, blank=True, related_name="liked_resorts")  # Danh sách người dùng yêu thích

    def __str__(self):
        return self.name

    def update_available_rooms(self, start_date, end_date, num_rooms):
        """ Cập nhật số phòng còn lại khi đặt hoặc hủy phòng """
        if not isinstance(self.available_rooms, dict):
            self.available_rooms = {}  # Khởi tạo nếu chưa có

        for i in range((end_date - start_date).days + 1):
            date_key = str(start_date + timedelta(days=i))
            if date_key not in self.available_rooms:
                self.available_rooms[date_key] = self.max_rooms  # Khởi tạo số phòng
            self.available_rooms[date_key] = max(0, self.available_rooms[date_key] - num_rooms)  # Đảm bảo số phòng không âm

        self.save()


    def get_available_rooms(self, start_date, end_date):
        """ Trả về số phòng trống trong khoảng thời gian """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

        min_rooms = self.max_rooms
        for i in range((end_date - start_date).days + 1):
            date_key = str(start_date + timedelta(days=i))
            if date_key in self.available_rooms:
                min_rooms = min(min_rooms, self.available_rooms[date_key])

        return min_rooms

    def get_average_rating(self):
        """ Trả về điểm đánh giá trung bình """
        ratings = self.ratings.all()
        if ratings.exists():
            return round(ratings.aggregate(models.Avg("score"))["score__avg"], 2)  # Tính trung bình, làm tròn 2 chữ số
        return "Chưa có đánh giá"

# Ảnh của resort
class ResortImage(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='resort_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ảnh cho: {self.resort.name}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name="ratings")
    score = models.IntegerField(choices=[(1, "1 sao"), (2, "2 sao"), (3, "3 sao"), (4, "4 sao"), (5, "5 sao")])  # Chỉ từ 1 đến 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "resort")  # Mỗi người dùng chỉ có thể đánh giá một lần

    def __str__(self):
        return f"{self.user.username} - {self.resort.name}: {self.score} sao"

 

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    num_rooms = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_id = models.CharField(max_length=15, unique=True, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_confirmed = models.BooleanField(default=False)  # Trạng thái xác nhận

    def __str__(self):
        return f"Booking for {self.resort.name} by {self.user.username}"

    def save(self, *args, **kwargs):
        # Tạo ID thanh toán ngẫu nhiên bắt đầu bằng "PAY" cộng với số ngẫu nhiên
        if not self.payment_id:
            self.payment_id = "PAY" + ''.join(random.choices(string.digits, k=11))
        
        # Sử dụng mã QR của ResortManager (không tạo mã QR mới)
        if not self.qr_code and self.resort.manager.qr_code:
            self.qr_code = self.resort.manager.qr_code

        super().save(*args, **kwargs)

class Bookroom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField() 
    num_rooms = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    id_room = models.CharField(max_length=15, unique=True, blank=True, null=True)  # ID đặt phòng
    created_at = models.DateTimeField(auto_now_add=True)

    total_rooms_booked = models.PositiveIntegerField(default=0)  # Tổng số phòng đã đặt theo ngày
    total_income_generated = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.0'))  # Tổng doanh thu theo ngày

    def save(self, *args, **kwargs):
        if not self.id_room:
            self.id_room = "ROOM" + "".join(random.choices(string.digits, k=11))  # Khởi tạo ID
        
        # Cập nhật thống kê
        self.total_rooms_booked = self.num_rooms
        self.total_income_generated = self.total_price

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bookroom for {self.resort.name} by {self.user.username}"




class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies")  # Bình luận gốc

    def __str__(self):
        return f"Comment by {self.user.username} on {self.resort.name}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Thông báo cho {self.user.username}: {self.message}"




class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    resort = models.ForeignKey("Resort", on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class MessageImage(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="images")
    image_chat = models.ImageField(upload_to="chat_images/")


