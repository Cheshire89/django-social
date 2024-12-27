from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model
)
from django.shortcuts import render, get_object_or_404
from django.http import (
    HttpResponse,
    HttpRequest,
    JsonResponse
)
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from .models import (
    Profile,
    Contact
)
from django.contrib.auth.decorators import (
    login_required,
)
from django.views.decorators.http import require_POST

User = get_user_model()

@login_required
def dashboard(request: HttpRequest):
    return render(
        request,
        'account/dashboard.html',
        {
            'section': 'dashboard'
        }
    )


@login_required
def user_edit(request: HttpRequest):
    '''User edit view.'''
    if request.method == 'POST':
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Profile updated successfully'
            )
        else:
            messages.error(
                request,
                'Error updating your profile'
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        'account/edit.html',
        {
            'user_form': user_form,
            'profile_form': profile_form
        }
    )

@login_required
def user_list(request: HttpRequest):
    '''Users list view.'''
    users = User.objects.filter(is_active = True)
    return render(
        request,
        'account/user/list.html',
        {'section': 'people', 'users': users}
    )

@login_required
def user_detail(request: HttpRequest, username: str):
    '''User detail view.'''
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request,
        'account/user/detail.html',
        {'section': 'people', 'user': user}
    )

@require_POST
@login_required
def user_follow(request: HttpRequest):
    '''Follow a user'''
    user_id = request.POST.get('id')
    action = request.POST.get('action')

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status':'error'})

def user_login(request: HttpRequest):
    '''User login view'''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenciated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(
        request,
        'account/login.html',
        {
            'form': form
        }
    )

def user_register(request: HttpRequest):
    '''User registration view.'''
    if request.method == 'POST':
        registration_form = UserRegistrationForm(request.POST)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(
                registration_form.cleaned_data['password']
            )
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(
                request,
                'account/register_done.html',
                {
                    'new_user': new_user
                }
            )
    else:
        user_form = UserRegistrationForm()
    return render(
        request,
        'account/register.html',
        {
            'user_form': user_form
        }
    )


