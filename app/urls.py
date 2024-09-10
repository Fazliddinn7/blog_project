from django.urls import path
from .views import news_list, news_detail, HomePageView, ContactPageView, LocalPageView, SportPageView, ForeignPageView, \
    TechnologyPageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('list/', news_list, name='news'),
    path('detail/<slug:slug>/', news_detail, name='news_detail_page'),
    path('contact-page', ContactPageView.as_view(), name='contact_page'),
    path('local/', LocalPageView.as_view(), name='local_page'),
    path('sport/', SportPageView.as_view(), name='sport_page'),
    path('foreign/', ForeignPageView.as_view(), name='foreign_page'),
    path('technology/', TechnologyPageView.as_view(), name='technology_page'),
]
