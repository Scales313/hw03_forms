from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from yatube.settings import POSTS_ON_PAGE

from .models import Group, Post
from .forms import PostForm


def index(request):
    '''
    the function displays the last
     {POSTS_ON_PAGE} posts on the site
    '''
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    '''
    the function displays the last
     {POSTS_ON_PAGE} posts on the site
     from selected group
    '''
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    '''
    the function displays the profile of the selected user
    '''
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    posts_count = Post.objects.filter(author=author).count()
    paginator = Paginator(posts, POSTS_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'posts': posts,
        'page_obj': page_obj,
        'posts_count': posts_count,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    '''
    the function displays the selected post
    '''
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    posts_count = Post.objects.filter(author=author).count()
    context = {
        'post': post,
        'posts_count': posts_count,
    }
    return render(request, 'posts/post_detail.html', context)


class CreateNewPost(CreateView):
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('profile/<str:username>/')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
