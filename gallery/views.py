from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from adminuses.models import Photo, Video
from django.db import models
from .models import Contact, Help_form, Notices, MembershipApplication
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

def membership_form(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        dob_str = request.POST.get('dob', '')
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        national_id_type = request.POST.get('national_id_type', '').strip()
        national_id_number = request.POST.get('national_id_number', '').strip()
        temporary_address = request.POST.get('temporary_address', '').strip()
        mother_tongue = request.POST.get('mother_tongue', '').strip()
        caste = request.POST.get('caste', '').strip()
        pradesh = request.POST.get('pradesh', '').strip()
        district = request.POST.get('district', '').strip()
        local_body_type = request.POST.get('local_body_type', '').strip()
        ward_number = request.POST.get('ward_number', '')
        passport_photo = request.FILES.get('passport_photo')
        citizenship_front = request.FILES.get('citizenship_front')
        citizenship_back = request.FILES.get('citizenship_back')
        payment_screenshot = request.FILES.get('payment_screenshot')

        errors = []
        if not first_name:
            errors.append('पहिलो नाम आवश्यक छ।')
        if not last_name:
            errors.append('थर आवश्यक छ।')
        if not dob_str:
            errors.append('जन्म मिति आवश्यक छ।')
        if not email:
            errors.append('इमेल आवश्यक छ।')
        if not mobile:
            errors.append('मोबाइल नं. आवश्यक छ।')
        if not national_id_type:
            errors.append('राष्ट्रिय परिचय पत्र नं आवश्यक छ।')
        if not national_id_number:
            errors.append('नागरिकता नं आवश्यक छ।')
        if not mother_tongue:
            errors.append('भाषा छान्नुहोस्।')
        if not caste:
            errors.append('पेशा छान्नुहोस्।')
        if not pradesh:
            errors.append('प्रदेश छान्नुहोस्।')
        if not district:
            errors.append('जिल्ला छान्नुहोस्।')
        if not local_body_type:
            errors.append('गाउँपालिका/नगरपालिका छान्नुहोस्।')
        if not ward_number:
            errors.append('वडा नं. आवश्यक छ।')
        elif not ward_number.isdigit() or int(ward_number) < 1:
            errors.append('वडा नं. वैध हुनुपर्छ।')
        if not passport_photo:
            errors.append('पासपोर्ट आकारको तस्बिर आवश्यक छ।')
        if not citizenship_front:
            errors.append('नागरिकता अगाडि पृष्ठ आवश्यक छ।')
        if not citizenship_back:
            errors.append('नागरिकता पछाडि पृष्ठ आवश्यक छ।')
        if not payment_screenshot:
            errors.append('भुक्तानी स्क्रिनसट आवश्यक छ।')

        if errors:
            for msg in errors:
                messages.error(request, msg)
            return render(request, 'sadasya_form.html')

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'जन्म मिति ठीक ढाँचामा हुनुपर्छ।')
            return render(request, 'sadasya_form.html')

        try:
            ward_int = int(ward_number)
        except ValueError:
            ward_int = 1

        try:
            MembershipApplication.objects.create(
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                dob=dob,
                email=email,
                mobile=mobile,
                national_id_type=national_id_type,
                national_id_number=national_id_number,
                temporary_address=temporary_address,
                mother_tongue=mother_tongue,
                caste=caste,
                pradesh=pradesh,
                district=district,
                local_body_type=local_body_type,
                ward_number=ward_int,
                passport_photo=passport_photo,
                citizenship_front=citizenship_front,
                citizenship_back=citizenship_back,
                payment_screenshot=payment_screenshot,
            )
            messages.success(request, "धन्यवाद! तपाईंको सदस्यता आवेदन सफलतापूर्वक पेश भयो।")
            return redirect('membership_form')
        except Exception as e:
            messages.error(request, f"आवेदन सेव गर्दा त्रुटि: {str(e)}")
            return render(request, 'sadasya_form.html')

    return render(request, 'sadasya_form.html')



