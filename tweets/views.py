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

    # ベースとなるクエリセットを作成
    # select_relatedでユーザー情報を事前に結合（JOIN）し、テンプレート表示時のN+1問題を防止
    base_qs = (
        Tweet.objects
        .select_related('user', 'reply__user', 'retweet__user')
        .order_by('-created_at')
    )
    match tab:
        case 'retweet':
            tweet_list = base_qs.filter(user=profile_user, retweet__isnull=False)
        case 'comment':
            tweet_list = base_qs.filter(user=profile_user, reply__isnull=False)
        case 'like':
            tweet_list = base_qs.filter(favorited_by__user=profile_user).distinct()
        case _:
            tweet_list = base_qs.filter(user=profile_user, retweet__isnull=True, reply__isnull=True)

    # ページネーション設定 (10件ずつ)
    paginator = Paginator(tweet_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tweet/profile.html', {
        'profile_user': profile_user,
        'page_obj': page_obj,
        'tab': tab
    })
