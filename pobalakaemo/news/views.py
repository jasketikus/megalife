from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .forms import *
from .utils import *


class NewsHome(DataMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Головна сторінка")
        return context|c_def

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('cat')


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'news/addpage.html'
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Додавання сторінки")
        return context|c_def

    def form_valid(self, form):
        poster = self.request.user
        instance = form.save(commit=False)
        instance.news_author = poster
        instance.save()
        success_message = 'Відправлено на модерацію.'
        messages.add_message(
            message=(success_message),
            level=messages.INFO,
            request=self.request,
        )
        return redirect('add_page')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'news/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Зворотній зв'язок")
        return context|c_def

    def form_valid(self, form):
        # print(form.cleaned_data)
        success_message = 'Лист відправлено. Дякуємо.'
        messages.add_message(
            message=(success_message),
            level=messages.INFO,
            request=self.request,
        )
        return redirect('contact')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Сторінка не знайдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = News
    template_name = 'news/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return context|c_def


class NewsCategory(DataMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return News.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категорія - ' + str(c.name),
                                      cat_selected=c.pk)
        return context|c_def


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'news/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        return context|c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'news/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        return context|c_def

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

