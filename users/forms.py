from allauth.account.forms import SignupForm
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .models import User
import datetime


# base.pyのACCOUNT_FORMSにてデフォルトのsignupフォームではなくこれを使うように指定
class CustomSignupForm(SignupForm):
    # 電話番号の形式チェック（cleanメソッドのような他のデータやDBとの比較するバリデーションとは分離）
    tel_validator = RegexValidator(
        regex=r'^\d{10,11}$',
        message='電話番号はハイフンなしの10桁または11桁の数字で入力してください'
    )
    # 要件：電話番号と生年月日を追加（required=Falseで任意入力）
    tel = forms.CharField(
        max_length=20,
        label='電話番号',
        required=False,
        validators=[tel_validator]
    )
    date_of_birth = forms.DateField(
        label='生年月日',
        required=False,
        widget=forms.SelectDateWidget(
            years=range(1900, datetime.date.today().year + 1),
            # 未選択時の各プルダウンのラベルを以下に
            empty_label=('年', '月', '日'),
        )
    )

    def clean_tel(self):
        tel = self.cleaned_data.get('tel')
        if tel and User.objects.filter(tel=tel).exists():
            raise ValidationError("この番号は既に登録されています")
        return tel

    def save(self, request):
        # allauthの標準処理でUserを作成
        user = super(CustomSignupForm, self).save(request)
        # フォームに入力された値をUserモデルのフィールドに保存
        user.tel = self.cleaned_data.get('tel')
        user.date_of_birth = self.cleaned_data.get('date_of_birth')
        user.save()
        return user
