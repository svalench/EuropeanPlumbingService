import six
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import ValidationError

from EuropeanPlumbingService.settings import DOMAIN, EMAIL_HOST_USER


class EmailSending:
    """
    Класс для отправки сообщений пользователям системы
    """

    def __init__(self):
        self.current_site = DOMAIN
        self.my_email = EMAIL_HOST_USER

    def send_cart_email(self, user, cart):
        data = cart
        self.send_html_email('Заказ', 'email_template/order.html', data, user.email)

    def send_email_registration(self, user):
        """отправка сообщения при авторизации"""
        mail_subject = 'Activate your account.'
        data = {
            'domain': self.current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        self.send_mail('Активация аккаунта', 'email_template/email_activation_template.html', data, user.email)

    def send_email_forgot_password(self, user, password):
        """отправка письма с новым паролем"""
        data = {"newpassword": password, "name": user.first_name, "last_name": user.last_name}
        if (self.send_mail('Восстановления пароля', 'email_template/email_change_pass.html', data, user.email)):
            user.set_password(password)
            user.save()

    def send_mail(self, subject: str, template: str, data: dict, email: str) -> bool:
        """отправка письма пользователю"""
        mail_subject = subject
        message = render_to_string(template, data)
        try:
            send_mail(mail_subject, message, self.my_email, [email])
            return True
        except Exception as e:
            ValidationError({"detail": "Проблема отправки письма. Обратитесь к администратору."})
            return False

    def send_html_email(self, subject: str, template: str, data: dict, email: str) -> bool:

        text_content = 'This is an important message.'
        html_content = render_to_string(template, data)
        msg = EmailMultiAlternatives(subject, text_content, self.my_email, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        msg_to_manager = EmailMultiAlternatives(subject, text_content, self.my_email, [self.my_email])
        msg_to_manager.attach_alternative(html_content, "text/html")
        msg_to_manager.send()


class TokenGenerator(PasswordResetTokenGenerator):
    """
    Класс генерации токена для пользователя при активации аккаунта
    """

    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def activation_accaunt(request, uidb64, token):
    """функция активации аккаунта и перенаправления пользователя в системе"""
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse(
            "Спасибо за активацию Вашего аккаунта. Теперь Вы можете войти в личный кабинет пользователя.")
    else:
        return HttpResponse('Ссылка на активацию не активна!')
