import autocomplete_light
from .models import Tag

autocomplete_light.register(Tag, search_fields=['tag'])