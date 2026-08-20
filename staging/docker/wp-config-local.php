<?php
define( 'DB_NAME', getenv( 'WORDPRESS_DB_NAME' ) ?: 'camden_smoke' );
define( 'DB_USER', getenv( 'WORDPRESS_DB_USER' ) ?: 'camden_smoke' );
define( 'DB_PASSWORD', getenv( 'WORDPRESS_DB_PASSWORD' ) ?: 'disposable-local-only' );
define( 'DB_HOST', getenv( 'WORDPRESS_DB_HOST' ) ?: 'database' );
define( 'DB_CHARSET', 'utf8mb4' );
define( 'DB_COLLATE', '' );

define( 'AUTH_KEY', 'disposable-local-auth-key-stage-11' );
define( 'SECURE_AUTH_KEY', 'disposable-local-secure-auth-key-stage-11' );
define( 'LOGGED_IN_KEY', 'disposable-local-logged-in-key-stage-11' );
define( 'NONCE_KEY', 'disposable-local-nonce-key-stage-11' );
define( 'AUTH_SALT', 'disposable-local-auth-salt-stage-11' );
define( 'SECURE_AUTH_SALT', 'disposable-local-secure-auth-salt-stage-11' );
define( 'LOGGED_IN_SALT', 'disposable-local-logged-in-salt-stage-11' );
define( 'NONCE_SALT', 'disposable-local-nonce-salt-stage-11' );

$table_prefix = 'wp_';

define( 'WP_ENVIRONMENT_TYPE', 'staging' );
define( 'WP_HOME', 'http://127.0.0.1:8088' );
define( 'WP_SITEURL', 'http://127.0.0.1:8088' );
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
define( 'SCRIPT_DEBUG', true );
define( 'WP_MEMORY_LIMIT', '512M' );
define( 'WP_MAX_MEMORY_LIMIT', '512M' );
define( 'DISALLOW_FILE_EDIT', true );
define( 'AUTOMATIC_UPDATER_DISABLED', true );

@ini_set( 'display_errors', 0 );

if ( ! defined( 'ABSPATH' ) ) {
    define( 'ABSPATH', __DIR__ . '/' );
}

require_once ABSPATH . 'wp-settings.php';
