from django.db import models

# Create your models here.
class LocalUser(models.Model):
  name = models.CharField('이름', max_length=24)
  age = models.IntegerField('나이', default=20)

  def __str__(self):
    return self.name