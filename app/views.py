from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView

from root.custom_permissions import OnlyLoggedSuperUser
from .forms import ContactForm, CommentForm
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


class HomePageView(ListView):
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


class SearchReturnView(ListView):
    model = News
    template_name = 'app/search.html'
    context_object_name = 'all_news'

    def get_queryset(self):
        pass


@login_required
def news_list(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list,
    }
    return render(request, 'app/list.html', context)


def news_detail(request, slug):
    new = get_object_or_404(News, slug=slug, status=News.Status.PUBLISHED)
    comments = new.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.new = new
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'new': new,
        'new_comment': new_comment,
        'comments': comments,
        'comment_form': comment_form,
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
