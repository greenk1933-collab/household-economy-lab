# Independent review notes — initial model snapshot

Reviewed `project_b/model.py` against downloaded federal rebate regulations s41(2), (2.01), (2.1), (2.2), Ontario ONHAP program disclosure, Ontario LTT guidance and Toronto MLTT rates. This records observations on the initial snapshot, not a claim that subsequent code still contains these issues.

Confirmed rebate logic: ordinary Ontario rebate is 75% of provincial HST up to $24,000; enhanced relief applies its upper-price phase-out to the $80,000-minus-ordinary top-up; the ordinary floor is retained where the first-buyer top-up would otherwise be negative; overlapping provincial programs must not be simply added; ONHAP deducts federal entitlement; tax-inclusive net quotes add back the documented assigned rebate before dividing by 1.13. The linear incidence solution satisfies the wedge, market clearing, zero-elasticity limits and share-sum identity.

Issue sent to owner: Toronto high-value brackets in the initial model applied the 2024–March 2026 schedule to every closing before April 2026. The advertised input scope included 2017–2023 closings, which need the older rate above $2m or an explicit scope restriction.

Timing limitation sent to owner: enhanced eligibility is legally tied to tax becoming payable before 2033. Requiring both possession and closing by December 2032 is stricter than that rule. Real-property tax timing and special condo timing need an explicit tax-payable date or a clearly restricted supported case.

Cost/eligibility cautions sent to owner: Toronto's published $102.56 plus HST processing fee must be included or visibly excluded; first-buyer eligibility must be self-certified against the full CRA criteria, distinct from ordinary primary residence of a relation; unsupported costs and nonresident taxes must remain explicit. Plotting may clip negative quantity segments at extreme elasticities, while keeping the valid interior equilibrium unchanged.
