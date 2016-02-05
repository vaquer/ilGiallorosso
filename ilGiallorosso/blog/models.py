from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.core.cache import cache
from community.models import UserGiallorosso
# from watson import register as watson_register


# Create your models here.
class Entry(models.Model):
    title = models.CharField('Titulo', max_length=300, db_index=True)
    slug = models.SlugField('Slug', max_length=350, db_index=True)
    date = models.DateField('Fecha de Publicacion', db_index=True)
    text = models.TextField('Texto', blank=True, null=True)
    about = models.CharField('Encabezado', max_length=300, blank=True, null=True)
    photo = models.ImageField('Imagen', upload_to="blog/entries/photos", blank=True, null=True)
    tags = models.ManyToManyField('Tag', db_index=True, verbose_name='Tags', blank=True, null=True)
    category = models.ForeignKey('Category', verbose_name='Categoria', blank=True, null=True)
    author = models.ForeignKey('Author', verbose_name='Autor', blank=True, null=True)
    top = models.BooleanField('Titular', default=False)
    active = models.BooleanField('Publicar', default=False)
    order = models.IntegerField('Orden', null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.slug)

    @models.permalink
    def get_absolute_url(self):
        return ('view_single_post', (), {'year': self.date.year, 'month': self.date.month, 'slug': self.slug})

    @property
    def get_permalink(self):
        return mark_safe('<a href="{0}" target="_blank">{1}</a>'.format(self.get_absolute_url(), self.title.encode("utf-8")))


    def get_related_entries(self):
        entries = cache.get('relate_entries_v2_{0}'.format(self.id))
        if not entries:
            entries = Entry.objects.select_related('author', 'category').filter(tags__in=self.tags.all(), active=True).exclude(slug=self.slug).order_by('-date').distinct()
            cache.set('relate_entries_v2_{0}'.format(self.id), entries, 60 * 60)

        if not len(entries):
            return None

        return entries[:5]

    def get_recent_entries(self):
        entries = cache.get('recent_entries_v2_{0}'.format(self.id))
        if not entries:
            entries = Entry.objects.select_related('author', 'category').filter(active=True).exclude(slug=self.slug).order_by('-date')
            cache.set('recent_entries_v2_{0}'.format(self.id), entries, 60 * 60)

        if not len(entries):
            return None

        return entries[:3]

    def get_tags(self):
        tags = cache.get('tags_of_{0}'.format(self.id))
        if not tags:
            tags = self.tags.all()
            cache.set('tags_of_{0}'.format(self.id), tags, 60 * 60)

        return tags 

    def get_top_tags(self):
        tags_top = []

        try:
            tags_top = [tag.tag for tag in self.get_tags()[:4]]
        except:
            return None

        return tags_top

    def get_top_tags_string(self):
        tags_top = self.get_top_tags()

        return ', '.join(tags_top) if tags_top else ''

    def has_photo(self):
        try:
            return True if self.photo.url else False
        except:
            return False

    def dehydrate(self):
        response = {
            'title': self.title.encode('utf-8'),
            'permalink': 'http://www.noticiasroma.com{0}'.format(self.get_absolute_url()),
            'about': self.about.encode('utf-8'),
            'photo': self.photo.url
        }

        return response

    def save(self):
        if not self.id:
            slug = slugify(self.title)
            count = Entry.objects.filter(slug=slug).count()
            if count > 0:
                slug = "{0}-{1}".format(slug, str(count))
            self.slug = slug

            self.date = timezone.now()
            self.order = Entry.objects.all().count() + 1

        cache.delete('entry_{0}_v4'.format(self.slug))
        super(Entry, self).save()

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'
# watson_register(Entry)

class Tag(models.Model):
    tag = models.CharField('Tag', max_length=150, unique=True, db_index=True)
    slug = models.SlugField('Slug', max_length=200, unique=True)

    def __unicode__(self):
        return u'{0}'.format(self.tag)

    @models.permalink
    def get_absolute_url(self):
        return ('view_tag', (), {'slug': self.slug})

    def save(self):
        if not self.id:
            slug = slugify(self.tag)
            count = Tag.objects.filter(slug=slug).count()
            if count > 0:
                slug = "{0}-{1}".format(slug, str(count))
            self.slug = slug

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
        return ('view_category', (), {'slug': self.slug})

    @property
    def get_permalink(self):
        return mark_safe('<a href="{0}" target="_blank">"{0}"</a>'.format(self.get_absolute_url()))
    
    def save(self):
        # if not self.id:
        slug = slugify(self.name)
        count = Category.objects.filter(slug=slug).count()
        if count > 0:
            slug = "{0}-{1}".format(slug, str(count))
        
        self.slug = slug

        super(Category, self).save()

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'


class Author(models.Model):
    user = models.ForeignKey(UserGiallorosso, verbose_name='Usuario editor', db_index=True)
    short_about = models.TextField("Biografia")
    photo = models.ImageField('Foto de editor', upload_to="blog/authors/photos", blank=True, null=True)

    def __unicode__(self):
        return u'{0}'.format(self.user.get_full_name())

    def get_author_info(self):
        author_info = cache.get('author_info_{0}'.format(self.id))

        if not author_info:
            author_info = self.user
            cache.set('author_info_{0}'.format(self.id), author_info, 60 * 60)
        return author_info

    def get_entries_of_this_author(self):
        return Entry.objects.filter(active=True, author=self).order_by('-order')

    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'
