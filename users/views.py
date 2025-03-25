from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.core.mail import send_mail
from .forms import UserRegisterForm


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_mail(user.email)
        return super().form_valid(form)

    def send_welcome_mail(self, user_email):
        subject = 'Добро пожаловать на наш сайт'
        message = 'Спасибо за регистрацию на сайте'
        from_email = 'anikanovfox5221anikanov@yandex.ru'
        recipient_list = [user_email,]

        send_mail(subject, message, from_email, recipient_list)
