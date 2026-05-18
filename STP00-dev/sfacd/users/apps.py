from django.apps import AppConfig


class UsersAppConfig(AppConfig):

    name = "sfacd.users"
    verbose_name = "Users"

    def ready(self):
        try:
            import users.signals  # noqa F401
        except ImportError:
            pass

        # Django 4.x対応：アプリ初期化完了後にadmin.site.loginを上書き
        from django.contrib import admin
        from django.contrib.auth.decorators import login_required
        admin.site.login = login_required(admin.site.login)
