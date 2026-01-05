"""
本番環境用設定
"""


from .base import *
import os

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['.herokuapp.com']

DATABASES = {
    'default': env.db(),
}

STORAGES['default'] = {
    'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
}

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': env('CLOUD_NAME'),
    'API_KEY': env('CLOUDINARY_API_KEY'),
    'API_SECRET': env('CLOUDINARY_API_SECRET')
}

# 本番環境はresendを使用
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'resend'
# HerokuのConfig Varsから読み込み
EMAIL_HOST_PASSWORD = os.environ.get('RESEND_API_KEY')
# resendで使用するメアド
DEFAULT_FROM_EMAIL = 'onboarding@resend.dev'

# Sassの自動コンパイルを本番でも有効にする（WhiteNoiseが拾えるようにするため）
SASS_PROCESSOR_ENABLED = True
SASS_PROCESSOR_ROOT = STATIC_ROOT

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
