import random
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import BaseModel
from main.models import Category


class User(AbstractUser, BaseModel):
    followed_categories = models.ManyToManyField(Category, blank=True)
    email = models.EmailField(unique=True, blank=False)
    profile_pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.jpg', null=True, blank=True)
    registration_complete = models.BooleanField(default=False)

    def check_username(self):
        if not self.username :
            i = str(self.id)
            temp_username = f"user-{i.split('-')[4]}"
            while User.objects.filter(username=temp_username):
                temp_username += str(random.randint(0, 9))
            self.username = temp_username

    def check_pass(self):
        if not self.password:
            i = str(self.id)
            temp_pass = f"user-{i.split('-')[4]}"
            while User.objects.filter(password=temp_pass):
                temp_pass += str(random.randint(0, 9))
            self.password = temp_pass

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def own_check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def create_verify_code(self):
        code = ''.join([str(random.randint(0, 100) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            code=code
        )
        return code

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_username()
        self.check_pass()
        self.hashing_password()


class UserConfirmation(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_codes')
    code = models.CharField(max_length=4)
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.expiration_time = datetime.now() + timedelta(minutes=5)

        super(UserConfirmation, self).save(*args, **kwargs)