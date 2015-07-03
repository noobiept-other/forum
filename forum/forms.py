from django import forms

from forum.models import Category, SubForum


class PostForm( forms.Form ):

    text = forms.CharField( max_length= 500, widget= forms.Textarea )


class ThreadForm( forms.Form ):

    title = forms.CharField( max_length= 100 )
    content = forms.CharField( max_length= 500, widget= forms.Textarea )


class CategoryForm( forms.Form ):

    category = forms.CharField( max_length= 20 )

    def clean_category(self):

        categoryName = self.cleaned_data[ 'category' ]

        try:
            Category.objects.get( name= categoryName )

        except Category.DoesNotExist:
            return categoryName

        raise forms.ValidationError( "Category already exists." )


class SubForumForm( forms.Form ):

    forumName = forms.CharField( max_length= 100 )

    def clean_forumName(self):

        name = self.cleaned_data[ 'forumName' ]

        try:
            SubForum.objects.get( name= name )

        except SubForum.DoesNotExist:

            return name

        raise forms.ValidationError( "A sub-forum with that name already exists." )

