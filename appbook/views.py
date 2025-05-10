from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum 
from appbook.forms import ResortManagerForm
from .models import *
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_GET
from datetime import datetime, timedelta , date 
import uuid
from django.contrib.auth import update_session_auth_hash
from django.utils.dateparse import parse_date
import random
import string
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# Trang chủ khi chưa đăng nhập
def view_home(request):
    return render(request, 'view/home.html')

# Đăng ký
def registerUser(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
        else:
            return render(request, 'view/register.html', {'form': form, 'error': 'Thông tin không hợp lệ'})
    else:
        form = CreateUserForm()
    return render(request, 'view/register.html', {'form': form})


# Đăng nhập
# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             auth_login(request, user)

#             # Rẽ 3 hướng: admin / resort / user
#             if user.is_superuser or user.is_staff:
#                 return redirect('/admin/') #Admin

#             try:
#                 user.resortmanager  # Kiểm tra có liên kết không
#                 return redirect('resort_home')
#             except ObjectDoesNotExist:
#                 return redirect('user_home')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'view/login.html', {'form': form})
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)

            # Kiểm tra nếu User có UserAp
            try:
                user_ap = user.userap  
                return redirect('userap_home')
            except UserAp.DoesNotExist:
                pass  # Nếu không phải UserAp, tiếp tục kiểm tra quyền khác

            # Kiểm tra nếu là admin hệ thống
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')  # Admin Django

            # Kiểm tra nếu là ResortManager
            try: 
                user.resortmanager  
                return redirect('resort_home')
            except ObjectDoesNotExist:
                return redirect('user_home')
    else:
        form = AuthenticationForm()

    return render(request, 'view/login.html', {'form': form})



# Đăng xuất
def logoutUser(request):
    logout(request) 
    return redirect('view_home')

# -------------------------------------------------------------------------------------------------------------------------------------------------------------------
# User
# @login_required
# def user_home(request):
#     # Lấy tất cả các resort
#     resorts = Resort.objects.all()

#     # Truyền resorts vào template
#     return render(request, 'user/home.html', {'resorts': resorts})

@login_required
def user_home(request):
    search_query = request.GET.get("search", "")  # Lấy dữ liệu tìm kiếm từ request
    resorts = Resort.objects.filter(is_hidden=False)  # Lọc các resort hiển thị

    if search_query:
        resorts = resorts.filter(models.Q(manager__name__icontains=search_query) | models.Q(name__icontains=search_query))

    return render(request, "user/home.html", {
        "resorts": resorts,
        "search_query": search_query
    })

# yeu thich
def toggle_favorite(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id)

    if request.user in resort.liked_users.all():
        resort.liked_users.remove(request.user)  # Bỏ yêu thích
        return redirect('user_like')  
    else:
        resort.liked_users.add(request.user)  # Thêm yêu thích
        return redirect('user_home')  

    

def user_like(request):
    favorite_resorts = request.user.liked_resorts.all()
    return render(request, 'user/user_like.html', {'favorite_resorts': favorite_resorts})


# @login_required
# def resort_detail(request, resort_id):
#     resort = get_object_or_404(Resort, id=resort_id)

#     today = timezone.now().date()
#     min_checkin_date = today + timedelta(days=1)
#     min_checkout_date = min_checkin_date + timedelta(days=1)

#     if request.method == "POST":
#         start_date = request.POST.get("start_date")
#         end_date = request.POST.get("end_date")
#         num_rooms = int(request.POST.get("num_rooms"))

#         if not start_date or not end_date or num_rooms < 1:
#             return render(request, "user/detail.html", {"resort": resort, "error": "Vui lòng chọn ngày đến, ngày đi và số phòng hợp lệ!"})

#         start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#         end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#         if start_date < min_checkin_date or end_date <= start_date:
#             return render(request, "user/detail.html", {"resort": resort, "error": "Ngày đến và ngày đi không hợp lệ!"})

#         # **Gọi đúng phương thức**
#         available_rooms = resort.get_available_rooms(start_date, end_date)
#         if num_rooms > available_rooms:
#             return render(request, "user/detail.html", {"resort": resort, "error": "Số phòng vượt quá số lượng có sẵn!"})

#         total_price = num_rooms * (end_date - start_date).days * resort.price_per_night

#         # **Lưu thông tin đặt phòng**
#         payment_id = "PAY" + "".join(random.choices(string.digits, k=11))
#         booking = Booking.objects.create(
#             user=request.user,
#             resort=resort,
#             start_date=start_date,
#             end_date=end_date,
#             num_rooms=num_rooms,
#             total_price=total_price,
#             payment_id=payment_id,
#             qr_code=resort.manager.qr_code
#         )

#         return redirect("user_payment", booking_id=booking.id)

#     return render(request, "user/detail.html", {
#         "resort": resort,
#         "min_checkin_date": min_checkin_date,
#         "min_checkout_date": min_checkout_date
#     })

# @login_required
# def resort_detail(request, resort_id):
#     resort = get_object_or_404(Resort, id=resort_id)
#     comments = resort.comments.filter(parent__isnull=True).order_by("-created_at")  # Chỉ lấy bình luận gốc
#     rating_avg = resort.get_average_rating()
#     user_rating = Rating.objects.filter(user=request.user, resort=resort).first()  # Kiểm tra nếu người dùng đã đánh giá

#     today = timezone.now().date()
#     min_checkin_date = today + timedelta(days=1)
#     min_checkout_date = min_checkin_date + timedelta(days=1)

#     if request.method == "POST":
#         if "submit_rating" in request.POST:
#             score = int(request.POST.get("score"))
#             if user_rating:
#                 user_rating.score = score
#                 user_rating.save()
#                 messages.success(request, "Cập nhật đánh giá thành công!")
#             else:
#                 Rating.objects.create(user=request.user, resort=resort, score=score)
#                 messages.success(request, "Bạn đã đánh giá resort này!")
#             return redirect("resort_detail", resort_id=resort.id)

#         elif "delete_comment" in request.POST:  # Xóa bình luận
#             comment_id = request.POST.get("comment_id")
#             comment = get_object_or_404(Comment, id=comment_id, user=request.user)
#             comment.delete()
#             return redirect("resort_detail", resort_id=resort.id)

#         elif "reply_submit" in request.POST:  # Trả lời bình luận
#             content = request.POST.get("content")
#             parent_id = request.POST.get("parent_id")
#             parent_comment = get_object_or_404(Comment, id=parent_id)
#             Comment.objects.create(user=request.user, resort=resort, content=content, parent=parent_comment)
#             return redirect("resort_detail", resort_id=resort.id)

#         elif "comment_submit" in request.POST:  # Đăng bình luận mới
#             content = request.POST.get("content")
#             Comment.objects.create(user=request.user, resort=resort, content=content)
#             return redirect("resort_detail", resort_id=resort.id)

#         else:  # Xử lý đặt phòng
#             start_date = request.POST.get("start_date")
#             end_date = request.POST.get("end_date")
#             num_rooms = int(request.POST.get("num_rooms"))

#             if not start_date or not end_date or num_rooms < 1:
#                 return render(request, "user/detail.html", {"resort": resort, "comments": comments, "rating_avg": rating_avg, "user_rating": user_rating, "error": "Vui lòng chọn ngày đến, ngày đi và số phòng hợp lệ!"})

#             start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#             end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

#             if start_date < min_checkin_date or end_date <= start_date:
#                 return render(request, "user/detail.html", {"resort": resort, "comments": comments, "rating_avg": rating_avg, "user_rating": user_rating, "error": "Ngày đến và ngày đi không hợp lệ!"})

#             available_rooms = resort.get_available_rooms(start_date, end_date)
#             if num_rooms > available_rooms:
#                 return render(request, "user/detail.html", {"resort": resort, "comments": comments, "rating_avg": rating_avg, "user_rating": user_rating, "error": "Số phòng vượt quá số lượng có sẵn!"})

#             total_price = num_rooms * (end_date - start_date).days * resort.price_per_night

#             payment_id = "PAY" + "".join(random.choices(string.digits, k=11))
#             booking = Booking.objects.create(
#                 user=request.user,
#                 resort=resort,
#                 start_date=start_date,
#                 end_date=end_date,
#                 num_rooms=num_rooms,
#                 total_price=total_price,
#                 payment_id=payment_id,
#                 qr_code=resort.manager.qr_code
#             )

#             return redirect("user_payment", booking_id=booking.id)

#     return render(request, "user/detail.html", {
#         "resort": resort,
#         "comments": comments,  
#         "rating_avg": rating_avg,  # Truyền đánh giá trung bình vào template
#         "user_rating": user_rating,  # Kiểm tra nếu người dùng đã đánh giá
#         "min_checkin_date": min_checkin_date,
#         "min_checkout_date": min_checkout_date
#     })

@login_required
def resort_detail(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id)
    comments = resort.comments.filter(parent__isnull=True).order_by("-created_at")
    rating_avg = resort.get_average_rating()
    user_rating = Rating.objects.filter(user=request.user, resort=resort).first()

    today = timezone.now().date()
    min_checkin_date = today + timedelta(days=1)
    min_checkout_date = min_checkin_date + timedelta(days=1)

    if request.method == "POST":
        if "submit_rating" in request.POST:  # Xử lý đánh giá
            score = request.POST.get("score")
            if score:
                score = int(score)
                if user_rating:
                    user_rating.score = score
                    user_rating.save()
                    messages.success(request, "Cập nhật đánh giá thành công!")
                else:
                    Rating.objects.create(user=request.user, resort=resort, score=score)
                    messages.success(request, "Bạn đã đánh giá resort này!")
            else:
                messages.error(request, "Vui lòng chọn đánh giá hợp lệ!")
            return redirect("resort_detail", resort_id=resort.id)

        elif "delete_comment" in request.POST:  # Xóa bình luận
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            comment.delete()
            messages.success(request, "Bình luận đã được xóa!")
            return redirect("resort_detail", resort_id=resort.id)

        elif "reply_submit" in request.POST:  # Trả lời bình luận
            content = request.POST.get("content")
            parent_id = request.POST.get("parent_id")
            if content and parent_id:
                parent_comment = get_object_or_404(Comment, id=parent_id)
                Comment.objects.create(user=request.user, resort=resort, content=content, parent=parent_comment)
                messages.success(request, "Phản hồi của bạn đã được đăng!")
            else:
                messages.error(request, "Vui lòng nhập nội dung phản hồi hợp lệ!")
            return redirect("resort_detail", resort_id=resort.id)

        elif "comment_submit" in request.POST:  # Đăng bình luận mới
            content = request.POST.get("content")
            if content:
                Comment.objects.create(user=request.user, resort=resort, content=content)
                messages.success(request, "Bình luận của bạn đã được đăng!")
            else:
                messages.error(request, "Vui lòng nhập nội dung bình luận!")
            return redirect("resort_detail", resort_id=resort.id)

        elif "booking_submit" in request.POST:  # Xử lý đặt phòng
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date")
            num_rooms_input = request.POST.get("num_rooms")

            if not start_date or not end_date or not num_rooms_input:
                return render(request, "user/detail.html", {
                    "resort": resort,
                    "comments": comments,
                    "rating_avg": rating_avg,
                    "user_rating": user_rating,
                    "error": "Vui lòng chọn ngày đến, ngày đi và số phòng hợp lệ!"
                })

            try:
                num_rooms = int(num_rooms_input)
            except ValueError:
                return render(request, "user/detail.html", {
                    "resort": resort,
                    "comments": comments,
                    "rating_avg": rating_avg,
                    "user_rating": user_rating,
                    "error": "Số phòng phải là một số hợp lệ!"
                })

            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

            if start_date < min_checkin_date or end_date <= start_date:
                return render(request, "user/detail.html", {
                    "resort": resort,
                    "comments": comments,
                    "rating_avg": rating_avg,
                    "user_rating": user_rating,
                    "error": "Ngày đến và ngày đi không hợp lệ!"
                })

            available_rooms = resort.get_available_rooms(start_date, end_date)
            if num_rooms > available_rooms:
                return render(request, "user/detail.html", {
                    "resort": resort,
                    "comments": comments,
                    "rating_avg": rating_avg,
                    "user_rating": user_rating,
                    "error": "Số phòng vượt quá số lượng có sẵn!"
                })

            total_price = num_rooms * (end_date - start_date).days * resort.price_per_night

            payment_id = "PAY" + "".join(random.choices(string.digits, k=11))
            booking = Booking.objects.create(
                user=request.user,
                resort=resort,
                start_date=start_date,
                end_date=end_date,
                num_rooms=num_rooms,
                total_price=total_price,
                payment_id=payment_id,
                qr_code=resort.manager.qr_code
            )

            return redirect("user_payment", booking_id=booking.id)

    return render(request, "user/detail.html", {
        "resort": resort,
        "comments": comments,  
        "rating_avg": rating_avg,
        "user_rating": user_rating,
        "min_checkin_date": min_checkin_date,
        "min_checkout_date": min_checkout_date
    })





# Hiển thị số phòng còn lại trong detail
@login_required
def get_available_rooms(request):
    resort_id = request.GET.get("resort_id")
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    # Chuyển đổi từ chuỗi sang kiểu datetime.date
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    resort = Resort.objects.get(id=resort_id)
    available_rooms = resort.get_available_rooms(start_date, end_date)  # Lấy số phòng theo ngày

    return JsonResponse({"available_rooms": available_rooms})
# payment
@login_required
def user_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "user/payment.html", {"booking": booking})
# huy payment
@login_required
def user_cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.delete()
        messages.success(request, "Đã hủy đặt phòng thành công!")
        return redirect("user_home")

    return render(request, "user/payment.html", {"booking": booking})

# xac nhan payment
@login_required
def confirm_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.is_confirmed = True  # Đánh dấu đơn đặt phòng đã được xác nhận
        booking.save()
        return redirect("user_home")  # Quay lại trang chính của user

    return render(request, "user/payment.html", {"booking": booking})



@login_required
def putbook_view(request):
    booked_rooms = Bookroom.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "user/putbook.html", {"booked_rooms": booked_rooms})

@login_required
def edit_user(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        if "update_info" in request.POST:  # Cập nhật thông tin cá nhân
            user.username = request.POST.get("username", user.username)
            user.email = request.POST.get("email", user.email)
            user.first_name = request.POST.get("first_name", user.first_name)
            user.last_name = request.POST.get("last_name", user.last_name)

            profile.birth_date = request.POST.get("birth_date", profile.birth_date)
            profile.gender = request.POST.get("gender", profile.gender)

            if "profile_image" in request.FILES:
                profile.profile_image = request.FILES["profile_image"]

            user.save()
            profile.save()
            messages.success(request, "Thông tin cá nhân đã được cập nhật!")
            return redirect("edit_user")

        elif "update_password" in request.POST:  # Thay đổi mật khẩu
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_password = request.POST.get("confirm_password")

            if not user.check_password(old_password):
                messages.error(request, "Mật khẩu cũ không chính xác!")
            elif new_password != confirm_password:
                messages.error(request, "Mật khẩu mới không khớp!")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Đảm bảo user không bị đăng xuất
                messages.success(request, "Mật khẩu đã được cập nhật thành công!")
                return redirect("edit_user")

    return render(request, "user/edit_user.html", {"user": user, "profile": profile})

@login_required
def user_check_booking(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-start_date")  # Hiển thị đơn đặt phòng của người dùng
    return render(request, "user/checkbook.html", {"bookings": bookings})

@login_required
def cancel_user_booking(request, payment_id):
    booking = get_object_or_404(Booking, payment_id=payment_id, user=request.user)  # Kiểm tra nếu đúng user mới hủy
    user = booking.user
    # Lưu thông báo hủy đặt phòng
    Notification.objects.create(user=user, message=f"Lịch đặt phòng tại {booking.resort.name} đã bị hủy.")
    booking.delete()
    return redirect('user_check_booking')

# Đà Nẵng
@login_required
def user_danang(request):
    search_query = request.GET.get("search", "")  # Lấy dữ liệu tìm kiếm từ request
    resorts = Resort.objects.filter(manager__address="Đà Nẵng", is_hidden=False)  # Lọc các resort ở Đà Nẵng

    if search_query:
        resorts = resorts.filter(Q(manager__name__icontains=search_query) | Q(name__icontains=search_query))  # Tìm kiếm theo tên quản lý hoặc tên resort

    return render(request, "user/danang.html", {
        "resorts": resorts,
        "search_query": search_query
    })
# Hà Nội
@login_required
def user_hanoi(request):
    search_query = request.GET.get("search", "")  # Lấy dữ liệu tìm kiếm từ request
    resorts = Resort.objects.filter(manager__address="Hà Nội", is_hidden=False)  # Lọc các resort ở Đà Nẵng

    if search_query:
        resorts = resorts.filter(Q(manager__name__icontains=search_query) | Q(name__icontains=search_query))  # Tìm kiếm theo tên quản lý hoặc tên resort

    return render(request, "user/hanoi.html", {
        "resorts": resorts,
        "search_query": search_query
    })
# HCM
@login_required
def user_hcm(request):
    search_query = request.GET.get("search", "")  # Lấy dữ liệu tìm kiếm từ request
    resorts = Resort.objects.filter(manager__address="HCM", is_hidden=False)  # Lọc các resort ở Đà Nẵng

    if search_query:
        resorts = resorts.filter(Q(manager__name__icontains=search_query) | Q(name__icontains=search_query))  # Tìm kiếm theo tên quản lý hoặc tên resort

    return render(request, "user/HCM.html", {
        "resorts": resorts,
        "search_query": search_query
    })
# Xem ResortManager
@login_required
def user_detail_resort(request, manager_id):
    manager = get_object_or_404(ResortManager, id=manager_id)
    resorts = Resort.objects.filter(manager=manager)

    return render(request, "user/detailresort.html", {"manager": manager, "resorts": resorts})
# -------------------------------------------------------------------------------------------------------------------------------------------------------
# Resort
@login_required
def resort_home(request):
    try:
        resort_manager = ResortManager.objects.get(user=request.user)
        resorts = Resort.objects.filter(manager=resort_manager).prefetch_related('images')
    except ResortManager.DoesNotExist:
        resort_manager = None
        resorts = []

    return render(request, 'resort/home.html', {'resort_manager': resort_manager, 'resorts': resorts})



@login_required
def resort_detail_admin(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id)
    comments = resort.comments.filter(parent__isnull=True).order_by("-created_at")  # Chỉ lấy bình luận gốc

    if request.method == "POST":
        if "delete_comment" in request.POST:  # Xóa bình luận
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            comment.delete()
            return redirect("resort_detail_admin", resort_id=resort.id)

        elif "reply_submit" in request.POST:  # Trả lời bình luận
            content = request.POST.get("content")
            parent_id = request.POST.get("parent_id")
            parent_comment = get_object_or_404(Comment, id=parent_id)
            Comment.objects.create(user=request.user, resort=resort, content=content, parent=parent_comment)
            return redirect("resort_detail_admin", resort_id=resort.id)

        else:  # Đăng bình luận mới
            content = request.POST.get("content")
            Comment.objects.create(user=request.user, resort=resort, content=content)
            return redirect("resort_detail_admin", resort_id=resort.id)

    return render(request, "resort/detail.html", {"resort": resort, "comments": comments})


# xoa bai postpost
@login_required
def delete_resort(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id, manager__user=request.user)

    if request.method == "POST":
        resort.delete()
        messages.success(request, "Đã xoá resort thành công!")
        return redirect("resort_home")

    return render(request, "resort/home.html")


@login_required
def postroom(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price_per_day = Decimal(request.POST['price_per_day'])  # Chuyển đổi dữ liệu
        max_rooms = int(request.POST['max_rooms'])
        room_type_capacity = int(request.POST['room_type_capacity'])
        images = request.FILES.getlist('images')
        is_hidden = 'is_hidden' in request.POST  # Kiểm tra nếu người dùng đã chọn checkbox

        try:
            manager = ResortManager.objects.get(user=request.user)
        except ResortManager.DoesNotExist:
            return render(request, 'resort/postroom.html', {'error': 'Bạn chưa được cấp quyền quản lý resort'})

        # Tạo Resort mới với trạng thái ẩn/hiện
        resort = Resort.objects.create(
            manager=manager,
            name=name,
            description=description,
            price_per_night=price_per_day,
            max_rooms=max_rooms,
            room_type_capacity=room_type_capacity,
            is_hidden=is_hidden  # Lưu trạng thái ẩn/hiện
        )

        # Tải lên tối đa 5 ảnh
        for image in images[:5]:
            ResortImage.objects.create(resort=resort, image=image)

        return redirect('resort_home')

    return render(request, 'resort/postroom.html')

# @login_required
# def postroom(request):
#     if request.method == 'POST':
#         name = request.POST['name']
#         description = request.POST['description']
#         price_per_day = request.POST['price_per_day']
#         max_rooms = int(request.POST['max_rooms'])
#         room_type_capacity = int(request.POST['room_type_capacity'])  # Nhận dữ liệu từ form
#         images = request.FILES.getlist('images')

#         # Kiểm tra quyền quản lý
#         try:
#             manager = ResortManager.objects.get(user=request.user)
#         except ResortManager.DoesNotExist:
#             return render(request, 'resort/postroom.html', {'error': 'Bạn chưa được cấp quyền quản lý resort'})

#         # Tạo Resort mới
#         resort = Resort.objects.create(
#             manager=manager,
#             name=name,
#             description=description,
#             price_per_night=price_per_day,
#             max_rooms=max_rooms,
#             room_type_capacity=room_type_capacity  # Lưu loại phòng
#         )

#         # Tải lên tối đa 5 ảnh
#         for image in images[:5]:  
#             ResortImage.objects.create(resort=resort, image=image)

#         return redirect('resort_home')

#     return render(request, 'resort/postroom.html')




# @login_required
# def editroom(request, resort_id):
#     resort = get_object_or_404(Resort, id=resort_id, manager__user=request.user)

#     if request.method == 'POST':
#         resort.name = request.POST['name']
#         resort.description = request.POST['description']
#         resort.price_per_night = request.POST['price_per_day']
#         resort.max_rooms = int(request.POST['max_rooms'])
#         resort.room_type_capacity = int(request.POST['room_type_capacity'])  # Nhận dữ liệu từ form

#         # Cập nhật hình ảnh
#         images = request.FILES.getlist('images')
#         if images:
#             ResortImage.objects.filter(resort=resort).delete()
#             for image in images[:5]:
#                 ResortImage.objects.create(resort=resort, image=image)

#         resort.save()
#         messages.success(request, "Cập nhật resort thành công!")
#         return redirect("resort_home")

#     return render(request, "resort/editroom.html", {"resort": resort})

@login_required
def editroom(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id, manager__user=request.user)

    if request.method == 'POST':
        resort.name = request.POST['name']
        resort.description = request.POST['description']
        resort.price_per_night = Decimal(request.POST['price_per_day'])
        resort.max_rooms = int(request.POST['max_rooms'])
        resort.room_type_capacity = int(request.POST['room_type_capacity'])
        resort.is_hidden = 'is_hidden' in request.POST  # Lưu trạng thái ẩn/hiện
        # Cập nhật hình ảnh
        images = request.FILES.getlist('images')
        if images:
            ResortImage.objects.filter(resort=resort).delete()
            for image in images[:5]:
                ResortImage.objects.create(resort=resort, image=image)

        resort.save()
        messages.success(request, "Cập nhật resort thành công!")
        return redirect("resort_home")

    return render(request, "resort/editroom.html", {"resort": resort})



# Edit Resort
@login_required
def edit_resort_manager(request):
    resort_manager = get_object_or_404(ResortManager, user=request.user)

    if request.method == 'POST':
        form = ResortManagerForm(request.POST, request.FILES, instance=resort_manager)
        if form.is_valid():
            form.save()

            # Cập nhật hình ảnh của ResortManager
            images = request.FILES.getlist('images')
            if images:
                ResortManagerImage.objects.filter(manager=resort_manager).delete()  # Xóa ảnh cũ
                for image in images[:5]:  
                    ResortManagerImage.objects.create(manager=resort_manager, image=image)

            return redirect('resort_home')  # Chuyển hướng sau khi lưu

    else:
        form = ResortManagerForm(instance=resort_manager)

    return render(request, 'resort/editresort.html', {'form': form, 'resort_manager': resort_manager})






@login_required
def check_booking(request):
    try:
        manager = ResortManager.objects.get(user=request.user)
        confirmed_bookings = Booking.objects.filter(resort__manager=manager, is_confirmed=True)
    except ResortManager.DoesNotExist:
        confirmed_bookings = None

    return render(request, "resort/checkbook.html", {"confirmed_bookings": confirmed_bookings})



@login_required
def cancel_booking(request, payment_id):
    booking = get_object_or_404(Booking, payment_id=payment_id)
    user = booking.user

    # Lưu thông báo hủy đặt phòng
    Notification.objects.create(user=user, message=f"Lịch đặt phòng tại {booking.resort.name} đã bị hủy.")
    
    booking.delete()
    return redirect("check_booking")  # Quản lý vẫn quay về trang đặt phòng



# Quản Lý Đơn Đặt
# @login_required
# def confirm_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id)

#     # Tạo bản ghi mới trong Bookroom
#     bookroom = Bookroom.objects.create(
#         user=booking.user,
#         resort=booking.resort,
#         start_date=booking.start_date,
#         end_date=booking.end_date,
#         num_rooms=booking.num_rooms,
#         total_price=booking.total_price
#     )

#     # Cập nhật số phòng còn lại tại Resort
#     resort = booking.resort
#     resort.update_available_rooms(booking.start_date, booking.end_date, booking.num_rooms)
#     resort.save()

#     # Lưu thông báo xác nhận đặt phòng
#     Notification.objects.create(user=booking.user, message=f"Lịch đặt phòng tại {booking.resort.name} đã được xác nhận!")

#     # Xóa đặt phòng cũ
#     booking.delete()
#     return redirect("check_booking")  # Quản lý quay về trang đặt phòng

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    resort = booking.resort

    # Kiểm tra số phòng có sẵn trong khoảng thời gian đặt
    available_rooms = resort.get_available_rooms(booking.start_date, booking.end_date)

    if available_rooms < booking.num_rooms:
        messages.error(request, "Những ngày này đã hết phòng.")  # Hiển thị thông báo
        return redirect("check_booking")

    # Nếu vẫn còn phòng, tiếp tục xác nhận
    bookroom = Bookroom.objects.create(
        user=booking.user,
        resort=booking.resort,
        start_date=booking.start_date,
        end_date=booking.end_date,
        num_rooms=booking.num_rooms,
        total_price=booking.total_price
    )

    # Cập nhật số phòng còn lại
    resort.update_available_rooms(booking.start_date, booking.end_date, booking.num_rooms)
    resort.save()

    # Gửi thông báo xác nhận
    Notification.objects.create(user=booking.user, message=f"Lịch đặt phòng tại {booking.resort.name} đã được xác nhận!")

    # Xóa đơn đặt cũ
    booking.delete()

    return redirect("check_booking")


# Thông Báo
@login_required
def user_notification(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")  # Hiển thị tất cả thông báo

    return render(request, "user/Notification.html", {"notifications": notifications})


# Thông Tin Vé Đã Xác Nhận
@login_required
def onbook_view(request):
    confirmed_bookings = Bookroom.objects.all()
    return render(request, "resort/onbook.html", {"confirmed_bookings": confirmed_bookings})



@login_required
def resort_statistical(request):
    manager = request.user.resortmanager
    resorts = Resort.objects.filter(manager=manager)

    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("day")

    try:
        year = int(year) if year else None
        month = int(month) if month else None
        day = int(day) if day else None
    except ValueError:
        messages.error(request, "Vui lòng chọn năm, tháng hoặc ngày hợp lệ.")
        return redirect("resort_statistical")

    data = []
    for resort in resorts:
        bookings = Bookroom.objects.filter(resort=resort)

        if year:
            bookings = bookings.filter(start_date__year=year)
        if month:
            bookings = bookings.filter(start_date__month=month)
        if day:
            bookings = bookings.filter(start_date__day=day)

        total_rooms = bookings.aggregate(Sum("total_rooms_booked"))["total_rooms_booked__sum"] or 0
        total_income = bookings.aggregate(Sum("total_income_generated"))["total_income_generated__sum"] or Decimal('0.0')

        data.append({
            "name": resort.name,
            "total_rooms": total_rooms,
            "total_income": total_income
        })

    years = Bookroom.objects.values_list("start_date__year", flat=True).distinct()

    return render(request, "resort/statistical.html", {
        "resorts": data,
        "selected_date": f"{day}/{month}/{year}" if day and month else f"{month}/{year}" if month else f"{year}",
        "years": sorted(years),
        "months": range(1, 13),
        "days": range(1, 32)
    })

@login_required
def tax_report(request):
    manager = request.user.resortmanager
    taxes = Tax.objects.filter(manager=manager)

    return render(request, "resort/tax.html", {"taxes": taxes})

@login_required
def confirm_tax(request, tax_id):
    tax = Tax.objects.get(id=tax_id)
    tax.status = "Đang đợi xác nhận"
    tax.save()
    return JsonResponse({"success": True})

# -----------------------------------------------------------------------------------------------------------------------------
# Chat
# user gui tin nhan
@login_required
def user_chat(request, manager_id):
    manager = get_object_or_404(User, id=manager_id)  # Đảm bảo lấy đúng User, không phải ResortManager
    messages = Message.objects.prefetch_related("images").filter(
        (Q(sender=request.user) & Q(receiver=manager)) | 
        (Q(sender=manager) & Q(receiver=request.user))
    ).order_by("timestamp")

    if request.method == "POST":
        content = request.POST.get("content")
        images = request.FILES.getlist("image_chat")  # Lấy danh sách ảnh từ form
        resort = Resort.objects.filter(manager__user=manager).first()  # Tìm resort liên quan đến quản lý

        if resort:
            message = Message.objects.create(sender=request.user, receiver=manager, resort=resort, content=content)
            for image in images:
                MessageImage.objects.create(message=message, image_chat=image)  # Lưu từng ảnh vào model MessageImage
        else:
            messages.error(request, "Không tìm thấy resort liên kết với quản lý.")
            return redirect("user_chat_list")

        return redirect("user_chat", manager_id=manager.id)

    return render(request, "user/chat.html", {"manager": manager, "messages": messages})


# hien thị cac tin nhan đến của resort
@login_required
def user_chat_list(request):
    user = request.user
    # Lấy danh sách quản lý resort mà user đã từng nhắn tin
    managers = User.objects.filter(id__in=Message.objects.filter(sender=user).values_list("receiver", flat=True)).distinct()
    return render(request, "user/chat_list.html", {"managers": managers})

# hien thị cac tin nhan đến của user
@login_required
def resort_chat_list(request):
    manager = request.user.resortmanager
    users = User.objects.filter(sent_messages__receiver=manager.user).distinct()
    return render(request, "resort/chat_list.html", {"users": users})
# resort gửi tin nhắn
@login_required
def resort_chat_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)
    manager = request.user.resortmanager
    messages = Message.objects.prefetch_related("images").filter(
        (Q(sender=request.user) & Q(receiver=user)) | (Q(sender=user) & Q(receiver=request.user))
    ).order_by("timestamp")

    if request.method == "POST":
        content = request.POST.get("content")
        images = request.FILES.getlist("image_chat")  # Nhận nhiều ảnh từ form
        resort = Resort.objects.filter(manager=manager).first()  # Lấy resort thuộc quản lý

        if resort:
            message = Message.objects.create(sender=request.user, receiver=user, resort=resort, content=content)
            for image in images:
                MessageImage.objects.create(message=message, image_chat=image)
            return redirect("resort_chat_detail", user_id=user.id)

    return render(request, "resort/chat_detail.html", {"messages": messages, "user": user})



# chat img
@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)
    resort = Resort.objects.filter(manager__user=receiver).first()

    if request.method == "POST":
        content = request.POST.get("content")
        images = request.FILES.getlist("image_chat")  # Nhận nhiều ảnh

        message = Message.objects.create(sender=request.user, receiver=receiver, resort=resort, content=content)
        for image in images:
            MessageImage.objects.create(message=message, image_chat=image)

        return redirect("chat_detail", user_id=receiver.id)

    return render(request, "user/chat.html", {"resort": resort})


# ---------------------------------------------------------------------------------------------------------------
# ChatBot
# Khởi tạo chatbot
# Khởi tạo chatbot với dữ liệu SQLite
chatbot = ChatBot(
    "ResortBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///db.sqlite3",
    language="vietnamese"  
)

trainer = ListTrainer(chatbot)

# Huấn luyện bot với dữ liệu tiếng Việt
trainer.train([
    "Xin chào",
    "Chào bạn, tôi có thể giúp gì?",
    "tôi muốn đặt phòng resort",
    "Bạn muốn đặt resort ở đâu?",
    "tôi muốn đặt ở Đà Nẵng",
    "Đà Nẵng có rất nhiều khu Resort hay ho bạn có thể bấm chọn vị trí Đà Nẵng ở đầu trang nó sẽ cung cấp cho bạn những Resort ở Đà Nẵng",
    "cảm ơn bạn",
    "không có gì.chúc bạn 1 ngày tốt lành",
    "Ngày mai là sinh nhật tôi",
    "Chúc bạn ngày mai sinh nhật vui vẻ 🎉🎉",
    "Thế mai t nên đi ăn sn đây",
    "Sinh Nhật của bạn hỏi tôi làm đéo gì?",
    "Thảo xinh không?",
    "đéo..",

])

@csrf_exempt  # Cho phép JavaScript gửi request mà không bị lỗi CSRF
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Đọc dữ liệu JSON
            user_message = data.get("message")
            bot_response = chatbot.get_response(user_message)
            return JsonResponse({"response": str(bot_response)})
        except Exception as e:
            return JsonResponse({"error": f"Lỗi nội bộ: {str(e)}"})
    
    return JsonResponse({"error": "Chỉ hỗ trợ phương thức POST"})

# -ADmin----------------------------------------------------------------------------------------------------------
@login_required
def userap_home(request):
    try:
        user_ap = request.user.userap  # Truy xuất UserAp từ User
    except UserAp.DoesNotExist:
        return redirect('user_home')

    search_query = request.GET.get("search", "")  # Lấy dữ liệu tìm kiếm từ request
    resort_managers = ResortManager.objects.all()

    if search_query:
        resort_managers = resort_managers.filter(name__icontains=search_query)  # Lọc theo tên Quản Lý Resort

    return render(request, "userap/home.html", {
        "user_ap": user_ap,
        "resort_managers": resort_managers,
        "search_query": search_query
    })



@login_required
def userap_home_user(request):
    try:
        user_ap = request.user.userap  # Truy xuất UserAp từ User
    except UserAp.DoesNotExist:
        return redirect('user_home')

    search_query = request.GET.get("search", "")  # Lấy dữ liệu tìm kiếm từ request
    users = User.objects.exclude(userap__isnull=False)

    if search_query:
        users = users.filter(username__icontains=search_query)  # Lọc theo Username

    return render(request, "userap/home_user.html", {
        "user_ap": user_ap,
        "users": users,
        "search_query": search_query
    })


@login_required
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return JsonResponse({"success": True})
    except User.DoesNotExist:
        return JsonResponse({"error": "User không tồn tại"}, status=404)

@login_required
def delete_resort_manager(request, manager_id):
    try:
        manager = ResortManager.objects.get(id=manager_id)
        manager.delete()
        return JsonResponse({"success": True})
    except ResortManager.DoesNotExist:
        return JsonResponse({"error": "ResortManager không tồn tại"}, status=404)
    
@login_required
def detail_resort(request, manager_id):
    manager = get_object_or_404(ResortManager, id=manager_id)
    resorts = Resort.objects.filter(manager=manager)

    if request.method == "POST" and "delete_resort" in request.POST:
        resort_id = request.POST.get("resort_id")
        resort = get_object_or_404(Resort, id=resort_id)
        resort.delete()
        return redirect("detail_resort", manager_id=manager.id)

    return render(request, "userap/detail_resort.html", {
        "manager": manager,
        "resorts": resorts
    })

@login_required
def userap_detail(request, resort_id):
    resort = get_object_or_404(Resort, id=resort_id)
    comments = resort.comments.filter(parent__isnull=True).order_by("-created_at")  # Chỉ lấy bình luận gốc

    if request.method == "POST":
        if "delete_comment" in request.POST:  # Xóa bình luận
            comment_id = request.POST.get("comment_id")
            comment = get_object_or_404(Comment, id=comment_id, user=request.user)
            comment.delete()
            return redirect("userap_detail", resort_id=resort.id)


    return render(request, "userap/userap_detail.html", {"resort": resort, "comments": comments})