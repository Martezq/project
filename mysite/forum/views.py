from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib import messages
from .models import Post, Comment, Topic
from .forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q



def search(request):
    query = request.GET.get('q', '')
    if query:
        topics = Topic.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

    else:
        topics = Topic.objects.all()
        posts = Post.objects.all()


    context = {
        'topics': topics,
        'posts': posts,
    }
    return render(request, 'forum/search_results.html', context)

def forum_main(request):
    topics = Topic.objects.all()
    topics_and_latest_posts = []

    for topic in topics:
        latest_post = Post.objects.filter(topic=topic).order_by('-created_at').first()
        topics_and_latest_posts.append((topic, latest_post))

    context = {
        'topics_and_latest_posts': topics_and_latest_posts,
    }
    return render(request, 'forum/forum_main.html', context)




def post_list(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    posts = Post.objects.filter(topic=topic).order_by('-created_at')
    paginator = Paginator(posts, 20) 

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    context = {
        'posts': posts,
        'topic_id': topic_id,
    }
    return render(request, 'forum/post_list.html', context)


@login_required
def post_create(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.user_id = request.user.id
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('forum:post_list', topic_id=topic_id)
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'forum/post_create.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user:
        messages.error(request, 'You do not have permission to edit this post.')
        return redirect('forum:post_list', topic_id=post.topic.id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('forum:post_list', topic_id=post.topic.id)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'forum/post_edit.html', context)


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.user:
        messages.error(request, 'You do not have permission to delete this post.')
        return redirect('forum:post_list', topic_id=post.topic.id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('forum:post_list', topic_id=post.topic.id)

    context = {
        'post': post,
        'topic_id': post.topic.id,
    }
    return render(request, 'forum/post_delete.html', context)



@login_required
def create_comment(request, post_id, parent_comment_id=None):
    post = get_object_or_404(Post, id=post_id)

    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)
    else:
        parent_comment = None

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.parent_comment = parent_comment
            comment.save()
            messages.success(request, 'Comment created successfully!')
            return redirect('forum:post_detail', pk=post_id)
    else:
        form = CommentForm(initial={'parent_comment': parent_comment})

    context = {
        'form': form,
    }
    return render(request, 'forum/comment_create.html', context)


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.filter(parent_comment=None).order_by('created_at')
        context['comments'] = comments
        context['form'] = CommentForm()
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'forum/comment_update.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        return reverse_lazy('forum:post_detail', kwargs={'pk': self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        return reverse_lazy('forum:post_detail', kwargs={'pk': self.object.post.pk})
