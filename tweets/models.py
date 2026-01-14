from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince


class Tweet(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tweets'
    )
    retweet = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='retweets'
    )
    reply = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        # 元ツイートから返信一覧を引く用（tweet.replies）
        related_name='replies'
    )
    # リツイート時のためにDBのnullは許可するが、ツイート時にblankは許可しないように
    content = models.CharField(max_length=140, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def get_following_tweets(cls, user):
        # フォローしているユーザーの取得
        following_ids = user.following.values_list('id', flat=True)
        return cls.objects.filter(user_id__in=following_ids)

    @property
    def formatted_date(self):
        # Twitter風な時間表示にする

        # Djangoの標準timesinceを取得（例: '10時間, 3 分'）
        ts = timesince(self.created_at, timezone.now())
        # カンマで区切って最初の要素だけを取り出すことで、上記のような場合でも、最初の「10時間」だけが取れる
        formatted = ts.split(',')[0]
        return formatted

    def __str__(self):
        # content がある場合は先頭20文字、ない場合（リツイートなど）は固定文言を返す
        if self.content:
            content_display = self.content[:20]
        else:
            content_display = "内容なし（リツイート）"
        return f"{self.user.username}: {content_display}"


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # ユーザーから「いいね一覧」を引く用
        related_name='likes'
    )
    tweet = models.ForeignKey(
        'Tweet',
        on_delete=models.CASCADE,
        # ツイートから「いいねしてくれた人一覧」を引く用
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ここで user_id と tweet_id の組み合わせをユニークにする（DBレベルの制約）
        unique_together = ('user', 'tweet')
