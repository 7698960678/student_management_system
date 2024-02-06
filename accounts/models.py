from django.db import models
from django.contrib.auth.models import (
	AbstractUser, BaseUserManager
)
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		"""
		creates a user with given email and password
		"""
		if not email:
			raise ValueError('user must have a email address')

		user = self.model(
			email=self.normalize_email(email), 
		)

		user.set_password(password)
		user.save(self._db)
		return user
	def create_staffuser(self, email, password):
		"""
		creates a user with staff permissions
		"""
		user = self.create_user(
			email=email,
			password=password
		)
		# user.staff = True
		user.is_staff =True
		user.save(using=self._db)
		return user
	def create_superuser(self, email, password):
		"""
		creates a superuser with email and password
		"""
		user = self.create_user(
			email=email,
			password=password
		)
		# user.staff = True
		# user.admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save(using=self._db)
		return user
	def create_admin(self, email, password):
		"""
		creates a user with staff permissions
		"""
		user = self.create_user(
			email=email,
			password=password
		)
		# user.staff = True
		user.is_staff = True
		user.is_admin = True
		user.is_teacher = False
		user.is_student = False
		user.save(using=self._db)
		return user
	def create_teacher(self, email, password):
		"""
		creates a user with staff permissions
		"""
		user = self.create_user(
			email=email,
			password=password
		)
		# user.staff = True
		user.is_staff = True
		user.is_admin = False
		user.is_teacher = True
		user.is_student = False
		user.save(using=self._db)
		return user
	def create_student(self, email, password):
		"""
		creates a user with staff permissions
		"""
		user = self.create_user(
			email=email,
			password=password
		)
		# user.staff = True
		user.is_staff = True
		user.is_admin = False
		user.is_teacher = False
		user.is_student = True
		user.save(using=self._db)
		return user
		
class User(AbstractUser):
	username= models.CharField(max_length=255)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField("Contact Number",max_length=10, unique=True, validators=[phone_regex],null=True, blank=True)
	email = models.EmailField(
		verbose_name='Email address',
		max_length=100,
		unique=True
	)

	# active = models.BooleanField(default=True)
	# staff = models.BooleanField(default=True)  # <- admin user, not super user
	# admin = models.BooleanField(default=True)  # <- super user
	
	is_admin = models.BooleanField(default=False)
	is_teacher = models.BooleanField(default=False)
	is_student = models.BooleanField(default = False)
	# notice the absence of password field
	# that is built in

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []  # <- email and password are required by default
	'''
	def get_full_name(self):
		return str(self.email)
	
	def has_perm(self, perm, obj=None):
		"""Does the user has a specific permission"""
		return True

	def has_module_perms(self, app_lable):
		"""Does the user has permission to view a specific app"""
		return True
	
	@property
	def is_staff(self):
		"""Is the user a staff member"""
		return self.staff

	@property
	def is_admin(self):
		"""Is the user a admin member"""
		return self.admin

	@property
	def is_active(self):
		"""Is the user active"""
		return self.active
	'''
	# hook the user manager to objects
	objects = UserManager()
	class Meta:
		verbose_name_plural = "1. User"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Admin(models.Model):
	token = models.ForeignKey(Token,on_delete=models.SET_NULL, null=True)
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	class Meta:
		verbose_name_plural = "2. Admin"
	def __str__(self) :
		return f'{self.user} : {self.token}'

class Teacher(models.Model):
	token = models.ForeignKey(Token,on_delete=models.SET_NULL, null=True)
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	admin = models.ForeignKey(Admin, on_delete = models.CASCADE,null=True, default="" )
	class Meta:
		verbose_name_plural = "3. Teacher"
	def __str__(self) :
		return f'{self.user} : {self.token}'

class Student(models.Model):
	token = models.ForeignKey(Token,on_delete=models.SET_NULL, null=True)
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE,null=True, default="" )
	class Meta:
		verbose_name_plural = "4. Student"
	def __str__(self) :
		return f'{self.user} : {self.token}'