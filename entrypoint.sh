#!/bin/bash
set -e

REGION="ap-northeast-1"
SECRET_MAPS="stp00/google-maps-api-keys"

# 環境変数 APP_ENV で検証/本番を切り替え（stg or prod）
APP_ENV=${APP_ENV:-prod}
SECRET_DB="stp00/${APP_ENV}/db-credentials"

echo "🔐 Fetching secrets from AWS Secret Manager... (ENV: ${APP_ENV})"

# Google Maps APIキー取得
MAPS_SECRET=$(aws secretsmanager get-secret-value \
  --secret-id "$SECRET_MAPS" \
  --region "$REGION" \
  --query SecretString \
  --output text)

# DB認証情報取得
DB_SECRET=$(aws secretsmanager get-secret-value \
  --secret-id "$SECRET_DB" \
  --region "$REGION" \
  --query SecretString \
  --output text)

# 環境変数にエクスポート
export LTSIPLimitKey=$(echo $MAPS_SECRET | python3 -c "import sys,json; print(json.load(sys.stdin)['LTSIPLimitKey'])")
export LTSHttpLimitKey=$(echo $MAPS_SECRET | python3 -c "import sys,json; print(json.load(sys.stdin)['LTSHttpLimitKey'])")
export DB_USER=$(echo $DB_SECRET | python3 -c "import sys,json; print(json.load(sys.stdin)['DB_USER'])")
export DB_PASSWORD=$(echo $DB_SECRET | python3 -c "import sys,json; print(json.load(sys.stdin)['DB_PASSWORD'])")

echo "✅ Secrets loaded successfully"

exec "$@"
