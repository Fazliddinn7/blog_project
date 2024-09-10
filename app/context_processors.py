from app.models import New, Category


def latest_post(request):
    latest_news = New.published.all().order_by('-publish_time')
    categories = Category.objects.all()
    context = {
        'latest_news': latest_news,
        'categories': categories,
    }
    return context
