from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='заголовок')
    content = models.TextField(verbose_name='текст')
    preview = models.ImageField(upload_to='blog/preview/', verbose_name='изображение', **NULLABLE)
    views_count = models.IntegerField(default=0, verbose_name='количетсво просмотров')
    public_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
