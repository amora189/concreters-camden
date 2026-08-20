#!/bin/sh
set -eu

datadir=/var/lib/mysql
socket=/run/mysqld/mysqld.sock
db_name=${MARIADB_DATABASE:-camden_smoke}
db_user=${MARIADB_USER:-camden_smoke}
db_password=${MARIADB_PASSWORD:-disposable-local-only}

mkdir -p "$datadir" /run/mysqld
chown -R mysql:mysql "$datadir" /run/mysqld

if [ ! -d "$datadir/mysql" ]; then
    mariadb-install-db --user=mysql --datadir="$datadir" --skip-test-db

    mariadbd --user=mysql --datadir="$datadir" --socket="$socket" --skip-networking &
    temporary_pid=$!

    attempts=0
    until mariadb-admin --socket="$socket" --user=root ping --silent; do
        attempts=$(( attempts + 1 ))
        if [ "$attempts" -ge 60 ]; then
            kill "$temporary_pid" || true
            exit 1
        fi
        sleep 1
    done

    mariadb --socket="$socket" --user=root <<SQL
CREATE DATABASE IF NOT EXISTS \`$db_name\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS '$db_user'@'%' IDENTIFIED BY '$db_password';
ALTER USER '$db_user'@'%' IDENTIFIED BY '$db_password';
GRANT ALL PRIVILEGES ON \`$db_name\`.* TO '$db_user'@'%';
FLUSH PRIVILEGES;
SQL

    mariadb-admin --socket="$socket" --user=root shutdown
    wait "$temporary_pid"
fi

exec mariadbd \
    --user=mysql \
    --datadir="$datadir" \
    --socket="$socket" \
    --bind-address=0.0.0.0 \
    --transaction-isolation=READ-COMMITTED \
    --binlog-format=ROW
