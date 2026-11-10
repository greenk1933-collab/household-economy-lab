# Verification results

Final automated run: **90 tests; 0 failures/errors**. Full machine-readable results: `pytest_results.xml`.

The suite checks credit allocation conservation, zero/negative balances, payoff, minimum shortfalls and promo expiry; Ontario thresholds, dates, quote basis, assignment timing and LTT regimes; tax-incidence equilibrium and zero/invalid response cases; GDP/labour/import accounting and coefficient integrity; regional observations and archival quarantine; and Streamlit interactions for all three products and navigation.

Browser QA and export inspection are recorded separately in `browser_qa.md`. Unit/UI tests validate the implemented scope, not the accuracy of unavailable data or causal identification. Acquisition refresh needs editorial review before changed contracts/rules are promoted.
