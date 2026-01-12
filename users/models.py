from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    tel = models.CharField(max_length=20, unique=True, blank=True, null=True)
    # passwordはAbstractUserで管理するため定義不要
    display_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.CharField(max_length=160, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    avatar_image = models.ImageField(upload_to='avatar_images/', blank=True, null=True)
    # フォロー・フォロワーの関係を直感的に取得するため
    following = models.ManyToManyField(
        'self',
        # 自動生成ではなく、自分で作ったFollowモデルを中間テーブルとして使う
        through='Follow',
        # (自分, 相手) の順でカラムを指定
        through_fields=('follower', 'followee'),
        # 片方方向のフォロー関係にするため
        symmetrical=False,
        # 相手側から「誰にフォローされているか」を取得する際の名称。以下例
        # 「自分がフォローしている人」の一覧を取得(request.user.following.all())
        # 「自分がフォローしている人」の一覧を取得(request.user.followers.all())
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # ユニーク制約で同じペアが2重に登録されるのを防ぐ
        unique_together = ('follower', 'followee')

    def __str__(self):
        return f'{self.follower.username} follows {self.followee.username}'
