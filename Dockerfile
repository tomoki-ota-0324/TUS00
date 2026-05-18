FROM python:3.13

# 元々の設定：ロケール・vim・ディレクトリ作成
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get install -y locales vim \
    # AWS CLI に必要なパッケージを追加
    curl unzip \
    && mkdir /src \
    && mkdir /src/STP00-dev \
    && rm -rf /var/lib/apt/lists/* \
    && echo "ja_JP UTF-8" > /etc/locale.gen \
    && locale-gen

# AWS CLI インストール
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws

# 元々の設定：Python出力バッファ無効化
ENV PYTHONUNBUFFERED 1

# 元々の設定：ソースコードコピー
COPY --chown=root:root ./STP00-dev /src/STP00-dev

# entrypoint.sh をコピーして実行権限付与
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 元々の設定：作業ディレクトリ
WORKDIR /src/STP00-dev

# 元々の設定：依存パッケージインストール
RUN pip install -r requirements/local.txt

ENTRYPOINT ["/entrypoint.sh"]

# 元々の設定：起動コマンド
CMD ["python"]
