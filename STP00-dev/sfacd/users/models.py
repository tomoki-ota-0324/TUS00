from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
# from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from sfacd.gis.models import Shop2, Department


class CustomUserManager(BaseUserManager):
    """
    Define a model manager gor User model with no username field
    """
    use_in_migrations = True
    
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password
        """
        if not email:
            raise ValueError('The given email must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save areguler User with the given email and password
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save SuperUser with the givin email and password
        """
        extra_fields.setdefault('is_staff,', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuesr must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

# class AbstractUser(AbstractBaseUser, PermissionsMixin):
#     """
#     An abstract base class implementing a fully featured User model with
#     admin-compliant permissions.
#     Username and password are required. Other fields are optional.
#     """
#     # username_validator = UnicodeUsernameValidator()

#     # username = models.CharField(
#     #     _('username'),
#     #     max_length=150,
#     #     unique=True,
#     #     help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#     #     validators=[username_validator],
#     #     error_messages={
#     #         'unique': _("A user with that username already exists."),
#     #     },
#     # )
#     # first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     # last_name = models.CharField(_('last name'), max_length=150, blank=True)
#     email = models.EmailField(_('email address'), blank=True)
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_('Designates whether the user can log into this admin site.'),
#     )
#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

#     # objects = UserManager()

#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['email']

#     class Meta:
#         verbose_name = _('user')
#         verbose_name_plural = _('users')

#     def clean(self):
#         super().clean()
#         self.email = self.__class__.objects.normalize_email(self.email)

#     def get_full_name(self):
#         """
#         Return the first_name plus the last_name, with a space in between.
#         """
#         full_name = self.name
#         return full_name.strip()

#     def get_short_name(self):
#         """Return the short name for the user."""
#         return self.name

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)

#     @property
#     def username(self):
#         """username属性のゲッター

#         他アプリケーションが、username属性にアクセスした場合に備えて定義
#         メールアドレスを返す
#         """
#         return self.email

class User(AbstractUser):
    """"
    拡張ユーザーモデル
    djangoデフォルトのusernameをなくし、idの自動連番をなくす
    """
    class Meta(AbstractUser.Meta):
        db_table = 'users_user'
        verbose_name_plural = 'ユーザーマスタデータ'

    id = models.IntegerField('従業員番号', primary_key=True, help_text="半角数字で入力してください。")
    username = models.CharField('その他', max_length=100, blank=True, default="")
    email = models.EmailField('メールアドレス', unique=True, help_text='メールアドレスはユニーク(一意)でなければいけません。')
    objects = CustomUserManager()
    name = models.CharField('従業員名', max_length=100)
    shop = models.ForeignKey(Shop2, on_delete=models.SET_NULL, null=True, verbose_name='所属店舗')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name='業務グループ',
        help_text='ここで選ばれた業務グループに商圏分析権限が付与されていると商圏機能にアクセスができます。\n業務を入力しない場合は不明を選択してください。')
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_staff = models.BooleanField('管理サイトアクセス許可', default=False, help_text=_('Designates whether the user can log into this admin site.'),)

    def __str__(self):
        return self.name

    #データベースの作り直し時にmakemigrationsでエラーが出る場合、CustomUserが影響しているように見える
    #修正：ローカルブランチcustomuserでならうまく動作するので、customUserブランチに切り替えて、makemigrationsする
    #その後、メインブランチにもどして、動作確認
