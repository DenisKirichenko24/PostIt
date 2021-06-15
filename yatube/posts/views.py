from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, User, Comment, Follow


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.group_posts.all()[:11]
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    post_ren = render(request, 'group.html', {'group': group, 'page': page})
    return post_ren


@login_required
def new_post(request):
    form = PostForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('index')
    return render(request, 'new.html', {'form': form})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_prof = profile.posts.all()
    posts_count = post_prof.count()
    follow_count = profile.follower.count()
    following_count = profile.following.count()
    following = False
    #  нашел данный метод в гугле но не понял можно ли его использовать
    #  так как писали что в новых версиях Джанго не поддерживается
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=profile).exists():
            following = True
    paginator = Paginator(post_prof, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {
        'profile': profile,
        'posts_count': posts_count,
        'page_num': page_number,
        'page': page,
        'follow_count': follow_count,
        'following_count': following_count,
        'following': following,
    })


def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    author = post.author
    posts_count = author.posts.count()
    form = CommentForm()
    comments = Comment.objects.filter(post=post_id)

    context = {
        'post': post,
        'author': author,
        'posts_count': posts_count,
        'form': form,
        'comments': comments
    }
    return render(request, 'post.html', context)


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    if request.user != post.author:
        return redirect('post', username, post_id)
    form = PostForm(request.POST or None,
                    files=request.FILES or None, instance=post)
    if form.is_valid():
        post.save()
        return redirect('post', username, post_id)
        return render(request, 'new.html', {'form': form, 'edit': True})
    return render(request, 'new.html', {
        'form': PostForm(instance=post),
        'post': post
    })


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.author = request.user
        new_comment.post = post
        new_comment.save()
        return redirect('post', username, post_id)
    form = CommentForm()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    follow_render = render(request, 'follow.html',
                           {'page': page, 'paginator': paginator})
    return follow_render


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        have_follow = Follow.objects.filter(user=request.user,
                                            author=author)
        if not have_follow:
            Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=author).delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
