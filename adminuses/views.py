from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .form import RoleLoginForm, AddPhotoForm, AddVideoForm, ChangeLogoForm, MemberForm, SlideForm, DocumentForm
from .models import User, Logo,Photo, Video, Slide, Members
from gallery.models import MembershipApplication, Notices
from .permissions import superadmin_required, admin_required 
from django.db import models  
from django.contrib import messages
from django.core.paginator import Paginator


def role_login(request):
    if request.method == "POST":
        form = RoleLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            # Authenticate using email (we assume username = email)
            try:
                user_obj = User.objects.get(email=email, role=role)
            except User.DoesNotExist:
                user_obj = None

            if user_obj:
                user = authenticate(username=user_obj.username, password=password)
                if user:
                    login(request, user)
                    return redirect('dashboard')  # Redirect to your dashboard
            form.add_error(None, "Invalid credentials")
    else:
        form = RoleLoginForm()
    return render(request, "login.html", {"form": form})


@admin_required
def dashboard(request):
    return render(request, "dashboard.html", )




def add_photo(request):
    form = AddPhotoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST': 
        if form.is_valid():
            Photo.objects.create(**form.cleaned_data)
            messages.success(request, 'Photo uploaded successfully!')
            return redirect('add_photo') 
        else:
            # Surface specific field errors to flash messages
            for field_name, field_errors in form.errors.items():
                if field_name == '__all__':
                    continue
                label = form.fields.get(field_name).label if field_name in form.fields else field_name
                for err in field_errors:
                    messages.error(request, f"{label}: {err}")
            for err in form.non_field_errors():
                messages.error(request, err)
            
    return render(request, 'add_photo.html', {'form': form})
 


def add_video(request):
    form = AddVideoForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            Video.objects.create(**form.cleaned_data)
            messages.success(request, 'Video uploaded successfully!')
            return redirect('add_video')
        else:
            # Surface specific field errors to flash messages
            for field_name, field_errors in form.errors.items():
                if field_name == '__all__':
                    continue
                label = form.fields.get(field_name).label if field_name in form.fields else field_name
                for err in field_errors:
                    messages.error(request, f"{label}: {err}")
            for err in form.non_field_errors():
                messages.error(request, err)
    return render(request, 'add_video.html', {'form': form})

def change_password(request):
    from django.contrib.auth import update_session_auth_hash
    from django.contrib import messages
    from .form import ChangePasswordForm
    if not request.user.is_authenticated:
        return redirect('role_login')
    form = ChangePasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password1']
            if not request.user.check_password(old_password):
                form.add_error('old_password', 'Current password is incorrect')
                messages.error(request, 'Current password is incorrect')
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password updated successfully')
                return redirect('dashboard')
        else:
            # Surface specific field errors to flash messages
            for field_name, field_errors in form.errors.items():
                # Skip non_field_errors here; handled below
                if field_name == '__all__':
                    continue
                label = form.fields.get(field_name).label if field_name in form.fields else field_name
                for err in field_errors:
                    messages.error(request, f"{label}: {err}")
            for err in form.non_field_errors():
                messages.error(request, err)
    return render(request, 'change_password.html', {'form': form})

def change_email(request):
    from django.contrib import messages
    from .form import ChangeEmailForm
    if not request.user.is_authenticated:
        return redirect('role_login')
    form = ChangeEmailForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            password = form.cleaned_data.get('current_password')
            if not request.user.check_password(password):
                form.add_error('current_password', 'Current password is incorrect')
                messages.error(request, 'Current password is incorrect')
            else:
                request.user.email = form.cleaned_data['new_email']
                request.user.save()
                messages.success(request, 'Email updated successfully')
                return redirect('dashboard')
        else:
            # Surface specific field errors to flash messages
            for field_name, field_errors in form.errors.items():
                if field_name == '__all__':
                    continue
                label = form.fields.get(field_name).label if field_name in form.fields else field_name
                for err in field_errors:
                    messages.error(request, f"{label}: {err}")
            for err in form.non_field_errors():
                messages.error(request, err)
    return render(request, 'change_email.html', {'form': form})

def logout(request):
    from django.contrib.auth import logout as auth_logout
    auth_logout(request)
    return redirect('role_login')

def manage_photos(request):
    query = request.GET.get('q', '')
    
    if query:
        photo_list = Photo.objects.filter(
            models.Q(title__icontains=query) | models.Q(description__icontains=query)
        ).order_by('-id')
    else:
        photo_list = Photo.objects.all().order_by('-id')

    paginator = Paginator(photo_list, 8)  # Show 6 photos per page
    page_number = request.GET.get('page')
    page_photos = paginator.get_page(page_number)

    return render(request, 'manage_photos.html', {'page_photos': page_photos})



def manage_videos(request):
    query = request.GET.get('q', '')
    
    if query:
        video_list = Video.objects.filter(
            models.Q(title__icontains=query) | models.Q(description__icontains=query)
        ).order_by('-id')
    else:
        video_list = Video.objects.all().order_by('-id')

    paginator = Paginator(video_list, 8)  # Show 6 videos per page
    page_number = request.GET.get('page')
    page_videos = paginator.get_page(page_number)

    return render(request, 'manage_videos.html', {'page_videos': page_videos})



def edit_photo(request, photo_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    try:
        photo = Photo.objects.get(id=photo_id)
    except Photo.DoesNotExist:
        return redirect('manage_photo')
    if request.method == 'POST':
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            photo.title = cleaned['title']
            photo.description = cleaned.get('description', '')
            photo.date = cleaned['date']
            if cleaned.get('image'):
                photo.image = cleaned['image']
            photo.save()
            return redirect('manage_photo')
    else:
        form = AddPhotoForm(initial={
            'title': photo.title,
            'description': photo.description,
            'date': photo.date,
        })
    return render(request, 'edit_photo.html', {'form': form, 'photo': photo})

def edit_video(request, video_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return redirect('manage_video')
    if request.method == 'POST':
        form = AddVideoForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            video.title = cleaned['title']
            video.description = cleaned.get('description', '')
            video.date = cleaned['date']
            if cleaned.get('video_file'):
                video.video_file = cleaned['video_file']
            video.save()
            return redirect('manage_video')
    else:
        form = AddVideoForm(initial={
            'title': video.title,
            'description': video.description,
            'date': video.date,
        })
    return render(request, 'edit_video.html', {'form': form, 'video': video})

def delete_photo(request, photo_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    try:
        photo = Photo.objects.get(id=photo_id)
    except Photo.DoesNotExist:
        return redirect('manage_photo')
    if request.method == 'POST':
        photo.delete()
        return redirect('manage_photo')
    return render(request, 'confirm_delete.html', {'object': photo, 'type': 'photo', 'cancel_url_name': 'manage_photo'})    

def delete_video(request, video_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    try:
        video = Video.objects.get(id=video_id)
    except Video.DoesNotExist:
        return redirect('manage_video')
    if request.method == 'POST':
        video.delete()
        return redirect('manage_video')
    return render(request, 'confirm_delete.html', {'object': video, 'type': 'video', 'cancel_url_name': 'manage_video'})


def change_logo(request):
    if not request.user.is_authenticated:
        return redirect('role_login')

    form = ChangeLogoForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            logo = form.cleaned_data['logo']
            Logo.objects.create(logo=logo)
            messages.success(request, "Logo uploaded successfully!")
            return redirect('change_logo')
        else:
            messages.error(request, "There was an error uploading the logo.")

    return render(request, 'change_logo.html', {'form': form})


def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)  # include request.FILES for images
        if form.is_valid():
            form.save()
            messages.success(request, 'Member added successfully!')
            return redirect('add_members')  # redirect to some page after saving
        else:
            # Surface specific field errors to flash messages
            for field_name, field_errors in form.errors.items():
                if field_name == '__all__':
                    continue
                label = form.fields.get(field_name).label if field_name in form.fields else field_name
                for err in field_errors:
                    messages.error(request, f"{label}: {err}")
            for err in form.non_field_errors():
                messages.error(request, err)
    else:
        form = MemberForm()
    return render(request, 'add_members.html', {'form': form})


def manage_members(request):
    members = Members.objects.all()
    return render(request, 'manage_members.html', {'members': members})


def delete_member(request, member_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    try:
        member = Members.objects.get(id=member_id)
    except Members.DoesNotExist:
        return redirect('manage_members')
    if request.method == 'POST':
        member.delete()
        return redirect('manage_members')
    return render(request, 'confirm_delete.html', {'object': member, 'type': 'member', 'cancel_url_name': 'manage_members'})


def edit_member(request, member_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    try:
        member = Members.objects.get(id=member_id)
    except Members.DoesNotExist:
        return redirect('manage_members')
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            member.name = cleaned['name']
            member.image = cleaned['image']
            member.position = cleaned['position']
            member.phone = cleaned['phone']
            member.save()
            return redirect('manage_members')
    else:
        form = MemberForm(initial={
            'name': member.name,
            'image': member.image,
            'position': member.position,
            'phone': member.phone,
        })
    return render(request, 'edit_member.html', {'form': form, 'member': member})



def add_slide(request):
    if request.method == "POST":
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Slide added successfully!')
            return redirect('add_slides')
        else:
            # Surface specific field errors to flash messages
            for field_name, field_errors in form.errors.items():
                if field_name == '__all__':
                    continue
                label = form.fields.get(field_name).label if field_name in form.fields else field_name
                for err in field_errors:
                    messages.error(request, f"{label}: {err}")
            for err in form.non_field_errors():
                messages.error(request, err)
    else:
        form = SlideForm()

    return render(request, 'add_slides.html', {'form': form})

def edit_slide(request, slide_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    try:
        slide = Slide.objects.get(id=slide_id)
    except Slide.DoesNotExist:
        return redirect('manage_slide')
    if request.method == 'POST':
        form = SlideForm(request.POST, request.FILES)
        if form.is_valid():
            cleaned = form.cleaned_data
            slide.image = cleaned['image']
            slide.caption = cleaned['caption']
            slide.save()
            return redirect('manage_slide')
    else:
        form = SlideForm(initial={
            'image': slide.image,
            'caption': slide.caption,
        })
    return render(request, 'edit_slide.html', {'form': form, 'slide': slide})

def delete_slide(request, slide_id):
    if not request.user.is_authenticated:
        return redirect('role_login')
    
    slide = get_object_or_404(Slide, id=slide_id)

    if request.method == 'POST':
        slide.delete()
        return redirect('manage_slide')
    
    return render(request, 'confirm_delete.html', {
        'object': slide,
        'type': 'slide',
        'cancel_url_name': 'manage_slide',
    })

def manage_slides(request):
    slides = Slide.objects.all()
    return render(request, 'manage_slides.html', {'slides': slides})

def search_slides(request):
    query = request.GET.get('q', '')
    if query:
        slides = Slide.objects.filter(caption__icontains=query)
    else:
        slides = Slide.objects.all()
    return render(request, 'manage_slides.html', {'slides': slides})

def membership_list(request):
    # Order by newest first
    applications = MembershipApplication.objects.order_by('-id')  
    # or if you have a created_at field:
    # applications = MembershipApplication.objects.order_by('-created_at')

    paginator = Paginator(applications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'membership_list.html', {
        'page_obj': page_obj
    })

def membership_detail(request, pk):
    application = get_object_or_404(MembershipApplication, pk=pk)
    return render(request, 'membership_detail.html', {
        'application': application
    })


def notice_post(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice uploaded successfully.")
            return redirect('notice_post')  # Redirect after saving
    else:
        form = DocumentForm()
    return render(request, 'notice_post.html', {'form': form})

def manage_notices(request):
    notice_list = Notices.objects.all().order_by('-id')

    paginator = Paginator(notice_list, 5)  # 5 notices per page
    page_number = request.GET.get('page')
    notices = paginator.get_page(page_number)

    return render(request, 'manage_notice.html', {'notices': notices})
    

def update_notice(request, notice_id):
    notice = get_object_or_404(Notices, id=notice_id)

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice updated successfully.")
            return redirect('manage_notices')
    else:
        form = DocumentForm(instance=notice)

    return render(request, 'edit_notice.html', {'form': form, 'notice': notice})


def delete_notice(request, notice_id):
    notice = get_object_or_404(Notices, id=notice_id)

    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted successfully.")
        return redirect('manage_notices')

    return render(request, 'confirm_delete.html', {
        'object': notice,
        'type': 'notice',
        'cancel_url_name': 'manage_notices'
    })