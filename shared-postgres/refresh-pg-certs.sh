#!/usr/bin/env bash
# Copia el cert de Let's Encrypt (poke.servegame.com) a un dir legible por el usuario
# postgres del contenedor (uid 999). privkey.pem es root-only => este script corre con sudo.
# Lo usa el deploy-hook de certbot tras cada renovación (ver /etc/letsencrypt/renewal-hooks).
set -euo pipefail
LIVE=/etc/letsencrypt/live/poke.servegame.com
DEST=/home/felipe/shared-postgres/certs
mkdir -p "$DEST"
cp -L "$LIVE/fullchain.pem" "$DEST/server.crt"
cp -L "$LIVE/privkey.pem"   "$DEST/server.key"
chown 999:999 "$DEST/server.crt" "$DEST/server.key"
chmod 644 "$DEST/server.crt"
chmod 600 "$DEST/server.key"
echo "pg certs refreshed -> $DEST"
