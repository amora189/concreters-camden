FROM careerpulse-careerpulse:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apache2 \
        ca-certificates \
        curl \
        libapache2-mod-php \
        mariadb-client \
        mariadb-server \
        php \
        php-cli \
        php-curl \
        php-gd \
        php-imagick \
        php-intl \
        php-mbstring \
        php-mysql \
        php-xml \
        php-zip \
        unzip \
    && rm -rf /var/lib/apt/lists/*

RUN a2enmod headers rewrite \
    && printf '%s\n' \
        '<Directory /var/www/html>' \
        '    Options FollowSymLinks' \
        '    AllowOverride All' \
        '    Require all granted' \
        '    <Files "debug.log">' \
        '        Require all denied' \
        '    </Files>' \
        '</Directory>' \
        'Header always set X-Robots-Tag "noindex, nofollow, noarchive"' \
        'ServerName localhost' \
        > /etc/apache2/conf-available/camden-local-staging.conf \
    && a2enconf camden-local-staging \
    && printf '%s\n' \
        'memory_limit=512M' \
        'upload_max_filesize=64M' \
        'post_max_size=64M' \
        'max_execution_time=300' \
        'display_errors=Off' \
        'log_errors=On' \
        > /etc/php/8.4/apache2/conf.d/99-camden-staging.ini \
    && cp /etc/php/8.4/apache2/conf.d/99-camden-staging.ini /etc/php/8.4/cli/conf.d/99-camden-staging.ini

COPY vendor/wordpress-7.0.4.tar.gz /tmp/wordpress.tar.gz
COPY vendor/wp-cli.phar /usr/local/bin/wp

RUN mkdir -p /usr/src/wordpress \
    && tar -xzf /tmp/wordpress.tar.gz -C /usr/src/wordpress --strip-components=1 \
    && rm /tmp/wordpress.tar.gz \
    && chmod 0755 /usr/local/bin/wp

COPY docker/wp-config-local.php /usr/local/share/wp-config-local.php
COPY docker/robots.txt /usr/local/share/robots.txt
COPY docker/wordpress-htaccess /usr/local/share/wordpress-htaccess
COPY docker/entrypoint-wordpress.sh /usr/local/bin/entrypoint-wordpress.sh
COPY docker/entrypoint-database.sh /usr/local/bin/entrypoint-database.sh

RUN chmod 0755 /usr/local/bin/entrypoint-wordpress.sh /usr/local/bin/entrypoint-database.sh

WORKDIR /var/www/html

EXPOSE 80
