from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from .forms import PostForm
from django.contrib import messages
from .models import Comment
from .forms import CommentForm


# Create your views here.
def home(request):
    return render(request, 'blog/base.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm

def home(request):
    return render(request, 'blog/base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.name}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user # Get the curret user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)

        user.save()

        messages.success(request, 'Profile updated')
        return redirect('profile')
    return render(request, 'blog/profle.html', {'user': request.user})



# === List View === #

# ===== LIST VIEW =====
class PostListView(ListView):
    """
    Display all blog posts
    URL: /posts/
    Template: blog/post_list.html
    Context variable: object_list (or post_list)
    """
    
    model = Post  # Which model to use
    template_name = 'blog/post_list.html'  # Custom template name
    context_object_name = 'posts' 
    ordering = ['-published_date']  # Newest first



class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        """
        Add extra context to the template:
        - comments: All comments for this post
        - comment_form: Form for new comments (if user logged in)
        """
        context = super().get_context_data(**kwargs)
        
        # Get the post object
        post = self.get_object()
        
        # Add comments to context
        context['comments'] = post.comments.all()  # Using related_name
        
        # Add comment form if user is authenticated
        if self.request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        
        return context



class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new blog post
    URL: /posts/new/
    Template: blog/post_form.html
    Only accessible to logged-in users
    
    LoginRequiredMixin: Redirects to login if not authenticated
    """
    
    model = Post
    form_class = PostForm  # Use our custom form
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')  # Redirect after success
    
    def form_valid(self, form):
        """
        This runs when form is valid
        We set the author before saving
        """
        form.instance.author = self.request.user  # Set author = current user
        return super().form_valid(form)
    


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing blog post
    URL: /posts/1/edit/
    Template: blog/post_form.html (reuses same form!)
    Only accessible to the post author
    
    UserPassesTestMixin: Allows custom permission check
    """
    
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        """
        Permission test - runs automatically
        Returns True if user can access, False if not
        """
        post = self.get_object()  # Get the post being edited
        return self.request.user == post.author  # Only author can edit
    


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a blog post
    URL: /posts/1/delete/
    Template: blog/post_confirm_delete.html
    Only accessible to the post author
    """
    
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        """Only author can delete"""
        post = self.get_object()
        return self.request.user == post
        

# ===== COMMENT VIEWS =====

class CommentCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new comment on a post
    URL: /post/<int:post_id>/comment/new/
    
    LoginRequiredMixin: User must be logged in
    """
    
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def form_valid(self, form):
        """
        Set the post and author before saving
        """
        # Get the post from URL parameter
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        
        # Set the comment's post and author
        form.instance.post = post
        form.instance.author = self.request.user
        
        # Add success message
        messages.success(self.request, 'Your comment has been added!')
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect back to the post after successful comment"""
        return reverse('post_detail', kwargs={'pk': self.object.post.id})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Edit an existing comment
    URL: /comment/<int:pk>/edit/
    
    Only the comment author can edit
    """
    
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        """Permission check - only author can edit"""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def form_valid(self, form):
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect back to the post after editing"""
        return reverse('post_detail', kwargs={'pk': self.object.post.id})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Delete a comment
    URL: /comment/<int:pk>/delete/
    
    Only the comment author can delete
    """
    
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    
    def test_func(self):
        """Permission check - only author can delete"""
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        """Add success message on delete"""
        messages.success(request, 'Your comment has been deleted.')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """Redirect back to the post after deletion"""
        comment = self.get_object()
        return reverse('post_detail', kwargs={'pk': comment.post.id})