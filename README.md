# Airport Data Insights

A Python dashboard exploring the historical Noida International Airport development dataset. Compare four planning phases, inspect capacity growth and investment estimates, browse facility cards, and export selected data for Power BI.

## Run locally

Python 3.10 or newer is required (checks use Python 3.12).

```sh
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The browser opens one dashboard. `python -m streamlit run Overview.py` is also supported. The old Tkinter and sequential Matplotlib windows have been replaced.

## Features

- Dark dashboard with phase filtering and clear units.
- Interactive investment, cumulative capacity, added capacity, and cargo charts.
- Online Lucide facility icons via Iconify, with always-visible text labels.
- Historical milestone view, data table, and filtered CSV download.
- Shared CSV loader with schema, numeric and capacity checks.
- Automated tests and GitHub Actions checks.

## Data integrity and limitations

This is an educational historical planning snapshot, **not live airport traffic or verified current operational information**. The original project claimed official sources but supplied no dated, row-level citations. Costs, years, statuses, areas and facility assignments should not be treated as independently verified facts. No new current airport claims have been introduced.

`noida_airport_data.csv` is the only runtime data source. The duplicate embedded datasets disagreed on runway counts, terminal areas and land areas; these have been removed in favor of the checked-in CSV. Original zero placeholders for later runway and land values are now blank (unknown), consistent with comments in the original table script. Other CSV values remain unchanged. Facility labels are inherited from the original overview, and do not verify runway counts or facility completion.

Capacity targets (12, 30, 50, 70 MPPA) are cumulative, so the old capacity pie chart was misleading. Added capacity is 12, 18, 20 and 20 MPPA. A phase filter does not change those baseline increments. Capacity targets are never summed. The combined cost metric is an arithmetic sum of inherited estimates; their accounting basis has not been verified.

The raw Excel workbook and legacy PNGs are retained as historical assets and are not read by the app. Launching either entry point does not overwrite the dataset. Downloads are explicit.

## Project structure

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit interface and Plotly charts |
| `data.py` | Portable loader, validation, derived metrics, facility mapping |
| `noida_airport_data.csv` | Canonical historical dataset |
| `Overview.py` | Compatibility dashboard entry point |
| `First data table.py` | Print the canonical dataset |
| `test_app.py` | Data and dashboard interaction tests |
| `THIRD_PARTY_NOTICES.md` | Icon credits and legacy asset notes |

## Verify

```sh
python -m unittest -v
```

Tests cover capacity increments, unknown values, invalid schema, phase filtering, empty selection, and prevention of accidental data overwrites.

## Icons

Icons load from `https://api.iconify.design/lucide/<name>.svg`. Internet is required for those images; facility names remain readable offline. See [Iconify SVG documentation](https://iconify.design/docs/api/svg.html), `THIRD_PARTY_NOTICES.md`, and `LUCIDE_LICENSE` for source and licensing information.

To host on Streamlit Community Cloud, select this repository and set the main file to `app.py`. No secrets are required. Hosting is not configured by this change.
