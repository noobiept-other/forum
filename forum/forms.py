from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class PostForm( forms.Form ):

    text = forms.CharField( widget= forms.Textarea )


class PrivateMessageForm( forms.Form ):

    title = forms.CharField( max_length= 100 )
    content = forms.CharField( max_length= 500, widget= forms.Textarea )


class NewThreadForm( forms.Form ):

    title = forms.CharField( max_length= 100 )
    content = forms.CharField( max_length= 500, widget= forms.Textarea )


class MyUserCreationForm( UserCreationForm ):

    email = forms.EmailField( required= True )

    class Meta:

        model = User
        fields = ( 'username', 'email', 'password1', 'password2' )


    def clean_email( self ):

        """
            Check if there's already an user with that email
        """

        email = self.cleaned_data[ 'email' ]

        try:
            User.objects.get( email= email )

        except User.DoesNotExist:

            return email

        else:
            raise ValidationError( 'An account with that email already exists.' )



    def save( self, commit= True ):

        user = super( MyUserCreationForm, self ).save( commit= False )
        user.email = self.cleaned_data[ 'email' ]

        if commit:
            user.save()

        return user


