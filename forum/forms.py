from django import forms
from django.utils.html import strip_tags

from forum.models import Category, SubForum


class CategoryForm( forms.Form ):

    category = forms.CharField( max_length= 50 )

    def clean_category(self):
        categoryName = strip_tags( self.cleaned_data[ 'category' ] )

        try:
            Category.objects.get( name= categoryName )

        except Category.DoesNotExist:
            return categoryName

        raise forms.ValidationError( "Category already exists." )


class SubForumForm( forms.Form ):

    forumName = forms.CharField( max_length= 50 )

    def clean_forumName(self):
        name = strip_tags( self.cleaned_data[ 'forumName' ] )

        try:
            SubForum.objects.get( name= name )

        except SubForum.DoesNotExist:

            return name

        raise forms.ValidationError( "A sub-forum with that name already exists." )


class ThreadForm( forms.Form ):

    title = forms.CharField( max_length= 50 )
    content = forms.CharField( max_length= 1000, widget= forms.Textarea )

    def clean_title(self):
        return strip_tags( self.cleaned_data[ 'title' ] )

    def clean_content(self):
        return strip_tags( self.cleaned_data[ 'content' ] )




class PostForm( forms.Form ):

    text = forms.CharField( max_length= 1000, widget= forms.Textarea )

    def clean_text(self):
        return strip_tags( self.cleaned_data[ 'text' ] )





