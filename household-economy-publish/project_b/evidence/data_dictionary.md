# Empirical data dictionary

All processed CSVs are UTF-8 with headers. Blank is unknown/not reported, not zero. Monetary values are nominal Canadian dollars. A `period` is YYYY-MM; an `observation_date` is YYYY-MM-DD with explicit date basis.

| File | Key | Measures and interpretation |
|---|---|---|
| `nhpi_regional.csv` | period + region + component | `value`: published index, December 2016=100. `component`: total house/land, house only, land only. `status`: original quality flag. `vector`: original StatCan vector. |
| `housing_construction_regional.csv` | period + region + indicator + unit_type | `value`: dwelling count. `indicator`: starts, under construction, completions. `unit_type`: total or component type. These are unadjusted levels, not annualized rates. |
| `nhpi_latest_comparison.csv` | region + period | Current index and same-month prior-year index; derived `year_over_year_pct` in percentage points of change. |
| `developer_model_prices.csv` | model_code + elevation + observation_date | Directly observed asking-offer rows, including grouped elevations. Base/advertised rebate/after-rebate CAD values reproduce sheet columns. Tax-exclusive base must not be inferred. `page` is PDF page, one-based. `unit_id` is blank because these are models, not individual homes. |
| `developer_price_observations.csv` | developer + unit_id + observation_date | Unit-level asking observations and quarantined archive leads. `reference_price_cad` and `promotion_cad` are simultaneous advertised comparison figures, not independent time observations. Current page's date is retrieval, not a known effective price date. |
| `published_elasticities.csv` | region + parameter + source_year | Dimensionless published structural coefficient. Demand is signed. Blank confidence bounds mean unavailable. Geographic/horizon caveats are essential. |
| `reporting_opportunities.csv` | topic | Evidence status, identification limits and concrete follow-up requirements. |

Raw ZIPs retain original full table metadata. Source register maps source title, URL, acquisition timestamp, raw path, SHA256, coverage, units, licensing/access conditions and limitations. `qa.json` records executed checks. `raw/fieldgate_visual_transcription.csv` is the auditable manual transcription input; regenerate its enriched output with `finalize_evidence.py`.
