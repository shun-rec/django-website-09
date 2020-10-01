# djangoチュートリアル #9 ログイン

## 最小コードで実用的なログインを作ろう！

## 完成版プロジェクト

<https://github.com/shun-rec/django-website-09>

## 事前準備

### 新規プロジェクト

```py
django-admin startproject pj_login
cd pj_login
```

### 新規アプリの作成

名前は何でも良いですが、今回はdjangoのデフォルトのアカウント周りのアプリ名に合わせて`registration`とします。

```py
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

### データベースの作成

djagnoのユーザーモデルを使うので、データベースを作成します。

```sh
python manage.py migrate
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
<h2>会員ページ</h2>
<p>{{ user }}さん、こんにちは！</p>

<p><a href="{% url 'logout' %}">ログアウト</a></p>
<p><a href="{% url 'password_change' %}">パスワードの変更</a></p>
<p><a href="{% url 'password_reset' %}">パスワードを忘れた場合</a></p>
{% endblock %}
```

## ログイン/ログアウトを作ろう

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

ページが`https`の環境では、最後に以下も追記してください。  
メールで送られるURLが`http`ではなく`https`になります。

```py
# 暗号化されたhttpsを使うようにする
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
```

### ログイン画面のテンプレートを作ろう

#### 共通のフォーム部分を作ろう

フォーム部分のHTMLはいくつかのページで使うので共通のものを１つ作っておきます。

`registration/templates/_form.html`を以下内容で新規作成します。

* submit_labelにボタンのラベルを渡してカスタマイズ出来るフォームです。

```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="{{ submit_label }}" />
</form>
```

#### ログイン画面のテンプレートを作ろう

`registration/templates/registration/login.html`を以下内容で新規作成します。

```html
{% extends "base.html" %}
{% block main %}
<h2>ログイン</h2>
{% include "_form.html" with submit_label="ログイン" %}
{% endblock %}
```

### 確認してみよう

* トップ画面がログイン必須
* ログイン画面が自分で用意したデザイン
* その他の画面はdjangoデフォルトのデザイン

であればOKです。

## テンプレートをカスタマイズしよう

指定された場所にテンプレートを作るだけでそれらが使われるようになります。

### パスワード変更(password_change)

`registration/templates/registration/password_change_form.html`

```html
{% extends "base.html" %}
{% block main %}
<h2>パスワード変更</h2>
{% include "_form.html" with submit_label="変更" %}
{% endblock %}
```

### パスワード変更完了(password_change_done)

`registration/templates/registration/password_change_done.html`

```html
{% extends "base.html" %}
{% block main %}
<h2>パスワード変更完了</h2>
<p>パスワードの変更が完了しました。</p>
{% endblock %}
```

### パスワード再発行(password_reset)

`registration/templates/registration/password_reset_form.html`

```html
{% extends "base.html" %}
{% block main %}
<h2>パスワード再設定</h2>
{% include "_form.html" with submit_label="送信" %}
{% endblock %}
```

### パスワード再発行完了(password_reset_done)

`registration/templates/registration/password_reset_done.html`

```html
{% extends "base.html" %}
{% block main %}
<h2>パスワード再設定メール送信完了</h2>
<p>パスワード再設定メールを送信しました。</p>
{% endblock %}
```

### パスワード再設定(password_reset_confirm)

`registration/templates/registration/password_reset_confirm.html`

```html
{% extends "base.html" %}
{% block main %}
<h2>パスワード再設定</h2>

{% if validlink %}
    {% include "_form.html" with submit_label="変更" %}
{% else %}
    <p>無効なリンクです。</p>
{% endif %}

{% endblock %}
```

### パスワード再設定完了(password_reset_complete)

`registration/templates/registration/password_reset_complete.html`

```html
{% extends "base.html" %}
{% block main %}
<h2>パスワード再設定完了</h2>
<p>パスワードの再設定が完了しました。</p>
<p><a href="{% url 'login' %}">ログイン</a></p>
{% endblock %}
```

### 確認しよう

すべての画面のデザインが変わっていればOKです。
