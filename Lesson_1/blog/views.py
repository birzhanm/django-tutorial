from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import PostForm
from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.objects.all().order_by('-published_date')
    context = {'posts':posts}
    return render(request, 'blog/post_list.html', context)

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post':post}
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if 'publish' in request.POST:
                post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'blog/post_new.html', context)

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            post.title = form.cleaned_data.get('title')
            post.text = form.cleaned_data.get('text')
            post.published_date=None
            if 'publish' in request.POST:
                post.published_date=timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    context = {'form': form, 'pk':pk}
    return render(request, 'blog/post_edit.html', context)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog:post_list')

def post_draft_list(request):
    draft_posts = Post.objects.filter(author=request.user, published_date__isnull=True).order_by('-created_date')
    context = {'draft_posts': draft_posts}
    return render(request, 'blog/post_draft_list.html', context)
