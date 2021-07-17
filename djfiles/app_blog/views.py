import csv
from datetime import datetime

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView

from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from djfiles import settings

from app_blog.models import Blog, Profile, FileHolder, Avatar
from app_blog.forms import RegistrationsForm, BlogForm


class MainView(generic.TemplateView):
    template_name = 'app_blog/base.html'


class RegistrationsView(generic.FormView):
    template_name = 'app_blog/registrations.html'
    success_url = reverse_lazy('blog')
    form_class = RegistrationsForm

    def form_valid(self, form):
        # вот тут по разному пробовал сделать, но короче не вышло
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(username, password=password)
        login(self.request, user)
        if form.cleaned_data['about_me']:
            profile = Profile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                about_me=form.cleaned_data['about_me'],
            )
            profile.save()
        else:
            profile = Profile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
            )
            profile.save()
        if form.cleaned_data['avatar']:
            Avatar.objects.create(
                profile=profile,
                image=form.cleaned_data['avatar'],
            )
        return redirect(self.success_url)


class AuthenticatedView(LoginView):
    template_name = 'app_blog/login.html'


class Logout(LogoutView):
    template_name = 'app_blog/logout.html'


class CreateBlogWithCsv(generic.CreateView):
    template_name = 'app_blog/create_blog_csv.html'
    model = Blog
    # не хочу указывать fields , но не указав его, выбрасывается искл.
    # вообще есть ощущение , что тут можно TemplateView использовать??
    fields = ('content', 'title',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = BlogForm
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            csv_file_availability = request.FILES.getlist('csv_file')
            if csv_file_availability:
                csv_file = request.FILES['csv_file'].read()
                csv_file_str = csv_file.decode('utf-8').split('\n')
                data_for_blog = csv.reader(csv_file_str, delimiter=',', quotechar='"')
                for data in data_for_blog:
                    convert_data = datetime.strptime(data[1], '%d:%m:%Y')
                    blog = Blog.objects.create(
                        user=request.user,
                        content=data[0],
                        published=convert_data,
                    )
                    blog.save()
                    files = request.FILES.getlist('image')
                    if files:
                        for f in files:
                            image_blog_obj = FileHolder.objects.create(blog=blog, image=f)

                            image_blog_obj.save()

        return redirect('/blog')


class CreateBlog(generic.CreateView):
    template_name = 'app_blog/create_blog.html'
    model = Blog
    fields = ('title', 'content',)
    success_url = reverse_lazy('blog')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_file = BlogForm()
        form_file.fields['csv_file'].widget = forms.HiddenInput()
        context['form_file'] = form_file
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user_id = self.request.user.id
        self.object.save()
        files = self.request.FILES.getlist('image')
        if files:
            for f in files:
                image_blog_obj = FileHolder.objects.create(blog=self.object, image=f)
                image_blog_obj.save()
        return super(CreateBlog, self).form_valid(form)


class BlogList(generic.ListView):
    template_name = 'app_blog/blog_list.html'
    queryset = Blog.objects.all().order_by('-created_at')
    context_object_name = 'blog_list'


class BlogDetail(generic.DetailView):
    template_name = 'app_blog/blog_detail.html'
    model = Blog
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()
        return (context)


class UserDetail(generic.DetailView):
    template_name = 'app_blog/user_detail.html'
    model = User
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media = settings.MEDIA_URL
        context['media'] = media
        return context


class ImageDetail(generic.DetailView):
    template_name = 'app_blog/image_detail.html'
    model = FileHolder
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
