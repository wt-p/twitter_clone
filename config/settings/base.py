"""
ローカル・本番環境共通設定
"""

import environ

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # githubログイン用
    'allauth.socialaccount.providers.github',
    'cloudinary_storage',
    'cloudinary',
    'sass_processor',
    'users',
]

# django.contrib.sitesフレームワークで使うデフォルトID
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 最新のallauthで必須とのことで追記
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'config/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    # 静的ファイル
    'staticfiles': {
        # 修正前
        # 'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
    # 画像アップロード
    # ローカル保存がデフォルト、productionの方でCloudinaryの設定を上書きする
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

# allauthの認証ロジックについての設定
AUTHENTICATION_BACKENDS = [
    # Django標準
    'django.contrib.auth.backends.ModelBackend',
    # allauth用
    # 'allauth.account.backends.DefaultBackend',
    # 最新版では以下のパスに変更されたそう
    'allauth.account.auth_backends.AuthenticationBackend',
]

# allauthの挙動設定
# ログイン後のリダイレクト先
LOGIN_REDIRECT_URL = '/home'
# ログアウト後のリダイレクト先
ACCOUNT_LOGOUT_REDIRECT_URL = '/home'

# サインアップ設定
# ユーザー名とメアド両方使用
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# メアド入力を必須にする
ACCOUNT_EMAIL_REQUIRED = True
# ユーザー名入力を必須にする
ACCOUNT_USERNAME_REQUIRED = True
# メール確認を必須にする
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# 1つのアカウントにメアドは1つ
ACCOUNT_MAX_EMAIL_ADDRESSES = 1

ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'
MESSAGES_ENABLED = True

# allauthにカスタムフォームを教える
ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

# --- SCSS設定（ここから） ---

# Djangoが静的ファイルを探す仕組みにSCSS用を追加
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# SCSSファイルを置くルートディレクトリ
SASS_PROCESSOR_ROOT = BASE_DIR / 'static'

# --- SCSS設定（ここまで） ---
