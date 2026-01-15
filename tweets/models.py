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
    content = models.CharField(max_length=140)
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
        return f'{self.user.username}: {self.content[:20]}'
