from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.views.generic import FormView
from .models import UserProfile
from .forms import ProfileCreationForm


class RegisterView(FormView):
    form_class = UserCreationForm

    template_name = 'common/register.html'
    success_url = reverse_lazy('common:profile-create')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_pass = form.cleaned_data.get('password')        
        login(self.request, authenticate(username=username, password=raw_pass))
        return super(RegisterView, self).form_valid(form)


class CreateUserProfile(FormView):
    form_class = ProfileCreationForm
    template_name = 'common/profile-create.html'
    success_url = reverse_lazy('common:index')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect(reverse_lazy('common:login'))
        return super(CreateUserProfile, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super(CreateUserProfile, self).form_valid(form)


def index(request):
    context = dict()
    if request.user.is_authenticated:
        context["username"] = request.user.username
        context['age'] = UserProfile.objects.get(user=request.user).age

    return render(request, "common/index.html", context)


def loginv(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            print("valid")
            return HttpResponseRedirect(reverse_lazy('common:index'))
        print("invalid")
        context = {'form': form}
    else:
        print("get")
        context = {'form': AuthenticationForm()}
    return render(request, 'common/login.html', context)


def logoutv(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse_lazy('common:index'))
