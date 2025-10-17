from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminuses.models import Photo, Video
from django.db import models
from .models import Contact, Help_form, Notices
from .form import DocumentForm
from django.core.paginator import Paginator


# Create your views here.
def photo_gallery(request):
    
    query = request.GET.get('q', '')
    if query:
        photos = Photo.objects.filter(
            models.Q(title__icontains=query) | models.Q(description__icontains=query)
        )
    else:
        photos = Photo.objects.all().order_by('-date')
    return render(request, 'photo_gallery.html', {  'photos': photos})



def video_gallery(request):
    
    query = request.GET.get('q', '')
    if query:
        videos = Video.objects.filter(
            models.Q(title__icontains=query) | models.Q(description__icontains=query)
        )
    else:
        videos = Video.objects.all().order_by('-date')
    return render(request, 'video_gallery.html', {  'videos': videos})

def contact_us(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        # save to database
        Contact.objects.create(name=name, email=email, message=message)

        # optional success message
        messages.success(request, "सन्देश सफलतापूर्वक पठाइयो। धन्यवाद!")
        return redirect("contact_us")  # redirect to the same page

    return render(request, "samparka.html")

def get_message(request):
    query = request.GET.get('q')
    if query:
        all_messages = Contact.objects.filter(
            models.Q(name__icontains=query) | models.Q(email__icontains=query)
        ).order_by('-id')
    else:
        all_messages = Contact.objects.all().order_by('-id')

    paginator = Paginator(all_messages, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'messages.html', {'page_messages': page_obj})


def delete_message(request, message_id):
    message = get_object_or_404(Contact, id=message_id)

    if request.method == 'POST':
        message.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect('messages')

    return render(request, 'confirm_delete.html', {
        'object': message,
        'type': 'message',
        'cancel_url_name': 'messages'
    })


def help(request):
    if request.method == "POST":
        full_name = request.POST.get('first_name')
        address = request.POST.get('address')
        contact_number = request.POST.get('number')
        amount = request.POST.get('amount') or request.POST.get('custom_amount')
        currency = request.POST.get('currency')
        donation_purpose = request.POST.get('donation_purpose')
        voucher_image = request.FILES.get('voucher_image')

        Help_form.objects.create(
            full_name=full_name,
            address=address,
            contact_number=contact_number,
            amount=amount,
            currency=currency,
            donation_purpose=donation_purpose,
            voucher_image=voucher_image
        )

        messages.success(request, "आपको धन्यवाद! तपाईंको सदस्यता आवेदन सफलतापूर्वक पठाइयो।")
        return redirect('help')  # redirect to same page or success page

    return render(request, "sahayog.html")


def help_list(request):
    query = request.GET.get('q')
    if query:
        all_help_forms = Help_form.objects.filter(
            models.Q(full_name__icontains=query) | models.Q(address__icontains=query) | models.Q(contact_number__icontains=query)
        ).order_by('-id')
    else:
        all_help_forms = Help_form.objects.all().order_by('-id')

    paginator = Paginator(all_help_forms, 10) # Show 10 help forms per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'help_list.html', {'page_help_forms': page_obj})


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

def notice_list(request):
    if request.user.is_authenticated:
        notices = Notices.objects.all().order_by('-uploaded_at')
        return render(request, 'notice_list.html', {'notices': notices})
    else:
        return render(request, 'admin_notice_list.html', {'notices': notices})