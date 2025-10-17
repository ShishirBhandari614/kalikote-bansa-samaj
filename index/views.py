from django.shortcuts import render
from adminuses.models import Members, Slide
from gallery.models import Notices


def index(request):
    members = Members.objects.all()
    slides = Slide.objects.all()
    notices = Notices.objects.all().order_by('-uploaded_at')[:6]
    context = {
        'members': members,
        'slides': slides,
        'notices': notices,
    }
    return render(request, 'index.html', context)




# Create your views here.
