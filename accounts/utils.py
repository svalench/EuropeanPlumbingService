
import re

from django.contrib.auth.base_user import BaseUserManager


def check_email(email):
    """проверка email  по reg """
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex, email)):
        return True
    else:
        return False

def generate_new_password():
    """генерация пароля для пользователя"""
    return BaseUserManager().make_random_password()
