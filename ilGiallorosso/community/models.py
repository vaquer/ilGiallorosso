from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserGiallorosso(models.Model):
    user = models.ForeignKey(User, verbose_name='Usuario Django')
    birth_date = models.DateField('Fecha de Nacimiento')
    pic = models.ImageField('Imagen', upload_to='users/pics', blank=True, null=True)
    social_media_user = models.BooleanField('Registrado por RedSocial', default=False)
    active = models.BooleanField('Activo', default=False)

    def __unicode__(self):
        return u'{0} - {1} {2}'.format(self.user.username, self.user.first_name, self.user.last_name)

    def get_full_name(self):
        return u'{0} {1}'.format(self.user.first_name, self.user.last_name)

    @models.permalink
    def get_absolute_url(self):
        return ('user_view', (), {'user_name': self.user.username})

    class Meta:
        verbose_name = 'Usuario Giallorosso'
        verbose_name_plural = 'Usuarios Giallorossos'
