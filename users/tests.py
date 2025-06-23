import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from users.models import User

