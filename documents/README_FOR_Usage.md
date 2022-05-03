## Installation for DEMO
DEMO実行のための開発環境作成方法を記載する。

##### Install Development Tools
下記の開発ツールをインストールする。

- [Docker for Desktop](https://www.docker.com/products/docker-desktop/)
- [VS Code](https://azure.microsoft.com/ja-jp/products/visual-studio-code/)
- [Git](https://git-scm.com/book/ja/v2/%E4%BD%BF%E3%81%84%E5%A7%8B%E3%82%81%E3%82%8B-Git%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB)

##### Setup VS Code
VS Codeを起動し、下記の拡張機能をインストールする。

- Docker
- Remote - Containers
- Japanese Language Pack for Visual Studio Code (optional)

##### Clone this repository 
ソースコードをクローンする。

```bash
git clone https://github.com/kchihogi/portfolio.git
```

##### Docker Build
Docker上で開発環境をDockerビルドする。

1. VS Codeを起動し、クローンしたリポジトリのフォルダを開く。
2. 左下のリモートウィンドウを開くアイコンをクリック。
3. Open Floder in Container... を選択。
4. webフォルダを選択し、Open。

note: Dockerビルドには時間がかかります。

##### Setup DB and Run Server
DBのマイグレーションとサーバーの立ち上げを行う。

- Dockerビルド後、起動したVS Codeからbashを開く。
```bash
cd web/site
python manage.py makemigrations portfolio
python manage.py migrate
python manage.py runserver
```

##### Access

- Web site: http://127.0.0.1:8000/portfolio/
- DB: http://127.0.0.1:8080/
