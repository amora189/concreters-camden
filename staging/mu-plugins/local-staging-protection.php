<?php
/**
 * Plugin Name: Camden Local Staging Protection
 * Description: Enforces non-indexing and blocks non-loopback hosts on the disposable smoke-test site.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

add_filter(
    'wp_robots',
    static function ( array $robots ): array {
        $robots['noindex'] = true;
        $robots['nofollow'] = true;
        $robots['noarchive'] = true;
        unset( $robots['index'], $robots['follow'] );

        return $robots;
    }
);

add_filter(
    'robots_txt',
    static function (): string {
        return "User-agent: *\nDisallow: /\n";
    },
    999
);

add_action(
    'plugins_loaded',
    static function (): void {
        $host = strtolower( (string) ( $_SERVER['HTTP_HOST'] ?? '' ) );
        $allowed = array( '127.0.0.1:8088', 'localhost:8088' );

        if ( $host !== '' && ! in_array( $host, $allowed, true ) ) {
            status_header( 403 );
            nocache_headers();
            exit( 'Local staging access only.' );
        }
    },
    0
);
