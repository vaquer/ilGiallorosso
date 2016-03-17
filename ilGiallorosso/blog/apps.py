from django.apps import AppConfig
from watson import search as watson


class BlogWatsonConfig(AppConfig):
    name = 'blog'

    def ready(self):
        noticiasRomaModel = self.get_model("Entry")
        watson.register(noticiasRomaModel)
