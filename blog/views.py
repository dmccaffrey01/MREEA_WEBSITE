from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.decorators import login_required
from .models import BlogPost
from .forms import BlogPostForm
from profiles.models import UserProfile
from django.contrib import messages
from membership.models import Membership


def blog_list(request):

    approved_posts = BlogPost.objects.filter(is_approved=True, is_awaiting_approval=False).order_by('-approved_at')

    for post in approved_posts:
        profile = UserProfile.objects.filter(user=post.author).first()
        post.profile = profile

    if request.user.is_superuser:
        awaiting_approval_posts = BlogPost.objects.filter(is_awaiting_approval=True).order_by('-created_at')
        for post in awaiting_approval_posts:
            profile = UserProfile.objects.filter(user=post.author).first()
            post.profile = profile
    else:
        awaiting_approval_posts = False
    
    context = {
        'approved_posts': approved_posts,
        'awaiting_approval_posts': awaiting_approval_posts,
    }

    return render(request, 'blog/blog_list.html', context)


def blog_detail(request, slug):

    post = BlogPost.objects.filter(slug=slug).first()

    if not post:
        messages.error(request, "Invalid blog post!")
        return redirect(reverse('blog_list'))
    
    context = {
        'post': post,
    }

    return render(request, 'blog/blog_detail.html', context)


@login_required
def add_blog(request):

    user = request.user

    membership = Membership.objects.filter(user=user).first()

    if (not membership ) or (not user.is_superuser):
        messages.error(request, "You must be a member to create a new blog post!")
        return redirect(reverse('blog_list'))
    
    if not membership.status.valid:
        messages.error(request, "You must be a member to create a new blog post!")
        return redirect(reverse('blog_list'))
    
    if request.method == "POST":
        form = BlogPostForm(request.POST)
    
        if form.is_valid():
            form_data = form.cleaned_data
            title = form_data["title"]
            content = form_data["content"]

            new_post = BlogPost.objects.create(
                title=title,
                content=content,
                author=user,
            )

            new_post.save()

            return redirect(reverse('blog_list'))
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    }

    return render(request, 'blog/blog_form.html', context)

