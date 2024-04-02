from django.shortcuts import render
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from .forms import ForgotMyPassword
from django.http import HttpResponseForbidden , HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordResetConfirmView
import base64
class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
def forgot_my_password(req):
    form = ForgotMyPassword()
    if req.method == 'POST':
        form = ForgotMyPassword(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                user = get_user_model().objects.get(username = username)
            except:
                return HttpResponseRedirect('/'+'accounts/forgot_my_password/')
            token = default_token_generator.make_token(user)
            uidb64 = base64.urlsafe_b64encode(str(user.id).encode()).decode()[0:-2]
            user_email = get_user_model().objects.get(username = user).email
            send_mail('email reset',f'reset link: {req.build_absolute_uri(reverse("password_reset_confirm",kwargs={"uidb64":uidb64,"token":token}))}','sharmindolat@gmail.com',[f'{user_email}'])
            return redirect('password_reset_done')
        else:
            return HttpResponseForbidden()
    return render(req,'registration/forgot_my_password.html',{'form':form})