from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
           
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=100,default="USER") 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    ROLE_CHOICES = [
        ("photographer", "Photographer"),
        ("client", "Client"),
    ]
    
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    


class Profile(models.Model):
    class KYC_STATUS(models.TextChoices):
        NOT_VERIFIED=("not_varified","Not varified")
        IN_review=("in_review","In review")
        VERIFIED=("varified","Varified")
        REJECTED=("rejected","Rejected")



    user=models.OneToOneField(MyUser,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=60,null=True)
    date_of_birth=models.DateField(null=True)
    document_type=models.CharField(max_length=60,null=True)
    document_number=models.CharField(max_length=25,null=True)
    issued_district=models.CharField(max_length=30,null=True)
    permanent_address=models.CharField(max_length=100,null=True)
    created_at=models.DateField(auto_now_add=True,null=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)

    #documents
    profile_photo=models.ImageField(upload_to="profile_pictures",null=True,blank=True)
    citizenship_front=models.ImageField(upload_to="citizenship",null=True,blank=True)
    citizenship_back=models.ImageField(upload_to="citizenship",null=True,blank=True)

    #verification
    kyc_verified=models.CharField(choices=KYC_STATUS,default=KYC_STATUS.NOT_VERIFIED)

    #rejection reason
    rejection_reason=models.TextField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.email}'s profile"