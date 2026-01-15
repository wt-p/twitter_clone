from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Tweet


def home(request):
    # 何もなかったらおすすめとして受け取る
    tab = request.GET.get('tab', 'recommend')
    if tab == 'following' and request.user.is_authenticated:
        tweet_list = Tweet.get_following_tweets(request.user)
    else:
        tweet_list = Tweet.objects.all()

    # ページネーション設定 (10件ずつ)
    paginator = Paginator(tweet_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tweet/home.html', {
        'page_obj': page_obj,
        'tab': tab
    })
