# Application and export verification

Verified locally on November 10, 2026, using Streamlit 1.67.0 and the in-app browser. The packaged data snapshot runs without a network connection. Public source links require internet.

| Check | Observed result |
|---|---|
| Landing and navigation | Landing page and all three routed products rendered; sidebar navigation opened the housing and value-added pages. Automated navigation also covers the methods page. |
| Credit calculation | Default scenario displayed $1,877.18 contractual interest, $1,782.02 counterfactual interest and a $95.16 difference. A payment change recalculated the results. |
| Credit precision regression | Browser testing exposed APR rounding from a 0.1 input step. Changed it to 0.01; an automated regression verifies preservation of the 20.95% default. |
| Housing legal calculator | Changing the pre-HST price from $1,000,000 to $1,675,000 changed total statutory relief from $130,000 to $77,000; the latter showed $53,000 incremental relief and $25,000 later receivable. |
| Housing incidence | The live chart rendered demand, original supply and shifted supply. Default buyer/seller shares were 33.3%/66.7%; automated interaction tests verify changed elasticities and the indeterminate zero/zero case. |
| Housing regional evidence | Actual regional price series, cross-region comparison, construction series and 48 builder offers rendered, with explicit coverage and counterfactual warnings. |
| Value-added calculation | $100 of the default furniture-industry final demand produced $73.90 associated GDP and $51.80 labour income. Changing the amount to $200 produced $147.80 and $103.60. |
| Retail sensitivity | The separate retail mode rendered its hypothetical-input notice and decomposition, including taxes, retail services and upstream imports. |
| Layout | Reviewed desktop/narrow browser views. Headings, controls and charts rendered. Some long Streamlit metric labels abbreviate in narrow columns; the complete labels remain in accessible text. Full device/accessibility certification was not performed. |
| Static exports | All three PNG and SVG exports were generated. PNGs were visually inspected; automated checks verify output presence and graphic/model data consistency where implemented. |
| Launch script | `launch.ps1 -NoBrowser -Port 8502` started the app and `/_stcore/health` returned `ok`. Both owned preview servers were then stopped. |

Final automated run: **90 tests passed, zero failures/errors**. The complete offline pipeline ran successfully, including processing, exports, reports and tests. See `pytest_results.xml` and `model_tests.md`.

CSV controls are implemented and their data paths are covered by application/model tests; an end-to-end browser download to a saved file was not separately verified. Streamlit logged non-fatal deprecation notices for `use_container_width`; the pinned version supports it. Source refreshes require editorial review and are not a substitute for re-verifying changed legal or contract terms.
