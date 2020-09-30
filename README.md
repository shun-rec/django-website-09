# djangoチュートリアル #9 ログイン

## 最小コードで実用的なログインを作ろう！

## 完成版プロジェクト

<https://github.com/shun-rec/django-website-09>

## 事前準備

### 新規プロジェクト

```py
django-admin startproject pj_login
```

### 新規アプリの作成

何でも良いですが、今回はdjangoのデフォルトのアカウント周りのアプリ名に合わせて`registration`とします。

```py
cd pj_form
python manage.py startapp registration
```

### ドメインの許可

全体設定`pj_login/settings.py`の28行目を以下のように修正。

* これを追加しないとブラウザで開いた時に、「このドメインではアクセス出来ません。」というエラーが出ます。
* 本番では自分のドメインを設定してください。

```py
ALLOWED_HOSTS = ["*"]
```

### アプリを追加

同じく全体設定33行目の`INSTALLED_APPS`の配列の**最初**に`registration`アプリを追加。

* djangoは上から順にテンプレートを探します。下に追加してしまうとデフォルトの`admin`アプリのテンプレートが表示されてしまいます。

```py
    'registration',
```

### スーパーユーザーを作成

今回はメールアドレスも設定してください。  
値は何でもOKです。

```sh
python manage.py createsuperuser
```

* ユーザー名: admin
* メールアドレス: dev@example.com
* パスワード: admin

### ベースのテンプレートの作成

前回と同じく[Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)を使っています。

`registration/templates/base.html`

```html
<!doctype HTML>
<html>
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <a class="navbar-brand" href="/">アカウント管理</a>
        </nav>
        <div class="container mt-4">
        {% block main %}
        <p>※コンテンツがありません。</p>
        {% endblock %}
        </div>
    </body>
</html>
```

### ログインが必要なページの作成

ログイン出来たことが分かりやすいように会員専用ページを作ります。  
ログインしていない場合はログインページに移動します。

`registration/templates/registration/index.html`を以下の内容で作成。

```html
{% extends "base.html" %}
{% block main %}
<h1>{{ user }}さん、こんにちは！</h1>

<p><a href="{% url 'logout' %}">ログアウト</a></p>
<p><a href="{% url 'password_change' %}">パスワードの変更</a></p>
<p><a href="{% url 'password_reset' %}">パスワードを忘れた場合</a></p>
{% endblock %}
```

## ログイン/ログアウト画面を作ろう

### URLの設定

`pj_login/urls.py`を以下に変更。

```py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView

# 実はページを表示するだけならこのように1行で書くことが出来ます。
index_view = TemplateView.as_view(template_name="registration/index.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", login_required(index_view), name="index"),
    path('', include("django.contrib.auth.urls")),
]
```

* login_requiredでビューを囲むとログイン必須のページが作れます。
* この１行でdjangoでデフォルトで用意している以下がすべて入ります。（新規登録はありません）
  * ログイン
  * ログアウト
  * パスワード変更
  * パスワード再発行

### 全体設定の設定

`pj_login/settings.py`の末尾に以下を追加。

```py
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"
```

* EMAIL_BACKEND: メールシステムを実際に使うのは少し手間なので開発用にコンソールでメールをシミュレーションします。
* LOGIN_URL: ログインが必要な場合の移動先URL
* LOGIN_REDIRECT_URL: ログインに成功した場合の移動先URL
* LOGOUT_REDIRECT_URL: ログアウト後の移動先URL

### 確認してみよう

djangoがデフォルトで用意しているページが表示されたらOKです。

## テンプレートをカスタマイズしよう

### ログイン

### パスワード変更

### パスワード再発行
