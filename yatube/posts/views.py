from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, User


def pages(request, value):
    paginator = Paginator(value, 10)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    last_posts = Post.objects.all()[:11]
    page = pages(request, last_posts)
    return render(request, 'index.html', {'page': page, })


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.group_posts.all()[:11]
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    post_ren = render(request, "group.html", {"group": group, "page": page})
    return post_ren


@login_required
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('index')
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    author_posts = author.posts.all()
    posts_count = author_posts.count()
    page = pages(request, author_posts)
    context = {
        'author': author,
        'count': posts_count,
        'page': page
    }
    return render(request, 'profile.html', context)


def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    posts_count = author.posts.count()
    form = CommentForm
    comments = post.comments.select_related('author').all()

    context = {
        "post": post,
        "author": author,
        "posts_count": posts_count,
        'form': form,
        'comments': comments
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    if request.user.username != username:
        return redirect('post', username, post_id)
    post = Post.objects.get(pk=post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid():
        post.save()
        return redirect('post', username, post_id)
    return render(request, 'new.html', {'form': form, 'edit': True})


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = post
        new_comment.save()
    return redirect('post', username, post_id)    
