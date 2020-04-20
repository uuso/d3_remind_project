from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import FormView
from django.http.response import HttpResponseRedirect

from django.contrib import auth

from .models import UserProfile
from .forms import ProfileCreationForm


def index(request):	
	context = {}
	if request.user.is_authenticated:
		context['username'] = request.user.username
		context['age'] = UserProfile.objects.get(user=request.user).age
		
	return render(request, template_name="common/index.html", context=context)


class RegisterView(FormView):
	form_class = auth.forms.UserCreationForm
	template_name = 'common/user-create.html'
	success_url = reverse_lazy('common:profile-create')

	def form_valid(self, form):
		form.save()
		username = form.cleaned_data.get('username')
		raw_password = form.cleaned_data.get('password1')
		
		# login(request, user, backend=None)
		# authenticate(request=None, **credentials)
		auth.login(self.request, auth.authenticate(username=username, password=raw_password))

		return super(RegisterView, self).form_valid(form)


class CreateUserProfileView(FormView):
	form_class = ProfileCreationForm
	template_name = 'common/profile-create.html'
	success_url = reverse_lazy('common:index')

	# dispatch(request, *args, **kwargs)
	# The view part of the view – the method that accepts a request argument 
	#     plus arguments, and returns a HTTP response.
	def dispatch(self, request, *args, **kwargs):
		# if self.request.user.is_anonymous:
		if not self.request.user.is_authenticated:
			return HttpResponseRedirect(reverse_lazy('common:user-login'))
		return super(CreateUserProfileView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		instance = form.save(commit=False) # не отправлять, но создать
		instance.user = self.request.user # добавим поле в форму
		instance.save() # а вот ее уже готовим к отправке
		return super(CreateUserProfileView, self).form_valid(form)
