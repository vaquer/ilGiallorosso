from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.core.cache import cache
from .models import Entry

class LastEntriesRss(Feed):
	title = "Ultimas noticias de la AS Roma"
	link = "/"
	description = "Las noticias mas recientes y opiniones mas originales de la AS Roma"

	def items(self):
		last_entries_rss = cache.get('last_entries_rss')

		if not last_entries_rss:
			last_entries_rss = Entry.objects.filter(active=True).order_by('-date')
			cache.set('last_entries_rss', last_entries_rss, 60 * 60)

		return last_entries_rss

	def item_title(self, item):
		return item.title

	def item_about(self, item):
		return item.about

	def get_context_data(self, **kwargs):
	    context = super(LastEntriesRss, self).get_context_data(**kwargs)
	    item = kwargs['item']
	    if item.photo:
	    	context['photo'] = item.photo.url
	    return context
