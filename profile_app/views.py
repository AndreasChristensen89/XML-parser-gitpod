
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from allauth.account.views import PasswordChangeView, PasswordResetView
from django.views.generic.edit import UpdateView
from django.contrib import messages
from django.views import generic
from .models import Profile
from .forms import UserForm, ProfileForm
from django.http import HttpResponseRedirect


@login_required
def profile(request):
    """
    A view to return the profile page
    Premium membership in context in order to provide link in template,
    in case admin deletes and create a new => new id for product
    """
    user_profile = get_object_or_404(Profile, user=request.user)

    template = 'profile_app/profiles.html'
    context = {
        'profile': user_profile,
    }

    return render(request, template, context)


class UpdateUser(SuccessMessageMixin, generic.UpdateView):
    """
    View to update user profile
    """
    form_class = UserForm
    template_name = 'profile_app/update_user.html'
    success_message = 'Profile updated successfully!'
    success_url = '/profiles'

    def get_object(self):
        return self.request.user


class UpdateProfileView(UpdateView):
    """
    User can update comment here
    """
    model = Profile
    fields = ['experimentalist_uid', 'laboratory_uid']
    template_name_suffix = '_update_profile'
    success_url = '/profiles'
