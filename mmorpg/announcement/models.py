from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.urls import reverse

CATEGORY = [
    ('TNK', 'Танки'),
    ('HIL', 'Хилы'),
    ('DD', 'ДД'),
    ('MER', 'Торговцы'),
    ('GUD', 'Гилдмастеры'),
    ('QUS', 'Квестгиверы'),
    ('BLC', 'Кузнецы'),
    ('TNR', 'Кожевники'),
    ('PBR', 'Зельевары'),
    ('SPM', 'Мастера заклинаний'),
]

RESPOND_STATUS = [
    ('ACP', 'Принято'),
    ('REJ', 'Отклонено'),
    ('EXP', 'Ожидание'),
]


STATUS_CHOICES = [
    ('ACTIVE', 'Активное'),
    ('INACTIVE', 'Неактивное'),
    ('COMPLETED', 'Завершено'),
]


class Announcement(models.Model):
    header = models.CharField(max_length=255)
    content = HTMLField()
    category = models.CharField(max_length=3, choices=CATEGORY, default='TNK')
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    def get_absolute_url(self):
        return reverse('announcement_detail', args=[str(self.id)])
    
    def __str__(self):
        return self.header
    

class Respond(models.Model):
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=3, choices=RESPOND_STATUS, default='EXP')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)