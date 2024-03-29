from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User

class RegisterForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_email(self):
		"""check if the email already exists"""
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise ValidationError('email already exists')
		return email

	def clean_password2(self):
		"""check if the both passwords match"""
		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('passwords don\'t match')
		return password2

class AdminUserCreationForm(forms.ModelForm):
	"""form for creating new admin users with all fields and repeated password field"""
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email',)

	def clean_email(self):
		"""check if the email already exists"""
		email = self.cleaned_data.get('email')
		qs = User.objects.filter(email=email)
		if qs.exists():
			raise ValidationError('email already exists')
		return email

	def clean_password2(self):
		"""check if the both passwords match"""
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError('passwords don\'t match')
		return password2

	def save(self, commit=False):
		"""save the password in hashed format"""
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class UserAdminChangeForm(forms.ModelForm):
	"""a form for updating users including all the fields but hashed password field"""
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User 
		fields = ('email', 'password')
		
	def clean_password(self):
		return self.initial["password"]