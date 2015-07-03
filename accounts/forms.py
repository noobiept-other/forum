from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class FixUserCreationForm( UserCreationForm ):
    """
        The django form has the User hard-coded (so doesn't work with custom user models)

        Just change the parts where the User is hard-coded
    """
    def clean_username(self):

        userModel = get_user_model()

        username = self.cleaned_data[ "username" ]

        try:
            userModel.objects.get( username= username )

        except userModel.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class MyUserCreationForm( FixUserCreationForm ):

    email = forms.EmailField( required= True )

    class Meta:

        model = get_user_model()
        fields = ( 'username', 'email', 'password1', 'password2' )

    def clean_email( self ):

        """
            Check if there's already an user with that email
        """

        userModel = get_user_model()
        email = self.cleaned_data[ 'email' ]

        try:
            userModel.objects.get( email= email )

        except userModel.DoesNotExist:

            return email

        else:
            raise ValidationError( 'An account with that email already exists.' )



    def save( self, commit= True ):

        user = super( MyUserCreationForm, self ).save( commit= False )
        user.email = self.cleaned_data[ 'email' ]

        if commit:
            user.save()

        return user


class PrivateMessageForm( forms.Form ):

    title = forms.CharField( max_length= 100 )
    content = forms.CharField( max_length= 500, widget= forms.Textarea )
