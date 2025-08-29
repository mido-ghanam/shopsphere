from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta
from django.db import models
import uuid

class Users(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
  user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
  joined_at = models.DateTimeField(auto_now_add=True)
  def __str__(self):
    return self.user.get_full_name()
  class Meta:
    db_table = 'users'
