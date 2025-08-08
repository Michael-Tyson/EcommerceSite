from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django.contrib.auth.models import User
from . models import UserProfile
class SignupForm(UserCreationForm):
	email = forms.EmailField(label="",required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address','required':False}))
	first_name = forms.CharField(label="", max_length=100,  required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name','required':False}))
	last_name = forms.CharField(label="", max_length=100 ,required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name','required':False}))

	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password1', 'password2')
		

	def __init__(self, *args, **kwargs):
		super(SignupForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
class UserupdateForm(UserChangeForm):
	password=None
	email = forms.EmailField(label="",required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address','required':False}))
	first_name = forms.CharField(label="", max_length=100,  required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name','required':False}))
	last_name = forms.CharField(label="", max_length=100 ,required=False, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name','required':False}))
	
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email')
    
		
		

	def __init__(self, *args, **kwargs):
		super(UserupdateForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

class UpdatepasswordForm(SetPasswordForm):
	class Meta:
		model=User
		fields=['new_password1','new_password2']
	def __init__(self, *args, **kwargs):
			super(UpdatepasswordForm, self).__init__(*args, **kwargs)

			
			self.fields['new_password1'].widget.attrs['class'] = 'form-control'
			self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
			self.fields['new_password1'].label = ''
			self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

			self.fields['new_password2'].widget.attrs['class'] = 'form-control'
			self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
			self.fields['new_password2'].label = ''
			self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
class UpdateprofileForm(forms.ModelForm):
  
  phone = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter phone number'}),required=False)
  address1  =  forms.CharField(label="" ,widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter address1"}),required=False)
  address2=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter address2"}),required=False)
  city=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter City"}),required=False)
  state=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter state"}),required=False)
  zipcode=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter zipcode"}),required=False)
  country=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':"Enter country"}),required=False)
  class Meta:
			model=UserProfile
			fields=('phone','address1','address2','city','state','zipcode','country',)
		
