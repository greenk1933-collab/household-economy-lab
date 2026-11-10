# Editorial case file

## Pitch (45 words)
You pay more than the minimum, but where does that extra money go? An audit of Canadian card agreements shows how jurisdiction and fine print determine which balance shrinks. Our calculator translates payment-allocation clauses into a visible debt path and a dollar cost readers can test themselves.

## Original collection and supported result
24 product-family/jurisdiction records, 11 issuer brands, Canada with Quebec distinguished. This is a current-document audit, not a historical borrower panel. Six Tangerine combinations have matched rates and minimum disclosures. The default $11,000/$600 scenario produces a $95.16 interest difference when only excess allocation changes. See findings.md and source_register.csv.

## Pipeline and validation
Official agreement PDFs/HTML → raw files/hashes and extracted text → manually coded jurisdiction/priority rules → category ledger → 16 deterministic tests → interactive repayment paths, exportable CSV and static PNG/SVG. Tests include hand arithmetic, minimum-before-excess, conservation, zero debt/rates, promo expiry, shortfall, invalid APRs and finite horizon.

## Reader value and further reporting
Readers can enter existing interest-bearing balances, APRs, promo expiry and a fixed payment; see both paths; and inspect the underlying agreements. Publication needs issuer/legal responses, authorized statement comparisons, verification of unresolved National Bank Quebec amendments, and full product-disclosure expansion. The federal budget proposal is not described as enacted law.

## 60–90 second interview explanation
I started with a question most card statements make difficult to answer: does an extra payment actually attack the expensive debt? I collected original agreements across eleven issuer brands and coded jurisdiction separately because the same brand can use different rules in Quebec. The audit exposed why amendments matter: Scotiabank's base agreement needs a later Quebec notice, and one National Bank document could not support a confident current Quebec classification. I left that unresolved rather than filling it in. I then built a ledger that accrues interest by balance category, pays the minimum first, and compares two ways of applying only the excess. In the documented Tangerine example, that single change shifts the interest bill by about $95. The reader can change the balances and watch the result change. The next reporting step is to check the model against authorized real statements and get issuer responses. It is a reproducible contract investigation, with a practical consumer tool and explicit limits.


# Housing editorial case file

**Pitch (48 words).** Ontario can change the tax on a new home overnight. It cannot instantly change the number of homes available. This pilot separates the rebate buyers are legally offered from the benefit they actually keep, combining builder price disclosures, regional price and construction data, and an interactive supply-and-demand explanation.

**Original collection.** Two complete official tables contain 409,860 observations; cleaned Ontario extracts contain 30,444 observations across prices and construction, December 2016–September 2026. The builder audit adds 48 Fieldgate model/elevation asking offers and one verified Tamarack unit snapshot. Four archived prices are quarantined. This is not a representative builder sample.

**Numerical finding.** Toronto's tax-exclusive new-house index fell 4.89% year over year in September 2026 while Ottawa's Ontario portion rose 1.00%. The spread shows different market paths; it does not identify how the rebate changed either path. A Fieldgate example already deducts $106,000 in its advertised after-rebate column, illustrating double-counting risk.

**Pipeline.** StatCan ZIP/CSV + builder PDFs/HTML + original research PDFs → hash/version records → Python standard-library filters and explicit geographic/component keys → arithmetic and missing-value QA → regional trajectories, price-basis audit and separately labelled theoretical controls. The application root implements the statutory engine and tax-wedge model.

**Reader value.** Readers can check the legal-rule assumptions, see why relative demand and supply responsiveness matter, and explore observed regional markets without confusing them with a causal estimate.

**Publication reporting still needed.** Obtain dated, same-unit builder price lists and executed adjustments before/after policy; reconcile floor-area and upgrade differences; document eligibility and rebate assignment; collect closed transaction prices and developer inventories; secure untreated comparators; test anticipation, pre-trends and concurrent financing changes; interview CRA/Ontario administrators, builders, buyers, market-data vendors and the cited researchers. Verify permissions before republishing full copyrighted builder sheets. No contact or messages have been sent.

**Interview explanation (about 80 seconds).** “I wanted to avoid the obvious mistake of treating a maximum rebate as the amount a buyer necessarily gains. I began with the tax-incidence diagrams in the supplied economics module, then separated three questions: what the law allows, what the market does, and what the evidence can actually identify. I downloaded the full official price and construction tables and built a reproducible Ontario panel. Toronto's latest annual price decline differs sharply from Ottawa's, but that comparison alone cannot tell us who captured a rebate. I also audited real builder documents. One price sheet already subtracts a proposed rebate in its advertised price, so a calculator can easily count the same saving twice. The interactive product keeps legal entitlement, observed prices and theoretical incidence visibly separate. I found published supply estimates and an independent national demand estimate, but I don't relabel those as local policy effects. The next reporting step is matched, dated contracts and a credible counterfactual, not a regression that gives a precise answer to the wrong question.”


## Implemented reader tools and verified scenario
A $1m eligible non-first-time purchase has $130k total relief, $106k above ordinary relief. The reader can normalize the quote, compare assigned versus delayed credits, and adjust hypothetical supply/demand responsiveness. The latter is not measured Ontario incidence. See `project_b/reports/methodology.md` for model and testing scope.


# Editorial case file: Buying Canadian

## Pitch (47 words)

What does buying Canadian actually support? Follow $100 through the producing industry and its suppliers, separating domestic value added from imported inputs and repeated sales. An official-data calculator shows why manufacturing, retailing and services contribute differently—and why a Canadian label cannot tell us a product's full economic footprint.

## Original collected evidence

Seven full Statistics Canada bulk releases, 14,045,511 records scanned, 79,094 cleaned context/latest-release records retained. Structural coverage: national detailed multipliers through 2022 and summary IO through 2024; current consumption, trade, GDP and employment series through their separately disclosed 2026 reference periods. 217 usable industry coefficient rows, with 12 consumer-facing categories. SHA-256 hashes and source vectors preserve the audit trail.

## Numerical result and its boundary

The national 2022 coefficients associate $73.90 of Canadian GDP with $100 of household/institutional furniture and cabinet industry output delivered to final demand at basic prices, compared with $30.30 for automobile/light-duty vehicle manufacturing. This is not a comparison of retail prices or net economic gains from changing purchase origin. The original checkout-dollar question remains limited by missing measured margins and product import shares.

## Pipeline

StatCan public ZIP/CSV releases → Python urllib raw snapshots and hashes → pandas chunked parsing, unit/period filters and duplicate checks → direct + indirect GDP/labour/import coefficients checked against published Simple multipliers → industry and user-assumption retail accounting engines → Streamlit/Plotly controls and Matplotlib SVG/PNG + CSV exports.

## Method and validation

Use the official-multiplier fallback, not an invented domestic matrix. Keep 2022 coefficients separate from 2024 advanced structural context and 2026 high-frequency indicators. Validate accounting identities, amount scaling, imported-goods margin retention, invalid inputs, exact source lineage and graphic/model equality. Actual control tests change amounts, domestic-share assumptions and the displayed indicator.

## Reader benefit

Readers can inspect industry value-added differences, separate labour income from other GDP, see direct versus supplier contributions, change a hypothetical retail-price decomposition, compare categories and download both calculations and source data. Labels make evidence classes and vintages visible.

## Remaining reporting

Obtain official domestic/import-use and purchaser-price margin matrices; verify the product classification bridge; interview Statistics Canada national-accounts staff and consumer-category sourcing specialists. A matched product comparison needs observed prices, margins and sourcing—not only an industry multiplier.

## 60–90 second interview explanation

“The question I started with was what $100 of buying Canadian actually supports. I collected seven complete Statistics Canada releases and wrote a pipeline that scanned more than 14 million records, keeping the original units, reference periods and source identifiers. The important analytical choice was to count value added, not every supplier's sales. I also caught a terminology trap: Statistics Canada's Simple multiplier is the direct-plus-indirect dollars-per-dollar figure, while its Type I multiplier is a ratio to the direct effect.

“The working product compares twelve broad categories. For example, the 2022 coefficients associate about $74 of Canadian GDP with $100 of furniture-industry output at basic prices. But I would not present that as the Canadian content of a $100 sofa at checkout. That requires retail margins, taxes and product import shares that I have not measured. So the interface separates the sourced industry comparison from a clearly labelled retail sensitivity tool. It also shows newer economic indicators without pretending they update the old supply-chain matrix. The result is a useful tested pilot with a precise reporting agenda for publication.”


## Cross-project comparison

| Pilot | Reporting contribution | Technical demonstration | Claim boundary |
|---|---|---|---|
| Credit | Original issuer contract audit | Allocation and debt simulation | Illustrative borrower scenario, not a statement or representative bank ranking |
| Housing | Rules audit, price-sheet transcription and regional controls | Piecewise tax model; equilibrium theory; identification reasoning | No measured causal subsidy-capture percentage |
| Value added | Official national-accounts extraction and classification mapping | Multiplier accounting and explicit retail decomposition | Associated activity, not new jobs or causal net GDP |
