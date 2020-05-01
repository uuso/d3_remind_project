from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib import auth
from allauth.socialaccount.models import SocialAccount
from . import forms


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['username'] = request.user.username
        soc_acc = SocialAccount.objects.filter(user=request.user)
        if soc_acc.count() > 0:
            context['provider'] = soc_acc.get().provider
            context['url'] = soc_acc.get().extra_data.get('html_url')
            context['data'] = soc_acc.get().extra_data
        else:
            # эти пользователи созданы из-под формы регистрации обычных пользователей в allauth
            # надо отключить
            context['provider'] = ''

    return render(request, template_name="common/index.html", context=context)


class RegisterView(generic.FormView):
    """При регистрации пользователя обычными CBV создадим ему SocialAccount чтобы в его extra_data
    записывать дополнительную информацию.
    """
    form_class = auth.forms.UserCreationForm
    template_name = 'common/user-create.html'
    success_url = reverse_lazy('common:index')

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')

        # создаем для нового пользователя SocialAccount со значениями по-умолчанию
        SocialAccount.objects.create(user_id=auth.models.User.objects.get(username=username).pk).save()
        
        auth.login(self.request, auth.authenticate(username=username, password=raw_password))

        return super(RegisterView, self).form_valid(form)

class UserInfoView(generic.FormView):
    form_class = forms.UserInfoForm
    template_name = 'common/user-info.html'
    success_url = reverse_lazy('common:index')

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        if self.request.user.is_authenticated:
            s_acc = get_object_or_404(SocialAccount.objects.filter(user_id=self.request.user.id))
            s_acc.extra_data.update(form.cleaned_data)
            # s_acc.extra_data = json.dumps(str(s_edata))
            s_acc.save()
            print("User: %s [%d]" % (self.request.user, self.request.user.id))
            print("User's SocialAccount: %s" % SocialAccount.objects.get(user_id=self.request.user.id))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        return context
