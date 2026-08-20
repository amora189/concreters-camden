# Disposable local WordPress smoke test

This environment is bound to `127.0.0.1:8088` and is not authoritative staging. Its database and uploads must be rebuilt after the original 83 media files and Astra Customizer export are supplied.

The database credentials in `docker-compose.yml` are deliberately disposable local-only values. Do not reuse them for any external environment. No SMTP, hosting, API, owner, or production credentials belong in this directory.

Apache sends the global `X-Robots-Tag` and denies direct access to `wp-content/debug.log`. The must-use plugin adds WordPress robots directives and rejects unexpected hosts; the physical `robots.txt` disallows all crawling. WordPress search visibility must also remain disabled.

Rollback checkpoints are written under `backups/` and are intentionally excluded from version control.

The disposable WXR test was rolled back to `backups/01-before-disposable-wxr-import/` after WordPress Importer created no attachment records with fetching disabled. Do not retry the authoritative import until all 83 original binaries and the Astra Customizer export are available and the corrected local-media import path has been tested.
