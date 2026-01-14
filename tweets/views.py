from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Tweet
from django.contrib.auth import get_user_model


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


def profile(request, username):
    User = get_user_model()
    # 自分以外のプロフィールにもアクセス可能
    profile_user = get_object_or_404(User, username=username)
    tab = request.GET.get('tab', 'tweet')
    # デフォルトのクエリ（「ツイート」タブの内容）を先に定義しておく
    tweet_list = profile_user.tweets.filter(retweet__isnull=True, reply__isnull=True)
    match tab:
        case 'retweet':
            tweet_list = profile_user.tweets.filter(retweet__isnull=False)
        case 'comment':
            tweet_list = profile_user.tweets.filter(reply__isnull=False)
        case 'like':
            tweet_ids = profile_user.likes.values_list('tweet_id', flat=True)
            tweet_list = Tweet.objects.filter(id__in=tweet_ids).select_related('user')

    # ページネーション設定 (10件ずつ)
    paginator = Paginator(tweet_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tweet/profile.html', {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'tab': tab
    })
