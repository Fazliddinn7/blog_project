from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView

from root.custom_permissions import OnlyLoggedSuperUser
from .forms import ContactForm
from .models import News


class LocalPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/local.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Mahalliy')


class SportPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Sport')


class ForeignPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/foreign.html'
    context_object_name = 'xorijiy_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Xorij')


class TechnologyPageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'pages/technology.html'
    context_object_name = 'texnologiya_yangiliklar'

    def get_queryset(self):
        return self.model.published.filter(category__name='Texnologiya')


class ContactPageView(LoginRequiredMixin, TemplateView):
    template_name = 'app/contact.html'
    form_class = ContactForm
    initial = {'key': 'value'}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h1>Biz bilan bog'langaningiz uchun tashakkur</h1>")
        return render(request, self.template_name, {'form': form})


# def home_view(request):
#     categories = Category.objects.all()
#     news_list = New.published.all().order_by('-publish_time')[:5]
#     local_news = New.published.filter(category__name='Mahalliy')[:5]
#     ommabop_news = New.published.all().order_by('-publish_time')[:5]
#     sport_news = New.published.filter(category__name='Sport')[:5]
#     technology_news = New.published.filter(category__name='Texnologiya')[:5]
#     foreign_news = New.published.filter(category__name='Xorij')[:5]
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_news': local_news,
#         'ommabop_news': ommabop_news,
#         'sport_news': sport_news,
#         'technology_news': technology_news,
#         'foreign_news': foreign_news,
#     }
#     return render(request, 'index.html', context)


class HomePageView(LoginRequiredMixin, ListView):
    model = News
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_news'] = News.published.filter(category__name='Mahalliy')[:5]
        context['sport_news'] = News.published.filter(category__name='Sport')[:5]
        context['technology_news'] = News.published.filter(category__name='Texnologiya')[:5]
        context['foreign_news'] = News.published.filter(category__name='Xorij')[:5]
        context['ommabop_news'] = News.published.all().order_by('-publish_time')[:5]
        return context


@login_required
def news_list(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list,
    }
    return render(request, 'app/list.html', context)


@login_required()
def news_detail(request, slug):
    new = get_object_or_404(News, slug=slug, status=News.Status.PUBLISHED)
    context = {
        'new': new,
    }
    return render(request, 'app/detail.html', context)


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    queryset = News.objects.filter(status=News.Status.PUBLISHED)
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    queryset = News.objects.filter(status=News.Status.PUBLISHED)
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    template_name = 'crud/create.html'
    fields = 'title', 'body', 'image', 'category', 'status'
