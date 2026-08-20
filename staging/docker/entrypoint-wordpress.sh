#!/bin/sh
set -eu

if [ ! -f /var/www/html/wp-includes/version.php ]; then
    cp -a /usr/src/wordpress/. /var/www/html/
fi

if [ ! -f /var/www/html/wp-config.php ]; then
    cp /usr/local/share/wp-config-local.php /var/www/html/wp-config.php
fi

if [ -f /var/www/html/index.html ] && grep -q 'Apache2 Debian Default Page' /var/www/html/index.html; then
    rm /var/www/html/index.html
fi

cp /usr/local/share/robots.txt /var/www/html/robots.txt

if [ ! -f /var/www/html/.htaccess ]; then
    cp /usr/local/share/wordpress-htaccess /var/www/html/.htaccess
fi

mkdir -p /var/www/html/wp-content/uploads /var/www/html/wp-content/upgrade
chown -R www-data:www-data /var/www/html 2>/dev/null || true

exec apachectl -D FOREGROUND
