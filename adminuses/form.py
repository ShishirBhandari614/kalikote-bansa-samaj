from django import forms
from .models import Members, Slide
from gallery.models import Notices


class RoleLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    role = forms.ChoiceField(
        choices=[
            ('superadmin', 'Super Admin'),
            ('subadmin', 'Sub Admin'),
        ]
    )

# Form for adding a photo
class AddPhotoForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Photo Title'}))
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}), required=False)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

# Form for adding a video
class AddVideoForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Video Title'}))
    video_file = forms.FileField()
    description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description'}), required=False)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


# Profile/account forms
class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'New Email'}))
    confirm_email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Confirm New Email'}))
    current_password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Current Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prevent email autofill and ensure password uses current-password
        self.fields['new_email'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['confirm_email'].widget.attrs.update({'autocomplete': 'off'})
        self.fields['current_password'].widget.attrs.update({'autocomplete': 'off'})

    def clean(self):
        cleaned = super().clean()
        new_email = cleaned.get('new_email')
        confirm_email = cleaned.get('confirm_email')
        if new_email and confirm_email and new_email != confirm_email:
            self.add_error('confirm_email', 'Emails do not match')
        return cleaned


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Current Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'placeholder': 'Confirm New Password'}))

    def clean(self):
        cleaned = super().clean()
        new1 = cleaned.get('new_password1')
        new2 = cleaned.get('new_password2')
        if new1 and new2 and new1 != new2:
            self.add_error('new_password2', 'Passwords do not match')
        return cleaned

class ChangeLogoForm(forms.Form):
    logo = forms.ImageField()

    def clean(self):
        cleaned = super().clean()
        logo = cleaned.get('logo')

class MemberForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['name', 'image', 'position', 'phone']


class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            # 'caption': forms.TextInput(attrs={
            #     'class': 'form-input',
            #     'placeholder': 'Enter Caption'
            # }),
        }
        labels = {
            'image': 'Upload Image',
            'caption': 'Enter Caption',
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Notices
        fields = ['name', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Notice Name'}),
            'file': forms.FileInput(attrs={'placeholder': 'Upload Notice File'}),
        }
        labels = {
            'name': 'Notice Name',
            'file': 'Upload Notice File',
        }