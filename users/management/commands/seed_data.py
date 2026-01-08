import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# これで現在有効なUserクラスが取得できる
User = get_user_model()


class Command(BaseCommand):
    help = 'テスト用のユーザー、ツイート、フォロー関係を生成するコマンド'

    def handle(self, *args, **kwargs):
        self.stdout.write('seedデータを作成中...')

        # テストユーザーの作成（50人）
        users = []
        for i in range(50):
            username = f'testuser_{i}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    usernname=username,
                    email=f'{username}@example.com',
                    password='password123'
                )
                users.append(user)

        all_users = list(User.objects.all())

