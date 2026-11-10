"""Combine project evidence into the local editorial handoff; no network calls."""
from pathlib import Path
import csv, hashlib, json, shutil
import xml.etree.ElementTree as ET
import pandas as pd
ROOT=Path(__file__).resolve().parent
R=ROOT/'reports'; R.mkdir(exist_ok=True)
def write(name,text): (R/name).write_text(text,encoding='utf-8')
def combine():
    specs=[('project_a/reports/source_register.csv','project_a'),('project_b/reports/source_register.csv','project_b'),('project_b/evidence/source_register.csv','project_b/evidence'),('project_c/reports/source_register.csv','project_c')]
    rows=[]
    fields=['project','title','publisher','url','retrieved_at','published_effective_revision_dates','reference_period','frequency','geography','unit_of_observation','unit_currency','file_format','path','acquisition_method','licence_access_restrictions','reliability','limitations','status','sha256']
    aliases={'published_effective_revision_dates':['published_effective_revision_dates','published_effective_revision'],'reference_period':['reference_period','reference_periods'],'path':['path','file_path'],'licence_access_restrictions':['licence_access_restrictions','licence_access','licence']}
    for file,base in specs:
        for row in csv.DictReader((ROOT/file).open(encoding='utf-8-sig')):
            out={k:next((row[a] for a in aliases.get(k,[k]) if row.get(a)), '') for k in fields}
            path=out['path'].replace('\\','/')
            if path and not path.startswith('project_'): path=base+'/'+path
            out['path']=path
            if path and not (ROOT/path).is_file(): out['limitations']+='; Original local file unavailable; retain source URL and status.'
            rows.append(out)
    inp=ROOT/'inputs'
    if inp.exists():
        for p in inp.rglob('*'):
            if p.is_file() and p.suffix in ['.pdf','.txt','.md']:
                rows.append(dict(project='Context',title=p.name,publisher='User-provided handoff / original author',url='',retrieved_at='2026-11-10',published_effective_revision_dates='See document',reference_period='Historical background',frequency='One supplied version',geography='Canada / course context',unit_of_observation='Document',unit_currency='Not applicable',file_format=p.suffix[1:],path=p.relative_to(ROOT).as_posix(),acquisition_method='Extracted from supplied ZIP; separate chat export hash matched',licence_access_restrictions='Private supplied reference; no public redistribution authorization inferred',reliability='Original context, not current policy verification',limitations='Historical conversation instructions not promoted to user instructions or factual authority',status='supplied',sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    pd.DataFrame(rows,columns=fields).to_csv(R/'source_register.csv',index=False)
    return rows

def main():
    rows=combine()
    exports=ROOT/'exports';exports.mkdir(exist_ok=True)
    for project,stem in [('project_a','credit_cards'),('project_b','ontario_tax_incidence'),('project_c','buy_canadian')]:
        for ext in ['png','svg']: shutil.copy2(ROOT/project/'exports'/f'{stem}.{ext}',exports/f'{stem}.{ext}')
    write('coverage.md','''# What was completed

All three phases ran: public-source acquisition, deterministic processing and model construction, and a local interactive application with three routed products. This is an independently developed portfolio pilot, not a commissioned Globe and Mail product or a publication-ready causal investigation.

| Product | Collected and processed evidence | Working product |
|---|---|---|
| Credit cards | 24 product-family/jurisdiction audit rows across 11 issuer brands; six matched Tangerine product/jurisdiction variants enabled | Contract-informed repayment and promotional-expiry simulation, counterfactual trajectory, institution audit and CSV export |
| Ontario housing | 409,860 raw statistical rows; 30,444 cleaned regional records, 48 verified model/elevation offers, one verified live unit offer; six published elasticity records | Scoped legal rebate and closing-cost calculator, live incidence diagram, regional price/construction explorer, builder evidence and CSV exports |
| Canadian value added | Seven complete archives, 14,045,511 raw rows scanned; 79,094 contextual/latest rows; 217 usable industry coefficients; 12 displayed categories; 249 concordance rows | Official-multiplier comparison, labour-income component, direct/upstream bars, retail sensitivity and context explorer |

The house-price and construction series run through September 2026. Consumption runs through Q2 2026; trade September 2026, industry GDP August 2026, employment October 2026. Structural detailed multipliers refer to 2022; the acquired national summary input-output table refers to 2024. Those vintages are never relabelled as observed 2026 relationships.

Missing deliverables are explicit: no verified longitudinal property-price panel, no policy-specific causal housing estimate, no complete proprietary/on-request purchaser-price margin/import matrix, no brand-specific domestic-content measure, and no full statement reconstruction for every audited issuer. These gaps constrain findings; they do not prevent the three scoped pilots from functioning.

See each project's reports for detailed sampling and acquisition coverage. The combined source register retains download failures and original hashes. The full bundle includes user-provided interview context and course materials for private use.
''')
    write('findings.md','\n\n'.join((ROOT/p).read_text(encoding='utf-8') for p in ['project_a/reports/findings.md','project_b/reports/findings.md','project_c/reports/findings.md']))
    write('methodology.md','''# Reproducible methods

`pipeline.py` runs the offline transformations against preserved source snapshots, rebuilds the model examples and graphics, and assembles these reports. `--acquire` explicitly refreshes public sources before processing; refreshed terms must be reviewed before promoting changed observations. The regular application makes no live data request. Data collection is separate from reader inputs.

Source types remain explicit: directly observed documents/offers, published estimates, derived calculations, hypothetical sensitivity scenarios, and unverified archival leads. No statistically identified policy-specific estimate is claimed. Missing values are not converted to zero. Monetary columns identify nominal CAD; context GDP retains chained-dollar labels and employment retains thousands-of-persons scaling.

## Credit cards

Primary contract text → manually reviewed product/jurisdiction coding → capped balance allocations → month-by-month interest scenario → two trajectories and CSV. Minimum treatment is held constant when comparing excess allocation. Only matched disclosed products are enabled. This is not an exact account statement.

## Ontario housing

Official rule documents → executable piecewise statutory schedules and date gates → tax-inclusive quote normalization → transfer-tax/credit timing calculation. Separately, the original course diagram → explicitly calibrated linear supply/demand curves → finite interior equilibrium and sensitivity controls. Official regional bulk tables → geographic/component filters → index changes and construction charts. Builder PDFs → reviewed transcription → same-date offer table; unavailable history remains quarantined.

## Canadian value added

Official bulk multiplier table → exact effect/unit/vintage selection → direct-plus-indirect coefficient integrity checks → documented industry mapping → associated GDP and labour income. A separate retail sensitivity model decomposes entered pre-tax value into user-specified Canadian retail services and domestic/imported basic product value; no observed share is invented. Newer consumption/trade/GDP/employment provide context only.

Detailed equations, constraints and source locators are in each `project_*/reports/methodology.md` and the housing evidence directory. `data_lineage.csv` maps delivered tables to source files and transformation commands.
''')
    write('limitations.md','\n\n'.join((ROOT/p).read_text(encoding='utf-8') for p in ['project_a/reports/limitations.md','project_b/reports/limitations.md','project_c/reports/limitations.md']))
    write('data_dictionary.md','\n\n'.join((ROOT/p).read_text(encoding='utf-8') for p in ['project_a/reports/data_dictionary.md','project_b/reports/data_dictionary.md','project_b/evidence/data_dictionary.md','project_c/reports/data_dictionary.md']))
    bbrief=(ROOT/'project_b/evidence/interview_brief.md').read_text(encoding='utf-8')
    bbrief+='''\n\n## Implemented reader tools and verified scenario\nA $1m eligible non-first-time purchase has $130k total relief, $106k above ordinary relief. The reader can normalize the quote, compare assigned versus delayed credits, and adjust hypothetical supply/demand responsiveness. The latter is not measured Ontario incidence. See `project_b/reports/methodology.md` for model and testing scope.\n'''
    write('interview_briefs.md',(ROOT/'project_a/reports/interview_brief.md').read_text(encoding='utf-8')+'\n\n'+bbrief+'\n\n'+(ROOT/'project_c/reports/interview_brief.md').read_text(encoding='utf-8')+'''

## Cross-project comparison

| Pilot | Reporting contribution | Technical demonstration | Claim boundary |
|---|---|---|---|
| Credit | Original issuer contract audit | Allocation and debt simulation | Illustrative borrower scenario, not a statement or representative bank ranking |
| Housing | Rules audit, price-sheet transcription and regional controls | Piecewise tax model; equilibrium theory; identification reasoning | No measured causal subsidy-capture percentage |
| Value added | Official national-accounts extraction and classification mapping | Multiplier accounting and explicit retail decomposition | Associated activity, not new jobs or causal net GDP |
''')
    lineage=[]
    for directory,command,source in [('project_a/data/processed','python -m project_a.process','project_a/data/raw; manual coding in process.py'),('project_b/data/processed','python -m project_b.export','project_b/data/raw; model.py rules'),('project_b/evidence/processed','python project_b/evidence/process.py && python project_b/evidence/finalize_evidence.py','project_b/evidence/raw; reviewed transcription'),('project_c/data/processed','python -m project_c.process && python -m project_c.concordance','project_c/data/raw bulk archives')]:
        for p in (ROOT/directory).glob('*.csv'):
            df=pd.read_csv(p)
            lineage.append(dict(output=p.relative_to(ROOT).as_posix(),rows=len(df),columns=len(df.columns),source=source,transformation=command,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    pd.DataFrame(lineage).to_csv(R/'data_lineage.csv',index=False)
    raw=[]
    for p in ROOT.rglob('*'):
        if p.is_file() and ('raw' in p.parts or 'inputs' in p.parts):
            raw.append(dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
    pd.DataFrame(raw).to_csv(R/'raw_manifest_sha256.csv',index=False)
    junit=R/'pytest_results.xml'
    if junit.exists():
        suites=ET.parse(junit).getroot().findall('testsuite')
        n=sum(int(s.get('tests',0)) for s in suites);bad=sum(int(s.get('failures',0))+int(s.get('errors',0)) for s in suites)
        write('model_tests.md',f'''# Verification results

Final automated run: **{n} tests; {bad} failures/errors**. Full machine-readable results: `pytest_results.xml`.

The suite checks credit allocation conservation, zero/negative balances, payoff, minimum shortfalls and promo expiry; Ontario thresholds, dates, quote basis, assignment timing and LTT regimes; tax-incidence equilibrium and zero/invalid response cases; GDP/labour/import accounting and coefficient integrity; regional observations and archival quarantine; and Streamlit interactions for all three products and navigation.

Browser QA and export inspection are recorded separately in `browser_qa.md`. Unit/UI tests validate the implemented scope, not the accuracy of unavailable data or causal identification. Acquisition refresh needs editorial review before changed contracts/rules are promoted.
''')
    print(f'Combined {len(rows)} source records, {len(lineage)} clean tables, {len(raw)} raw/context files.')
if __name__=='__main__':main()
