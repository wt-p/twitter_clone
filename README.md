# Twitter Clone（Django）

Djangoを用いたTwitterクローンアプリケーションです。 <br>
現在は基本機能の実装を終え、さらなる機能拡張やリファクタリングを繰り返している真っ最中です。<br>
「ただ動くものを作る」だけでなく、Dockerでの環境構築や、GitHubでのプルリクエストベースの開発など、実務で通用する質の高い開発フローを意識して日々開発しています。

---

<a id="toc"></a>
## 目次
- [使用技術](#tech)
- [開発・実行環境](#env)
- [構成概要](#arch)
- [環境構築 / 起動方法](#setup)
- [実装機能](#features)
- [品質・開発フロー](#quality)
- [デプロイ](#deploy)
- [成果物](#deliverables)
- [Roadmap（今後の実装予定）](#roadmap)

---

<a id="tech"></a>
## 使用技術
### App Profile

<table>
  <tr>
    <th>Environment</th>
    <th>Language</th>
    <th>Framework / Library</th>
    <th>Database</th>
    <th>Tools</th>
    <th>External Services</th>
  </tr>
  <tr>
    <td>
      <img src="https://img.shields.io/badge/-Docker-EEE.svg?logo=docker&style=flat">
      <img src="https://img.shields.io/badge/-Linux-EEE.svg?logo=linux&style=flat">
      <br>
      <img src="https://img.shields.io/badge/-Heroku-430098.svg?logo=heroku&style=flat">
    </td>
    <td>
      <img src="https://img.shields.io/badge/-Python-F9DC3E.svg?logo=python&style=flat">
      <img src="https://img.shields.io/badge/-HTML5-333.svg?logo=html5&style=flat">
      <img src="https://img.shields.io/badge/-CSS3-1572B6.svg?logo=css3&style=flat">
      <img src="https://img.shields.io/badge/-JavaScript-276DC3.svg?logo=javascript&style=flat">
    </td>
    <td>
      <img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat">
      <img src="https://img.shields.io/badge/-django--allauth-092E20.svg?logo=django&style=flat">
      <br>
      <img src="https://img.shields.io/badge/-SCSS-CC6699.svg?logo=sass&style=flat">
      <img src="https://img.shields.io/badge/-WhiteNoise-555.svg?style=flat">
      <img src="https://img.shields.io/badge/-Gunicorn-499848.svg?style=flat">
    </td>
    <td>
      <img src="https://img.shields.io/badge/-PostgreSQL-555.svg?logo=postgresql&style=flat">
    </td>
    <td>
      <img src="https://img.shields.io/badge/-Git-F05032.svg?logo=git&style=flat">
      <img src="https://img.shields.io/badge/-GitHub-181717.svg?logo=github&style=flat">
      <br>
      <img src="https://img.shields.io/badge/-Docker--Compose-2496ED.svg?logo=docker&style=flat">
      <img src="https://img.shields.io/badge/-flake8-555.svg?logo=python&style=flat">
      <img src="https://img.shields.io/badge/-MailCatcher-555.svg?style=flat">
      <img src="https://img.shields.io/badge/-DBeaver-372923.svg?style=flat">
    </td>
    <td>
      <img src="https://img.shields.io/badge/-Cloudinary-3448C5.svg?logo=cloudinary&style=flat">
      <img src="https://img.shields.io/badge/-Resend-000000.svg?style=flat">
    </td>
  </tr>
</table>

- **Environment**: Docker / Linux / Heroku  
- **Language**: Python / HTML / CSS / JavaScript  
- **Framework / Library**: Django / django-allauth / SCSS / WhiteNoise / Gunicorn  
- **Database**: PostgreSQL  
- **Tools**: Git / GitHub / Docker Compose / flake8 / PyCharm / DBeaver / MailCatcher  
- **External Services**: Resend / Cloudinary  

---

<a id="env"></a>
## 開発・実行環境
- 開発環境：macOS  
- 実行環境：Linux（Docker / Heroku）

---

<a id="arch"></a>
## 構成概要
- Docker / Docker Compose による開発環境のコンテナ化
- Web / DB / MailCatcher を分離した構成
- ローカル・本番での環境差異を最小限に抑える構成を意識

---

<a id="setup"></a>
## 環境構築 / 起動方法

### 前提
- Docker
- Docker Compose

### セットアップ手順

```
git clone <this-repository>
cd twitter_clone
docker compose --build -d
```

### 初期セットアップ（初回のみ）

```
docker compose exec web python manage.py migrate
docker compose exec web python manage.py seed_data
docker compose exec web python manage.py createsuperuser
```

### アクセス
#### Twitterクローン
- http://localhost:3000
#### MailCatcher
- http://localhost:1080

---

<a id="features"></a>
## 実装機能

### 🏠 タイムライン
- ログイン状況に応じたヘッダーの動的表示
- 「おすすめ」「フォロー中」のタブ切り替え表示
- ボタン型ページネーション

### 🔐 認証・ユーザー管理
- サインアップ / ログイン（メール認証対応）
- GitHub アカウントによる OAuth ログイン
- カスタムユーザーモデル（電話番号・生年月日拡張）

### 👤 プロフィール
- ユーザー情報の表示および編集機能
- アクティビティ別タブ表示（ツイート / いいね / RT / コメント）

### 🐦 ツイート・リアクション
- テキスト投稿機能（最大140文字）
- いいね / リツイート / 返信の表示用 UI（ボタン等は順次実装予定）

---

<a id="quality"></a>
## 品質・開発フロー
- プルリクエスト単位での開発・レビュー
- flake8 による静的解析
- PEP8 を意識したコーディング
- 実務を想定したブランチ運用

---

<a id="deploy"></a>
## デプロイ
- Heroku にデプロイ済み
- 本番環境での動作確認を実施

---

<a id="deliverables"></a>
## 成果物
- アプリ URL  
  https://enigmatic-sands-55648-4c5cb567b505.herokuapp.com/

---

<a id="roadmap"></a>
## Roadmap（今後の実装予定）
- プロフィール(画像編集)
- ツイート機能(画像アップロード)
- ツイート詳細ページ
- いいね / リツイート
- フォロー / ブックマーク
- メッセージ（DM）
- 通知機能
