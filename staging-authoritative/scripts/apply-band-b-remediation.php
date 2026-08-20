<?php
/**
 * Apply owner-sighted Band B media dispositions after the immutable WXR import.
 *
 * Run through WP-CLI only. The WXR remains unchanged. This script also executes
 * the already-settled D32 removal for the 15 suburb modules identified by their
 * local-work-card class, because GENERIC photographs may not remain in an
 * evidential "local work" module.
 */

if (PHP_SAPI !== 'cli' || !defined('WP_CLI')) {
    fwrite(STDERR, "FAIL: run through wp eval-file only.\n");
    exit(1);
}

WP_CLI::error(
    'Obsolete mutator refused: Band B is already enforced in build/46-active-main-import.xml by the reproducible derivative pipeline.'
);

$manifest = $args[0] ?? '/import/45-media-remediation.csv';
if (!is_readable($manifest)) {
    WP_CLI::error("Remediation manifest is not readable: {$manifest}");
}

/** @return array<int,array<string,string>> */
function band_b_read_manifest(string $path): array
{
    $handle = fopen($path, 'rb');
    if ($handle === false) {
        WP_CLI::error("Could not open remediation manifest: {$path}");
    }
    $header = fgetcsv($handle);
    if ($header === false) {
        WP_CLI::error('Remediation manifest is empty.');
    }
    $required = [
        'attachment_id', 'current_filename', 'verdict', 'ship_action',
        'target_filename', 'target_title', 'target_alt', 'usage_restriction',
    ];
    if ($header !== $required) {
        WP_CLI::error('Remediation manifest header does not match the required schema.');
    }

    $rows = [];
    while (($values = fgetcsv($handle)) !== false) {
        if ($values === [null] || $values === []) {
            continue;
        }
        if (count($values) !== count($header)) {
            WP_CLI::error('Malformed remediation row: ' . implode(',', $values));
        }
        $row = array_combine($header, $values);
        $id = (int) $row['attachment_id'];
        if (isset($rows[$id])) {
            WP_CLI::error("Duplicate remediation row for attachment {$id}.");
        }
        if (!in_array($row['ship_action'], ['RENAME', 'EXCLUDE'], true)) {
            WP_CLI::error("Unknown ship_action for attachment {$id}: {$row['ship_action']}");
        }
        $rows[$id] = $row;
    }
    fclose($handle);
    if (count($rows) !== 9) {
        WP_CLI::error('Expected 9 Band B remediation rows; found ' . count($rows) . '.');
    }
    return $rows;
}

/** @param mixed $value */
function band_b_subtree_has_local_work_card($value): bool
{
    if (!is_array($value)) {
        return false;
    }
    if (isset($value['settings']['_css_classes'])
        && strpos((string) $value['settings']['_css_classes'], 'local-work-card') !== false) {
        return true;
    }
    foreach ($value as $child) {
        if (band_b_subtree_has_local_work_card($child)) {
            return true;
        }
    }
    return false;
}

/** @param mixed $value */
function band_b_contains_image_id($value, int $target): bool
{
    if (!is_array($value)) {
        return false;
    }
    if (isset($value['id']) && (int) $value['id'] === $target
        && (isset($value['url']) || isset($value['alt']) || isset($value['source']))) {
        return true;
    }
    foreach ($value as $child) {
        if (band_b_contains_image_id($child, $target)) {
            return true;
        }
    }
    return false;
}

/**
 * Rename every image dictionary for one attachment ID without touching layout.
 *
 * @param mixed $value
 */
function band_b_rename_image(&$value, int $target, array $row, int &$count): void
{
    if (!is_array($value)) {
        return;
    }
    if (isset($value['id']) && (int) $value['id'] === $target
        && (isset($value['url']) || isset($value['alt']) || isset($value['source']))) {
        if (isset($value['url']) && is_string($value['url'])) {
            $value['url'] = preg_replace(
                '~[^/]+$~',
                $row['target_filename'],
                $value['url']
            );
        }
        $value['alt'] = $row['target_alt'];
        $count++;
    }
    foreach ($value as &$child) {
        band_b_rename_image($child, $target, $row, $count);
    }
    unset($child);
}

/** Remove a target image dictionary from non-widget settings, fail-closed. */
function band_b_clear_image_dictionary(&$value, int $target, int &$count): void
{
    if (!is_array($value)) {
        return;
    }
    foreach ($value as $key => &$child) {
        if (is_array($child)
            && isset($child['id'])
            && (int) $child['id'] === $target
            && (isset($child['url']) || isset($child['alt']) || isset($child['source']))) {
            unset($value[$key]);
            $count++;
            continue;
        }
        band_b_clear_image_dictionary($child, $target, $count);
    }
    unset($child);
}

/**
 * @param array<int,mixed> $elements
 * @return array<int,mixed>
 */
function band_b_mutate_elements(
    array $elements,
    array $rows,
    bool $top_level,
    array &$stats
): array {
    $result = [];
    foreach ($elements as $node) {
        if (!is_array($node)) {
            $result[] = $node;
            continue;
        }

        if ($top_level && band_b_subtree_has_local_work_card($node)) {
            $stats['local_work_modules_removed']++;
            foreach ($rows as $attachment_id => $row) {
                if (band_b_contains_image_id($node, (int) $attachment_id)) {
                    if ($row['ship_action'] === 'EXCLUDE') {
                        $stats['unusable_references_removed_with_module']++;
                    } else {
                        $stats['generic_references_removed_with_module']++;
                    }
                }
            }
            continue;
        }

        $settings = $node['settings'] ?? [];
        $drop_widget = false;
        foreach ($rows as $attachment_id => $row) {
            $attachment_id = (int) $attachment_id;
            if (!band_b_contains_image_id($settings, $attachment_id)) {
                continue;
            }
            if ($row['ship_action'] === 'RENAME') {
                band_b_rename_image(
                    $node['settings'],
                    $attachment_id,
                    $row,
                    $stats['generic_references_remediated']
                );
                continue;
            }

            $widget_type = (string) ($node['widgetType'] ?? '');
            if ($widget_type === 'image'
                && isset($node['settings']['image']['id'])
                && (int) $node['settings']['image']['id'] === $attachment_id) {
                $drop_widget = true;
                $stats['unusable_slots_removed']++;
                break;
            }
            if ($widget_type === 'image-box'
                && isset($node['settings']['image']['id'])
                && (int) $node['settings']['image']['id'] === $attachment_id) {
                unset($node['settings']['image']);
                $stats['unusable_slots_removed']++;
                continue;
            }
            $before = $stats['unusable_slots_removed'];
            band_b_clear_image_dictionary(
                $node['settings'],
                $attachment_id,
                $stats['unusable_slots_removed']
            );
            if ($before === $stats['unusable_slots_removed']) {
                WP_CLI::error(
                    "Attachment {$attachment_id} occurs in unsupported widget settings; rollback required."
                );
            }
        }
        if ($drop_widget) {
            continue;
        }

        if (isset($node['elements']) && is_array($node['elements'])) {
            $node['elements'] = band_b_mutate_elements(
                $node['elements'],
                $rows,
                false,
                $stats
            );
        }
        $result[] = $node;
    }
    return array_values($result);
}

$rows = band_b_read_manifest($manifest);
$stats = [
    'pages_changed' => 0,
    'generic_references_remediated' => 0,
    'unusable_slots_removed' => 0,
    'local_work_modules_removed' => 0,
    'unusable_references_removed_with_module' => 0,
    'generic_references_removed_with_module' => 0,
];

$page_ids = get_posts([
    'post_type' => 'page',
    'post_status' => 'any',
    'numberposts' => -1,
    'fields' => 'ids',
]);
foreach ($page_ids as $page_id) {
    $raw = get_post_meta($page_id, '_elementor_data', true);
    if (!is_string($raw) || $raw === '') {
        continue;
    }
    $data = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
    $mutated = band_b_mutate_elements($data, $rows, true, $stats);
    if ($mutated !== $data) {
        $encoded = wp_json_encode($mutated, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
        update_post_meta($page_id, '_elementor_data', wp_slash($encoded));
        $stats['pages_changed']++;
    }
}

foreach ($rows as $attachment_id => $row) {
    if ($row['ship_action'] !== 'RENAME') {
        continue;
    }
    if (get_post_type($attachment_id) !== 'attachment') {
        WP_CLI::error("Active generic attachment {$attachment_id} is missing; rollback required.");
    }
    wp_update_post([
        'ID' => $attachment_id,
        'post_title' => $row['target_title'],
        'post_name' => sanitize_title(pathinfo($row['target_filename'], PATHINFO_FILENAME)),
    ]);
    update_post_meta($attachment_id, '_wp_attachment_image_alt', $row['target_alt']);
}

// Fail closed on residual unsafe references and on evidential use of GENERIC assets.
$residual_unusable = 0;
$residual_local_generic = 0;
foreach ($page_ids as $page_id) {
    $raw = get_post_meta($page_id, '_elementor_data', true);
    if (!is_string($raw) || $raw === '') {
        continue;
    }
    $data = json_decode($raw, true, 512, JSON_THROW_ON_ERROR);
    foreach ($rows as $attachment_id => $row) {
        if ($row['ship_action'] === 'EXCLUDE'
            && band_b_contains_image_id($data, (int) $attachment_id)) {
            $residual_unusable++;
        }
    }
    if (band_b_subtree_has_local_work_card($data)) {
        foreach ($rows as $attachment_id => $row) {
            if ($row['ship_action'] === 'RENAME'
                && band_b_contains_image_id($data, (int) $attachment_id)) {
                $residual_local_generic++;
            }
        }
    }
}
if ($residual_unusable !== 0 || $residual_local_generic !== 0) {
    WP_CLI::error(
        "Residual Band B failure: unusable={$residual_unusable}, " .
        "generic-in-local-work={$residual_local_generic}. Rollback required."
    );
}

if ($stats['local_work_modules_removed'] !== 15) {
    WP_CLI::error(
        'Expected 15 local-work modules to be removed; removed ' .
        $stats['local_work_modules_removed'] . '. Rollback required.'
    );
}
if ($stats['generic_references_remediated'] !== 106) {
    WP_CLI::error(
        'Expected 106 surviving GENERIC references to be remediated; remediated ' .
        $stats['generic_references_remediated'] . '. Rollback required.'
    );
}
if (($stats['unusable_slots_removed'] + $stats['unusable_references_removed_with_module']) !== 28) {
    WP_CLI::error(
        'Expected 28 UNUSABLE references to be removed across the two assets; removed ' .
        ($stats['unusable_slots_removed'] + $stats['unusable_references_removed_with_module']) .
        '. Rollback required.'
    );
}
if ($stats['generic_references_removed_with_module'] !== 4) {
    WP_CLI::error(
        'Expected 4 GENERIC references to leave with local-work modules; removed ' .
        $stats['generic_references_removed_with_module'] . '. Rollback required.'
    );
}

WP_CLI::success(
    'Band B applied: ' . wp_json_encode($stats, JSON_UNESCAPED_SLASHES)
);
