<?php
/**
 * Fail-closed post-import database/rendered-output verification.
 *
 * Execute only through verify-post-import.sh after an authorised staging
 * import.  This file performs no mutation.  It requires WordPress to be loaded
 * by `wp eval-file` and exits non-zero on any failed assertion.
 */

defined( 'ABSPATH' ) || exit( 2 );

global $wpdb;

$allowlist_path = $args[0] ?? '';
$claims_path    = $args[1] ?? '';
$menu_path      = $args[2] ?? '';
$media_path     = $args[3] ?? '';

$read_json = static function ( string $path ): array {
	if ( ! is_readable( $path ) ) {
		throw new RuntimeException( "Required control is unreadable: {$path}" );
	}
	$value = json_decode( file_get_contents( $path ), true, 512, JSON_THROW_ON_ERROR );
	if ( ! is_array( $value ) ) {
		throw new RuntimeException( "Required control is not a JSON object: {$path}" );
	}
	return $value;
};

$normalise = static function ( string $value ): string {
	$value = html_entity_decode( wp_strip_all_tags( $value ), ENT_QUOTES | ENT_HTML5, 'UTF-8' );
	return trim( preg_replace( '/\s+/u', ' ', $value ) );
};

$failures = array();
$passes   = array();
$evidence = array();
$assert   = static function ( bool $condition, string $name, $detail ) use ( &$failures, &$passes ): void {
	$row = array( 'assertion' => $name, 'detail' => $detail );
	if ( $condition ) {
		$passes[] = $row;
	} else {
		$failures[] = $row;
	}
};

try {
	$allowlist   = $read_json( $allowlist_path );
	$claim_gate  = $read_json( $claims_path );
	$menu_policy = $read_json( $menu_path );
	$media       = $read_json( $media_path );

	$expected = array();
	foreach ( $allowlist['pages'] as $page ) {
		$expected[ (int) $page['page_id'] ] = $page;
	}
	$expected_ids = array_keys( $expected );
	sort( $expected_ids, SORT_NUMERIC );

	// 1. Exact active architecture. Additional pages fail even if draft.
	$actual_ids = $wpdb->get_col( "SELECT ID FROM {$wpdb->posts} WHERE post_type = 'page' ORDER BY ID ASC" ); // phpcs:ignore WordPress.DB.PreparedSQL.NotPrepared
	$actual_ids = array_map( 'intval', $actual_ids );
	sort( $actual_ids, SORT_NUMERIC );
	$missing    = array_values( array_diff( $expected_ids, $actual_ids ) );
	$additional = array_values( array_diff( $actual_ids, $expected_ids ) );
	$assert( empty( $missing ) && empty( $additional ), 'active page inventory exact', compact( 'missing', 'additional' ) );
	$assert( ! in_array( 1600, $missing, true ) && get_post_field( 'post_name', 1600 ) === 'privacy-policy', 'privacy page present', array( 'post_id' => 1600 ) );
	$assert( ! file_exists( ABSPATH . 'camden-calculator-import.xml' ) && empty( array_filter( $actual_ids, static fn( int $id ): bool => str_contains( (string) get_post_field( 'post_name', $id ), 'crossover-requirements' ) ) ), 'calculator absent until built', array( 'calculator_artifact' => 'absent by current control' ) );

	foreach ( $expected as $id => $page ) {
		$post = get_post( $id );
		if ( ! $post ) {
			continue;
		}
		$assert( $post->post_name === $page['slug'], "page {$id} slug", array( 'expected' => $page['slug'], 'actual' => $post->post_name ) );
		$assert( $post->post_status === $page['intended_status'], "page {$id} intended status", array( 'expected' => $page['intended_status'], 'actual' => $post->post_status ) );
	}

	// 2. Astra wp_css exclusion. D32 made all local-work-card rules dead and
	// the import plan excludes the wp_css record rather than creating an empty
	// public custom_css post.
	$css = get_post( 893 );
	$assert( ! $css || $css->post_type !== 'custom_css', 'Astra wp_css excluded / custom CSS post 893 absent', $css ? $css->post_type : 'absent' );
	$assert( (int) get_theme_mod( 'custom_css_post_id', 0 ) !== 893 && (int) get_option( 'custom_css_post_id', 0 ) !== 893, 'excluded custom_css_post_id is not assigned', array( 'theme_mod' => get_theme_mod( 'custom_css_post_id', 0 ), 'option' => get_option( 'custom_css_post_id', 0 ) ) );
	$assert( ! preg_match( '/Werribee/i', wp_json_encode( get_theme_mods() ) ), 'excluded Astra wp_css absent from imported theme mods', array_keys( get_theme_mods() ) );

	// 3. Menus are verified in the resulting database, not in the plan.
	$locations = get_nav_menu_locations();
	foreach ( $menu_policy['locations'] as $location => $policy ) {
		$term_id = (int) $policy['term_id'];
		$actual  = isset( $locations[ $location ] ) ? (int) $locations[ $location ] : 0;
		$assert( $actual === $term_id, "menu location {$location}", array( 'expected' => $term_id, 'actual' => $actual ) );
		$items = wp_get_nav_menu_items( $term_id, array( 'post_status' => 'any' ) );
		$assert( is_array( $items ) && count( $items ) === (int) $policy['retained_items'], "menu {$location} pruned count", array( 'expected' => $policy['retained_items'], 'actual' => is_array( $items ) ? count( $items ) : null ) );
		$expected_items = $menu_policy['retained_items'][ $policy['menu_name'] ];
		$expected_menu_contract = array_map(
			static fn( array $item ): array => array(
				'post_id'   => (int) $item['post_id'],
				'object'    => $item['object'],
				'object_id' => (string) $item['object_id'],
			),
			$expected_items
		);
		$actual_menu_contract = is_array( $items ) ? array_map(
			static fn( WP_Post $item ): array => array(
				'post_id'   => (int) $item->ID,
				'object'    => $item->object,
				'object_id' => (string) $item->object_id,
			),
			$items
		) : array();
		$assert( $actual_menu_contract === $expected_menu_contract, "menu {$location} exact retained targets/order", array( 'expected' => $expected_menu_contract, 'actual' => $actual_menu_contract ) );
	}
	$assigned_terms = array_map( 'intval', array_values( $locations ) );
	foreach ( $menu_policy['unassigned'] as $policy ) {
		$assert( ! in_array( (int) $policy['term_id'], $assigned_terms, true ), "menu term {$policy['term_id']} remains unassigned", $assigned_terms );
	}

	// 4. Denied attachments do not exist as public attachment records.
	$denied_ids = array_unique(
		array_merge(
			array_map( 'intval', $media['retired_brand_ids'] ),
			array_map( 'intval', $media['band_b_unusable_ids'] ),
			array_map( 'intval', $media['band_a_denied_ids'] ),
			array_map( 'intval', $media['other_excluded_ids'] ),
			array_map( 'intval', array_keys( $media['unauthorised_ai_ids'] ) )
		)
	);
	foreach ( $denied_ids as $attachment_id ) {
		$post = get_post( $attachment_id );
		$assert( ! $post || $post->post_type !== 'attachment', "denied attachment {$attachment_id} unavailable", $post ? $post->post_type : 'absent' );
		$assert( ! wp_get_attachment_url( $attachment_id ), "denied attachment {$attachment_id} has no public URL", wp_get_attachment_url( $attachment_id ) );
	}
	$uploads = wp_get_upload_dir();
	foreach ( $media['denied_assets'] as $asset ) {
		$filenames = isset( $asset['forbidden_filenames'] ) ? $asset['forbidden_filenames'] : array( $asset['filename'] );
		foreach ( $filenames as $filename ) {
			$matches = glob( trailingslashit( $uploads['basedir'] ) . '*/*/' . $filename );
			$assert( empty( $matches ), "denied media binary {$filename} absent from public uploads", $matches ?: array() );
		}
	}
	foreach ( $media['generic_assets'] as $asset ) {
		$attachment_id = (int) $asset['attachment_id'];
		$file = get_attached_file( $attachment_id );
		$alt = get_post_meta( $attachment_id, '_wp_attachment_image_alt', true );
		$assert( $file && wp_basename( $file ) === $asset['target_filename'], "generic attachment {$attachment_id} uses remediated filename", array( 'expected' => $asset['target_filename'], 'actual' => $file ? wp_basename( $file ) : null ) );
		$assert( $alt === $asset['target_alt'], "generic attachment {$attachment_id} uses visible-only alt text", array( 'expected' => $asset['target_alt'], 'actual' => $alt ) );
	}
	$custom_logo_id = (int) get_theme_mod( 'custom_logo', 0 );
	$site_icon_id   = (int) get_option( 'site_icon', 0 );
	$assert( $custom_logo_id > 0 && wp_basename( (string) get_attached_file( $custom_logo_id ) ) === 'structure-co-horizontal.svg', 'replaced header logo slot uses Structure Co horizontal wordmark', array( 'attachment_id' => $custom_logo_id, 'file' => get_attached_file( $custom_logo_id ) ) );
	$assert( $site_icon_id > 0 && wp_basename( (string) get_attached_file( $site_icon_id ) ) === 'structure-co-icon-512.png', 'replaced favicon slot uses Structure Co icon', array( 'attachment_id' => $site_icon_id, 'file' => get_attached_file( $site_icon_id ) ) );

	// 5. Collect exact visible DB fields and Elementor media references.
	$visible_by_page = array();
	$rendered_by_page = array();
	$raw_rendered_by_page = array();
	$unresolved_media = array();
	$denied_slot_hits = array();
	$visible_keys = array_flip(
		array( 'editor', 'title', 'title_text', 'heading_title', 'description_text', 'text', 'html', 'testimonial_content', 'testimonial_name', 'testimonial_job', 'item_description', 'item_title', 'tab_content', 'tab_title', 'content', 'caption', 'alt', 'before_text', 'highlighted_text', 'after_text', 'inner_text', 'list_item_text', 'accordion_content', 'toggle_content', 'value' )
	);
	$generic_by_id = array_column( $media['generic_assets'], null, 'attachment_id' );
	$walk = function ( $node, int $page_id, string $path = '$' ) use ( &$walk, &$visible_by_page, &$unresolved_media, &$denied_slot_hits, $visible_keys, $denied_ids, $generic_by_id, $normalise ): void {
		if ( ! is_array( $node ) ) {
			return;
		}
		$attachment_id = null;
		$media_url    = '';
		$typed_image  = false;
		if ( isset( $node['id'], $node['url'] ) && is_numeric( $node['id'] ) && is_string( $node['url'] ) && str_contains( $node['url'], 'wp-content/uploads' ) ) {
			$attachment_id = (int) $node['id'];
			$media_url = $node['url'];
		} elseif ( ( $node['$$type'] ?? '' ) === 'image' ) {
			$typed_id = $node['value']['src']['value']['id']['value'] ?? null;
			if ( is_numeric( $typed_id ) ) {
				$attachment_id = (int) $typed_id;
				$media_url = (string) ( $node['value']['src']['value']['url']['value'] ?? '' );
				$typed_image = true;
			}
		}
		if ( null !== $attachment_id ) {
			$post = get_post( $attachment_id );
			$file = get_attached_file( $attachment_id );
			if ( ! $post || $post->post_type !== 'attachment' || ! $file || ! file_exists( $file ) ) {
				$unresolved_media[] = array( 'page_id' => $page_id, 'attachment_id' => $attachment_id, 'path' => $path, 'file' => $file );
			}
			if ( in_array( $attachment_id, $denied_ids, true ) ) {
				$denied_slot_hits[] = array( 'page_id' => $page_id, 'attachment_id' => $attachment_id, 'path' => $path );
			}
			if ( ! $typed_image && isset( $generic_by_id[ $attachment_id ] ) && wp_basename( wp_parse_url( $media_url, PHP_URL_PATH ) ) !== $generic_by_id[ $attachment_id ]['target_filename'] ) {
				$unresolved_media[] = array( 'page_id' => $page_id, 'attachment_id' => $attachment_id, 'path' => $path, 'reason' => 'Elementor URL does not use remediated filename' );
			}
		}
		foreach ( $node as $key => $value ) {
			$child_path = $path . '.' . (string) $key;
			if ( is_string( $value ) && isset( $visible_keys[ (string) $key ] ) ) {
				$text = $normalise( $value );
				if ( $text !== '' ) {
					$visible_by_page[ $page_id ][] = $text;
				}
			} elseif ( is_array( $value ) ) {
				$walk( $value, $page_id, $child_path );
			}
		}
	};

	foreach ( $expected_ids as $page_id ) {
		$post = get_post( $page_id );
		if ( ! $post ) {
			continue;
		}
		$visible_by_page[ $page_id ] = array( $normalise( $post->post_title ), $normalise( $post->post_content ) );
		$raw = get_post_meta( $page_id, '_elementor_data', true );
		if ( $raw !== '' ) {
			$data = json_decode( $raw, true );
			$assert( is_array( $data ), "page {$page_id} Elementor JSON parses", json_last_error_msg() );
			if ( is_array( $data ) ) {
				$walk( $data, $page_id );
			}
		}
		if ( class_exists( '\\Elementor\\Plugin' ) ) {
			$raw_rendered_by_page[ $page_id ] = \Elementor\Plugin::instance()->frontend->get_builder_content_for_display( $page_id, true );
		} else {
			$raw_rendered_by_page[ $page_id ] = apply_filters( 'the_content', $post->post_content );
		}
		$rendered_by_page[ $page_id ] = $normalise( $raw_rendered_by_page[ $page_id ] );
	}
	$assert( empty( $unresolved_media ), 'all Elementor media references resolve to local attachment files', $unresolved_media );
	$assert( empty( $denied_slot_hits ), 'unusable/retired media slots removed', $denied_slot_hits );

	// 6. Reader-visible CoreX/E&T and unsupported claims are absent from DB/render.
	$source_hits = array();
	foreach ( $visible_by_page as $page_id => $fields ) {
		foreach ( $fields as $text ) {
			if ( preg_match( '/CoreX|E(?:&amp;|&)T\s*Co|Camden based Concrete Company Site/i', $text ) ) {
				$source_hits[] = array( 'page_id' => $page_id, 'text' => $text );
			}
		}
		if ( preg_match( '/CoreX|E(?:&amp;|&)T\s*Co|Camden based Concrete Company Site/i', $rendered_by_page[ $page_id ] ?? '' ) ) {
			$source_hits[] = array( 'page_id' => $page_id, 'rendered' => true );
		}
	}
	$assert( empty( $source_hits ), 'reader-visible CoreX/E&T/tagline absent', $source_hits );
	$assert( get_option( 'blogname' ) === 'Structure Co Concreters Camden', 'WordPress site title exact', get_option( 'blogname' ) );
	$assert( ! preg_match( '/Camden based|CoreX|E(?:&amp;|&)T/i', (string) get_option( 'blogdescription' ) ), 'WordPress tagline contains no source/local-presence claim', get_option( 'blogdescription' ) );

	$unsupported_survivors = array();
	foreach ( $claim_gate['occurrences'] as $claim ) {
		if ( $claim['evidence_status'] !== 'UNSUPPORTED' ) {
			continue;
		}
		$page_id = (int) $claim['page_id'];
		$needle  = $normalise( $claim['exact_claim'] );
		foreach ( $visible_by_page[ $page_id ] ?? array() as $field ) {
			if ( $needle !== '' && str_contains( $field, $needle ) ) {
				$unsupported_survivors[] = array( 'claim_id' => $claim['claim_id'], 'page_id' => $page_id, 'placement' => $claim['placement'] );
				break;
			}
		}
	}
	$assert( empty( $unsupported_survivors ), 'no registered unsupported claim survives', $unsupported_survivors );

	// 7. Schema must follow the verified identity policy generated with the claims.
	$schema_failures = array();
	$schema_types_by_page = array();
	$service_nodes = 0;
	$provider_nodes = 0;
	$defined_ids_by_page = array();
	$referenced_ids_by_page = array();
	$walk_schema = function ( $node, int $page_id ) use ( &$walk_schema, &$schema_types_by_page, &$service_nodes, &$provider_nodes, &$defined_ids_by_page, &$referenced_ids_by_page ): void {
		if ( ! is_array( $node ) ) {
			return;
		}
		if ( array_is_list( $node ) ) {
			foreach ( $node as $child ) {
				$walk_schema( $child, $page_id );
			}
			return;
		}
		$types = isset( $node['@type'] ) ? (array) $node['@type'] : array();
		foreach ( $types as $type ) {
			if ( is_string( $type ) ) {
				$schema_types_by_page[ $page_id ][] = $type;
				if ( $type === 'Service' ) {
					$service_nodes++;
					if ( array_key_exists( 'provider', $node ) ) {
						$provider_nodes++;
					}
				}
			}
		}
		if ( isset( $node['@id'] ) && is_string( $node['@id'] ) ) {
			if ( $types ) {
				$defined_ids_by_page[ $page_id ][] = $node['@id'];
			} else {
				$referenced_ids_by_page[ $page_id ][] = $node['@id'];
			}
		}
		foreach ( $node as $child ) {
			if ( is_array( $child ) ) {
				$walk_schema( $child, $page_id );
			}
		}
	};
	foreach ( $raw_rendered_by_page as $page_id => $rendered ) {
		if ( preg_match_all( '#<script[^>]+application/ld\+json[^>]*>(.*?)</script>#is', $rendered, $matches ) ) {
			foreach ( $matches[1] as $blob ) {
				$data = json_decode( html_entity_decode( $blob, ENT_QUOTES | ENT_HTML5, 'UTF-8' ), true );
				if ( ! is_array( $data ) ) {
					$schema_failures[] = array( 'page_id' => $page_id, 'reason' => 'invalid JSON-LD' );
					continue;
				}
				$walk_schema( $data, $page_id );
			}
		}
	}
	foreach ( $referenced_ids_by_page as $page_id => $references ) {
		$undefined = array_values( array_diff( array_unique( $references ), array_unique( $defined_ids_by_page[ $page_id ] ?? array() ) ) );
		if ( $undefined ) {
			$schema_failures[] = array( 'page_id' => $page_id, 'reason' => 'undefined @id reference', 'ids' => $undefined );
		}
	}
	$identity_policy = $claim_gate['identity_schema_policy'];
	$local_identity_pages = array();
	$organisation_pages = array();
	foreach ( $schema_types_by_page as $page_id => $types ) {
		if ( array_intersect( array( 'LocalBusiness', 'GeneralContractor' ), $types ) ) {
			$local_identity_pages[] = $page_id;
		}
		if ( in_array( 'Organization', $types, true ) ) {
			$organisation_pages[] = $page_id;
		}
	}
	$identity_allowed_pages = array_keys( array_filter( $expected, static fn( array $page ): bool => in_array( $page['url'], array( '/', '/contact/' ), true ) ) );
	if ( $identity_policy['local_business_or_general_contractor_permitted'] ) {
		$assert( ! empty( $local_identity_pages ) && ! array_diff( $local_identity_pages, $identity_allowed_pages ), 'LocalBusiness/GeneralContractor follows verified staffed identity state', array( 'actual_pages' => $local_identity_pages, 'allowed_pages' => $identity_allowed_pages ) );
	} else {
		$assert( empty( $local_identity_pages ), 'LocalBusiness/GeneralContractor omitted while staffed identity is unverified', $local_identity_pages );
	}
	if ( $identity_policy['organisation_permitted'] ) {
		$assert( ! empty( $organisation_pages ) || ! empty( $local_identity_pages ), 'verified identity has an Organization or LocalBusiness definition', array( 'organization_pages' => $organisation_pages, 'local_business_pages' => $local_identity_pages ) );
	} else {
		$assert( empty( $organisation_pages ), 'Organization omitted while legal entity is unverified', $organisation_pages );
	}
	if ( $identity_policy['service_provider_required'] ) {
		$assert( $provider_nodes === $service_nodes, 'every Service has provider under verified identity state', compact( 'service_nodes', 'provider_nodes' ) );
	} else {
		$assert( $provider_nodes === 0, 'Service.provider omitted while provider identity is undefined', compact( 'service_nodes', 'provider_nodes' ) );
	}
	$assert( empty( $schema_failures ), 'schema JSON and @id references valid', $schema_failures );
	$assert( empty( $schema_failures ), 'schema matches verified identity state', array( 'identity_policy' => $identity_policy, 'failures' => $schema_failures ) );

	// 8. Canonical and current approved-wave/indexability state.
	$canonical_failures = array();
	$robots_failures = array();
	foreach ( $expected as $page_id => $page ) {
		$permalink = trailingslashit( wp_parse_url( get_permalink( $page_id ), PHP_URL_PATH ) ?: '/' );
		$rank_math_canonical = (string) get_post_meta( $page_id, 'rank_math_canonical_url', true );
		$canonical_url = $rank_math_canonical !== '' ? $rank_math_canonical : wp_get_canonical_url( $page_id );
		$actual = trailingslashit( wp_parse_url( $canonical_url, PHP_URL_PATH ) ?: '/' );
		$want   = trailingslashit( $page['url'] );
		if ( $actual !== $want || $permalink !== $want ) {
			$canonical_failures[] = array( 'page_id' => $page_id, 'expected' => $want, 'canonical' => $actual, 'permalink' => $permalink );
		}
		$page_robots = (array) get_post_meta( $page_id, 'rank_math_robots', true );
		if ( str_starts_with( $page['evidence_readiness_state']['effective_robots'], 'noindex' ) && ! in_array( 'noindex', $page_robots, true ) ) {
			$robots_failures[] = array( 'page_id' => $page_id, 'expected' => $page['evidence_readiness_state']['effective_robots'], 'actual' => $page_robots );
		}
	}
	$robots = apply_filters( 'wp_robots', array() );
	$assert( empty( $canonical_failures ), 'permalink/canonical path matches allowlist', $canonical_failures );
	$assert( empty( $robots_failures ), 'page-level indexability matches approved wave', $robots_failures );
	$assert( (string) get_option( 'blog_public' ) === '0' && isset( $robots['noindex'] ) && $robots['noindex'], 'current approved wave remains globally noindex', array( 'blog_public' => get_option( 'blog_public' ), 'robots' => $robots ) );
	$assert( ! wp_sitemaps_get_server()->sitemaps_enabled(), 'staging sitemap disabled', array() );

	$evidence['actual_page_ids']       = $actual_ids;
	$evidence['unresolved_media']      = $unresolved_media;
	$evidence['unsupported_survivors'] = $unsupported_survivors;
	$evidence['schema_failures']       = $schema_failures;
} catch ( Throwable $error ) {
	$failures[] = array( 'assertion' => 'verifier completed', 'detail' => $error->getMessage() );
}

$result = array(
	'result'   => empty( $failures ) ? 'PASS' : 'FAIL',
	'passes'   => $passes,
	'failures' => $failures,
	'evidence' => $evidence,
);
echo wp_json_encode( $result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . PHP_EOL;
exit( empty( $failures ) ? 0 : 1 );
