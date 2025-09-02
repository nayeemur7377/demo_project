from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

# Registration
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        phone = request.POST.get('phone')
        role = request.POST['role']
        profile_pic = request.FILES.get('profile_pic')
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            phone=phone,
            role=role,
            password=password1,
            profile_pic=profile_pic
        )
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')
    return render(request, "register.html")



# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('note_list')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, "login.html")



#Logout
def logout_view(request):
    logout(request)
    return redirect('login')







#change password
@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not request.user.check_password(current_password):
            messages.error(request, "Current password is incorrect.")
            return redirect("change_password")

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect("change_password")

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)  # keep user logged in
        messages.success(request, "Password updated successfully.")
        return redirect("note_list")

    return render(request, "change_password.html")


