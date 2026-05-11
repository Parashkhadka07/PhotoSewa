from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from accounts.models import MyUser, Profile

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    
    class Meta:
        model = MyUser
        fields = ["full_name", "email", "user_role"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ["email", "password", "is_active", "is_admin", "user_role"]

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "full_name", "is_admin", "is_staff", "user_role"]
    list_filter = ["is_admin", "is_staff", "is_active"]
    
    fieldsets = [
        (None, {"fields": ["full_name", "email", "password", "user_role"]}),
        ("Permissions", {"fields": ["is_active", "is_admin", "is_staff", "groups", "user_permissions"]}),
    ]
    
    add_fieldsets = [
        (None, {
            "classes": ["wide"],
            "fields": ["email", "full_name", "user_role", "password1", "password2"],
        }),
    ]
    
    search_fields = ["email", "full_name"]
    ordering = ["email"]
    filter_horizontal = ["groups", "user_permissions"]

admin.site.register(MyUser, UserAdmin)

#this is just for the valadition of the rejected reason
class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("kyc_verified")
        reason = cleaned_data.get("rejection_reason")

        # Validation: If status is 'rejected', 'rejection_reason' is required
        if status == "rejected" and not reason:
            self.add_error('rejection_reason', "Please explain why this profile was rejected.")
        
        return cleaned_data

class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm#this is where upper class is used to validate it
    list_display = ["full_name", "user", "kyc_verified"]
    list_filter = [ "kyc_verified"]
    
    fieldsets=[("Basic informations",{"fields":["profile_photo","full_name", "user","date_of_birth","permanent_address",]}),
               ("KYC informations",{"fields":["document_type","document_number","issued_district","citizenship_front","citizenship_back"]}),
                ("Details",{"fields":["specialization","Phone","price_charge","currency","no_of_cameras","location","intrest"]}),
               ("KYC Decision",{"fields":["kyc_verified","rejection_reason"]}),
              ]
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "kyc_verified" in form.base_fields:
            form.base_fields["kyc_verified"].choices = [
                ("verified", "Verified"),
                ("rejected", "Rejected"),
            ]
            
        return form

    def get_readonly_fields(self ,request,obj=None):
        readonly_fields=("full_name", "user","date_of_birth","document_type","document_number","issued_district","permanent_address","created_at","specialization","profile_photo","citizenship_front","citizenship_back","Phone","price_charge","currency","no_of_cameras","location","intrest")

        if request.user.is_superuser:
            return ()
        return readonly_fields

        

    def get_queryset(self, request):
    # Get the original queryset
        qs = super().get_queryset(request)
    
    # 1. Admins (Superusers) always see everything
        if request.user.is_superuser:
            return qs

    # 2. Check if the user is currently looking at the "List" of profiles
    # We use 'resolver_match' to see if the current URL is the 'changelist'
        is_list_view = request.resolver_match and request.resolver_match.url_name.endswith('_changelist')

        if is_list_view:
        # Only filter the list if they haven't clicked a specific filter in the sidebar
            if "kyc_verified__exact" not in request.GET:
                return qs.filter(kyc_verified="in_review")

    # 3. If we are NOT in the list view (meaning we are inside a profile), 
    # return the full queryset so the page doesn't crash with a "Deleted" error.
        return qs


    
admin.site.register(Profile, ProfileAdmin)