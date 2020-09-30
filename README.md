# djangoチュートリアル #10 サインアップ/ログイン

## 最小コードで実用的なサインアップ/ログインを作ろう！

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

## ログイン/ログアウト画面を作ろう

### URLの設定

