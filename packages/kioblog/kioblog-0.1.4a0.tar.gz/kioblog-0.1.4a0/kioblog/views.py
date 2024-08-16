from django.views import generic
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator

from kioblog import models
from kioblog import decorators


class HomeView(generic.TemplateView):
    template_name = 'kioblog/home.html'

    def get_context_data(self, **kwargs):
        category = kwargs.get('category', False)
        page = kwargs.get('page', 1)
        if category:
            posts = models.Post.objects.filter(category__slug=category, draft=False)
        else:
            posts = models.Post.objects.filter(draft=False)
        paginator = Paginator(posts, 5)
        data = {'posts': paginator.get_page(page),
                'page_range': range(1, paginator.num_pages + 1),
                'recent_posts': models.Post.get_recent_posts()}

        return data


@method_decorator(decorators.load_recent_posts, name='dispatch')
class PostView(generic.DetailView):
    template_name = 'kioblog/post.html'
    model = models.Post
