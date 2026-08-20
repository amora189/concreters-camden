<?php
/**
 * Plugin Name: Camden authoritative staging — enforced noindex
 * Description: Global noindex that cannot be switched off from wp-admin. Stage 29, §4.29.1.
 *
 * A must-use plugin, so it cannot be deactivated through the UI. This is the
 * last line of defence against an authoritative staging site being indexed
 * while it carries unfinished copy, unverified business facts and placeholder
 * markers.
 *
 * This does NOT replace per-page robots directives. Wave release still works
 * page by page on the live host. This only guarantees that staging itself is
 * never indexable, whatever anyone clicks.
 */

defined( 'ABSPATH' ) || exit;

// 1. Force the blog_public option off on every read.
add_filter( 'pre_option_blog_public', static fn() => '0' );

// 2. Emit an explicit robots meta on every response.
add_filter(
	'wp_robots',
	static function ( array $robots ): array {
		$robots['noindex']   = true;
		$robots['nofollow']  = true;
		$robots['noarchive'] = true;
		$robots['nosnippet'] = true;
		unset( $robots['index'], $robots['follow'] );
		return $robots;
	},
	PHP_INT_MAX
);

// 3. Send X-Robots-Tag as a header too, so non-HTML responses are covered.
add_action(
	'send_headers',
	static function (): void {
		header( 'X-Robots-Tag: noindex, nofollow, noarchive, nosnippet', true );
	},
	PHP_INT_MAX
);

// 4. Serve a blanket disallow robots.txt regardless of any plugin's opinion.
add_filter(
	'robots_txt',
	static fn(): string => "User-agent: *\nDisallow: /\n",
	PHP_INT_MAX
);

// 5. Refuse to emit a sitemap from staging.
add_filter( 'wp_sitemaps_enabled', '__return_false', PHP_INT_MAX );

// 6. Hard block on remote media fetching, belt and braces with
//    WP_HTTP_BLOCK_EXTERNAL. Standing rule 3: no remote media, ever.
add_filter(
	'pre_http_request',
	static function ( $preempt, $args, $url ) {
		$host = wp_parse_url( $url, PHP_URL_HOST );
		if ( in_array( $host, array( 'localhost', '127.0.0.1', 'db', 'wordpress' ), true ) ) {
			return $preempt;
		}
		return new WP_Error(
			'camden_remote_blocked',
			sprintf( 'Remote request to %s blocked by authoritative staging policy.', $url )
		);
	},
	PHP_INT_MAX,
	3
);

// 7. Loud admin notice so nobody mistakes this for production.
add_action(
	'admin_notices',
	static function (): void {
		echo '<div class="notice notice-error"><p><strong>AUTHORITATIVE STAGING.</strong> '
			. 'Global noindex is enforced by a must-use plugin and cannot be disabled here. '
			. 'This is not the live site.</p></div>';
	}
);
