# Data dictionary

issuer_audit.csv / JSON: issuer (brand); card (specific product or explicitly named family); jurisdiction (Quebec/outside); contract_effective (date/revision or blank); agreement_url; clause_or_page (1-based PDF page or contract section); purchase_apr/cash_apr/transfer_apr (fractions, missing means not verified); promo_terms; minimum_payment_rule; allocation_of_minimum; allocation_of_excess (highest/proportional/unresolved); installment_exceptions; rule_confidence; verified_on; evidence_class; source_id; simulation_enabled; notes. Null is unknown, never zero.

credit_scenarios.csv: scenario; month (synthetic period, 0 = opening); balance (principal + unpaid interest); interest (period charge); cumulative_interest; payment (capped at debt); minimum; each named segment's balance and excess allocation. All amounts CAD. The first row has no segment allocation because no payment has occurred.

scenario_summary.json: aggregate values for the single exported example. source_register.csv: source metadata, acquisition status, usable path and SHA256. acquisition_log.json retains HTTP/download outcomes. Raw files remain publisher-owned reference material.


# Housing model outputs

All cost columns are nominal CAD. `price_excluding_hst` is the recovered contractual consideration. `total_relief` is the sum of Ontario, federal and ONHAP relief after caps and offsets. `additional_vs_ordinary` subtracts ordinary Ontario and federal rebates; `additional_vs_no_temporary_relief` also retains eligible first-time relief in the counterfactual. `total_cost` includes entered charges and relevant transfer taxes; `closing_cash_cost` postpones only rebates not credited by the builder. It is before mortgage financing and deposits. `later_receivable` is the difference between those two cost figures. Booleans report scoped eligibility, not an independently adjudicated legal determination.

Incidence data: `ed` is the nonnegative magnitude of demand elasticity, `es` is supply elasticity; both are scenario inputs. Price changes are CAD per unit, quantities are index units, and shares are fractions summing to1. `tax_change` is signed. `buyer_benefit` and `producer_benefit` reverse sign for a tax increase. See `../evidence/data_dictionary.md` for the empirical datasets.


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


# Project C data dictionary

* `multipliers_latest_long.csv`: original latest 2022 detailed national multiplier rows. Key = REF_DATE + GEO + Multiplier type + Variable + Industry. VALUE remains in its original UOM. Jobs rows use different units and are never passed to the calculator. STATUS and VECTOR retain source lineage.
* `industry_coefficients.csv`: one usable latest industry row per IOIC `code`; `reference_year` and `source_table` fix vintage. `gdp_direct`, `gdp_indirect` are CAD basic-price value added per CAD of domestic output delivered to final demand. `labour_*` are labour income per CAD; `imports_*` are upstream international imports per CAD. Every coefficient has a corresponding source vector. Missing coefficients prevent a row's promotion.
* `category_coefficients.csv`: 12 editorial display categories, exact industry labels and codes, matching retail service code, scope and confidence labels, plus coefficients. This is not an official product concordance. `retailer_code` selects the industry coefficient for a user-specified retail margin, not an observed margin share.
* `36100013_clean.csv`: latest summary national multiplier data, original variables and units.
* `36100084_clean.csv`: 2024 summary national IO rows, purchaser/basic valuation kept separate, original CAD millions. No domestic technical matrix is inferred from this extract.
* `36100124_clean.csv`: national current-price quarterly household consumption since 2019, seasonally adjusted quarterly rates, CAD millions. REF_DATE is the quarter's starting month.
* `12100163_clean.csv`: customs, unadjusted monthly merchandise trade since 2019, NAPCS categories, CAD millions; Trade distinguishes flows.
* `36100434_clean.csv`: national real industry GDP since 2019, chained 2017 CAD millions, seasonally adjusted annual rates. Chain-volume components should not be summed to infer current-price totals.
* `14100022_clean.csv`: national industry employment, all genders, age 15+, monthly unadjusted, thousands of persons, since 2019. This is context, not a jobs multiplier.
* `coverage.csv`: raw scanned and retained row counts and reference-date ranges by table.
* `buy_canadian_scenarios.csv`: deterministic $100 basic-price industry calculations used in the publication graphic. GDP sums only direct and indirect value added; labour is a subset. `accounting_residual` = final-demand amount minus GDP and upstream imports, preserving the unallocated product-tax/subsidy and rounding difference.

Empty numeric observations remain missing. Published zeros remain zeros. Original scalars are retained rather than silently converted. All monetary calculator inputs/outputs are nominal CAD scenarios using 2022 coefficient ratios; they are not an inflation-adjusted forecast.

Official classification supplement: 249 rows from Statistics Canada’s NAICS 2022-to-IOIC 2022 GDP-industry concordance were acquired and parsed into `official_naics_ioic_concordance.csv`, preserving its scope notes. This does not fill the missing NAPCS/household-consumption bridge. Source: https://www.statcan.gc.ca/en/statistical-programs/document/1303_D7_V4
