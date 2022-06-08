from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='회원번호')
    user_id = models.CharField(max_length=30, verbose_name='아이디')
    pw = models.CharField(max_length=20, verbose_name='비밀번호')

    class Meta:
        db_table = 'user'
        verbose_name = '회원'
        verbose_name_plural = '회원들'
    
    def __str__(self):
        return f'{self.id} : {self.user_id}'