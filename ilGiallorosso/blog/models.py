from watson import register as watson_register
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from community.models import UserGiallorosso


# Create your models here.
class Entry(models.Model):
    title = models.CharField('Titulo', max_length=300, db_index=True)
    slug = models.SlugField('Slug', max_length=350, db_index=True)
    date = models.DateField('Fecha de Publicacion', default=timezone.now(), db_index=True)
    text =  models.TextField('Texto', blank=True, null=True)
    about = models.CharField('Encabezado', max_length=300, blank=True, null=True)
    photo = models.ImageField('Imagen', upload_to="blog/entries/photos", blank=True, null=True)
    tags = models.ManyToManyField('Tag', db_index=True, verbose_name='Tags', blank=True, null=True)
    category = models.ForeignKey('Category', verbose_name='Categoria', blank=True, null=True)
    author = models.ForeignKey('Author', verbose_name='Autor', blank=True, null=True)
    top = models.BooleanField('Titular', default=False)
    active = models.BooleanField('Publicar', default=False)

    @models.permalink
    def get_absolute_url(self):
        return ('single_entry', (), {'year': self.date.year, 'month': self.date.month, 'slug': self.slug})

    def get_related_entries(self):
        entries = Entry.objects.filter(tags__in=self.tags.all()).exclude(slug=self.slug).order_by('date')
        if not len(entries):
            return None

        return entries[:5]

    def get_recent_entries(self):
        entries = Entry.objects.filter(active=True).exclude(slug=self.slug).order_by('date')
        if not len(entries):
            return None

        return entries[:3]

    def get_tags(self):
        return self.tags.all()

    def get_top_tags(self):
        tags_top = []

        try:
            tags_top = [tag.tag for tag in self.get_tags()[:5]]
        except:
            return ''

        return ', '.join(tags_top)

    def save(self):
        if not self.id:
            slug = slugify(self.title)
            count = Entry.objects.filter(slug=slug).count()
            if count > 0:
                slug = "{0}-{1}".format(slug, str(count))
            self.slug =  slug

        super(Entry, self).save()

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
watson_register(Entry)

class Tag(models.Model):
    tag = models.CharField('Tag', max_length=150, unique=True)
    slug = models.SlugField('Slug', max_length=200, unique=True)

    def __unicode__(self):
        return u'{0}'.format(self.tag)

    @models.permalink
    def get_absolute_url(self):
        return ('single_tag', (), {'slug': self.slug})

    def save(self):
        if not self.id:
            slug = slugify(self.tag)
            count = Tag.objects.filter(slug=slug).count()
            if count > 0:
                slug = "{0}-{1}".format(slug, str(count))
            self.slug =  slug

        super(Tag, self).save()

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class Category(models.Model):
    name = models.CharField("Categoria", max_length=150, unique=True)
    slug = models.SlugField("Slug", max_length=200, db_index=True)
    short_description = models.CharField('Descripcion', max_length=500)
    pic = models.ImageField("Imagen", upload_to="blog/categories/pics", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.name)

    @models.permalink
    def get_absolute_url(self):
        return ('single_category', (), {'slug', self.slug})

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Author(models.Model):
    user = models.ForeignKey(UserGiallorosso, verbose_name='Usuario editor', db_index=True)
    short_about = models.TextField("Biografia")
    photo = models.ImageField('Foto de editor', upload_to="blog/authors/photos", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user.get_full_name())

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
