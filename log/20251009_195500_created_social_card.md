# Created social card image

Created `docs/static/img/docusaurus-social-card.jpg` from `docs/static/img/adk_tutorial.png`.

Commands used:

```bash
sips -Z 1200 "docs/static/img/adk_tutorial.png" --out "docs/static/img/docusaurus-social-card_temp.jpg"
sips -c 630 1200 "docs/static/img/docusaurus-social-card_temp.jpg" --out "docs/static/img/docusaurus-social-card.jpg"
```

Resulting image:

- Path: docs/static/img/docusaurus-social-card.jpg
- Dimensions: 1200x630

Notes:

- `sips` warned about output file suffix mismatch when writing a JPEG from a PNG source; this is cosmetic. The output is a valid JPEG.
