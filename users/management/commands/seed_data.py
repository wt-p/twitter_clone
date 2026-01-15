import random
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from tweets.models import Tweet, Like

# これで現在有効なUserクラスが取得できる
User = get_user_model()


class Command(BaseCommand):
    help = """
        以下のデータを生成・同期するシードスクリプトです：
        1. テストユーザー10名の作成（既存ユーザーはプロフィール補完）
        2. 各ユーザーによる3〜5件の通常ツイート（指定済みリストからランダム）
        3. 全ユーザーにおいて最低1件の「リツイート」「返信」「いいね」「フォロー」を保証
    """

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.MIGRATE_HEADING('--- Seedデータ作成プロセス開始 ---'))

        # 1. ユーザーの生成とプロフィール更新
        self.stdout.write('1. ユーザー情報を作成中...')
        for i in range(10):
            user, created = User.objects.get_or_create(
                username=f'testuser_{i}',
                defaults={
                    'email': f'testuser_{i}@example.com',
                    'display_name': f'ユーザー_{i}',
                    'password': make_password('password123'),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'[新規作成] {user.username}'))

        all_users = User.objects.all()
        for user in all_users:
            updated = False
            if not user.bio:
                user.bio = f'こんにちは、{user.username}です。Twitterクローン開発中！'
                updated = True
            if not user.location:
                user.location = random.choice(['東京', '大阪', '名古屋', '福岡', '沖縄'])
                updated = True
            if not user.website:
                user.website = 'https://example.com'
                updated = True
            if not user.date_of_birth:
                user.date_of_birth = datetime.date(1990, 1, 1)
                updated = True
            if updated:
                user.save()
        self.stdout.write('[完了] 全ユーザーのプロフィールを補完しました。')

        tweet_contents = [
            '今日も1日お疲れ様でした！進捗ダメです！ 🫠',
            'デプロイ直前の緊張感、何回やっても慣れないわ...',
            'バグが取れなくて3時間。原因はタイポでした。解散！ 🙄',
            'カフェでコーディングすると捗る気がするのは何でだろう。 ☕',
            'お昼ごはん、何食べようかな。ラーメンの口になってる 🍜',
            '結局、家のカレーが一番美味しい説 🍛',
            'コンビニの新作スイーツ、ついつい買っちゃうよね。 🍰',
            '朝起きたら喉が痛い...。みんなも風邪には気をつけて！ 😷',
            '週末の天気が良さそうで嬉しい！キャンプ行きたい ⛺',
            '最近買ったキーボードが最高すぎて、無駄にタイピングしてる ⌨️',
            '積読が溜まっていく一方...。時間が足りない！ 📚',
            '推しの新曲が良すぎてもう無限ループしてる 🎧',
            'フォロー外から失礼します！これめっちゃわかります 🤝',
            'あ、もうこんな時間...。SNS見てると時間溶けるの早すぎ ⏰',
            '久しぶりに実家に帰ったら、猫に忘れられてて泣いた 🐈',
            '散歩中に見かけた空が綺麗だったので共有 ☁️',
            '筋トレ始めて3日目。今のところ筋肉痛との戦い 💪',
            '「明日から本気出す」をもう3日言ってる 🛌',
        ]

        # 2. 通常ツイートの生成
        self.stdout.write('2. 通常ツイートを生成中...')
        for user in all_users:
            current_count = user.tweets.filter(retweet__isnull=True, reply__isnull=True).count()
            if current_count < 3:
                num_to_create = random.randint(3, 5)
                for _ in range(num_to_create):
                    Tweet.objects.create(
                        user=user,
                        content=random.choice(tweet_contents) + f' (ID:{random.randint(100, 999)})'
                    )
        self.stdout.write('[完了] 通常ツイートの生成が完了しました。')

        # 3. フォロー、リツイート、コメント、いいねの生成
        self.stdout.write('3. フォロー・RT・コメント・いいねを作成中...')
        all_tweets = list(Tweet.objects.filter(retweet__isnull=True, reply__isnull=True))

        for user in all_users:
            # フォロー（1人〜3人）
            target_follows = random.sample(
                [u for u in all_users if u != user], random.randint(1, 3)
            )
            for target in target_follows:
                user.following.add(target)

            # リツイート（無ければ1件作成）
            if not Tweet.objects.filter(user=user, retweet__isnull=False).exists():
                target = random.choice(all_tweets)
                Tweet.objects.create(user=user, retweet=target, content=None)

            # コメント（無ければ1件作成）
            if not Tweet.objects.filter(user=user, reply__isnull=False).exists():
                target = random.choice(all_tweets)
                Tweet.objects.create(
                    user=user,
                    reply=target,
                    content='それな'
                )

            # いいね（無ければ1件作成）
            if not Like.objects.filter(user=user).exists():
                target = random.choice(all_tweets)
                Like.objects.get_or_create(user=user, tweet=target)

        self.stdout.write(self.style.SUCCESS('--- Seedデータの作成がすべて完了しました！ ---'))
