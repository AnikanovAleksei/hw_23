from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)


class PostCreateView(CreateView):
    model = Post
    fields = ["title", "content", "image", "is_published", "number_of_views"]
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.number_of_views += 1
        self.object.save()
        return super().get(request, *args, **kwargs)


class PostUpdateView(UpdateView):
    model = Post
    fields = ["title", "content", "image", "is_published", "number_of_views"]
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse('blog:post_detail', kwargs={'pk': pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
