from django.db import models


# Create your models here.
class User(models.Model):

    '''yonghu'''

    username = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)
    user_pwd = models.CharField(max_length=256)
    user_email = models.EmailField()
    user_c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['user_c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'
