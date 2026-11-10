from pathlib import Path
import csv,json
BASE=Path(__file__).resolve().parent
def write_csv(path,rows,columns=None):
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns or list(rows[0]));w.writeheader();w.writerows(rows)

rows=list(csv.DictReader((BASE/'raw/fieldgate_visual_transcription.csv').open(encoding='utf-8')))
for r in rows:
    r.update(developer='Fieldgate Homes',development='Upper East Side Unionville',region='Markham (Toronto CMA)',observation_date='2026-07-11',date_basis='Printed footer; URL filename says AUG-12 but does not override printed date',price_type='Asking model/elevation offer',source_url='https://www.fieldgatehomes.com/upper-east/brokerportal/files/PriceList/UES-NEW-RELEASE-PRICE-LIST-AUG-12.pdf',evidence_class='directly observed',unit_id='',hst_basis='Conditional advertised rebate; do not treat base-price column as automatically pre-HST',incentive='20000 decor upgrade allowance; not a cash discount',limitations='One price-list date; some rows group elevations; no transaction or lot identifier')
    if r['advertised_rebate_cad']:
        assert int(r['base_price_cad'])-int(r['advertised_rebate_cad'])==int(r['after_rebate_price_cad'])
write_csv(BASE/'processed/developer_model_prices.csv',rows)

path=BASE/'processed/developer_price_observations.csv'
obs=list(csv.DictReader(path.open(encoding='utf-8')))
for r in obs:
    if r['observation_date']=='2025-11-12':
        r['comparability_note']='Search-index extraction only; original PDF returned HTTP404; unverified archival observation; do not promote to verified historical panel'
        r['evidence_class']='unverified archival lead'
    else:
        r['date_basis']='Retrieval date; page metadata modified 2026-04-20 does not establish price change date'
        r['comparability_note']='Downloaded raw builder HTML confirms price; size2270 conflicts with prior2285; HST basis unspecified; not a causal pre/post pair'
write_csv(path,obs)

path=BASE/'processed/published_elasticities.csv'
elastic=list(csv.DictReader(path.open(encoding='utf-8')))
if not any(r['parameter']=='demand' for r in elastic):
    elastic.append(dict(region='Canada',parameter='demand',estimate='-0.6',lower_ci='',upper_ci='',source_year='2015',reference_period='1982Q1-2015Q1',horizon='Long-run national housing stock demand',source_url='https://www.oar-rao.bank-banque-canada.ca/record/6599/files/wp2015-40.pdf',source_location='PDF page30 printed25 Section6.2',evidence_class='published estimate',transferability_limit='Rounded inversion of freely estimated inverse coefficient1.6 t-stat2.5; maintained inverse1.8; not a city or new-home estimate; do not mechanically pair with city supply'))
write_csv(path,elastic)

meta={
'18100205-eng.zip':('New housing price index monthly 18-10-0205-01','Statistics Canada','2026-10-22','1981-01 to 2026-09','Monthly','Canada and regions','Region-month-component','December2016=100 index','Statistics Canada Open Licence','Published estimates; builder selling prices exclude GST/HST; singles semis towns not condos; not SA'),
'34100154-eng.zip':('Housing starts under construction and completions 34-10-0154-01','Statistics Canada / CMHC','2026-10-19','1972-01 to 2026-09','Monthly','Canadian CMAs','Region-month-estimate-type','Dwelling units','CMHC Licence Agreement for Use of Data','Not seasonally adjusted; geography changes with census definitions; under-construction is not unsold inventory'),
'supply_elasticities_2021.pdf':('Canadian housing supply elasticities SAN2021-21','Bank of Canada / Nuno Paixao','2021-09-09','Historical cycles through2020','One publication','151 Canadian census agglomerations','City structural supply estimate','Elasticity','Bank of Canada copyright; research citation','No paired regional demand parameters; not policy-specific; London estimate extreme'),
'tamarack_2025.pdf':('Findlay Creek under-construction townhomes promotion','Tamarack Homes','2025-11-12','2025-11-12','Price-sheet snapshot','Ottawa','Unit advertised asking price','CAD','Builder copyrighted marketing document','Original404; search-index extraction only; archival leads quarantined'),
'tamarack_131_kerala.html':('Findlay Creek Block48.1049 advertised property','Tamarack Homes','2026-04-20 metadata modified; price effective date unknown','Retrieved2026-11-10','Live snapshot','Ottawa','Unit asking price','CAD','Builder copyrighted marketing document','Current raw HTML available; size and tax basis require reconciliation'),
'nhpi_metadata.html':('New Housing Price Index survey2310 metadata','Statistics Canada','','Current methodology','Metadata','Canada','Survey definition','','Statistics Canada Open Licence','Index price is tax-exclusive; not all new property types'),
'mattamy_rebate_basis.html':('Government rebates pricing disclosure','Mattamy Homes','2026-07-22','Current page disclosure','Disclosure','Ontario','Advertised price basis','','Builder copyrighted disclosure','Estimated rebate already included in Ontario website prices; conditional purchaser eligibility'),
'upper_east_2026.pdf':('Upper East Side Unionville price list','Fieldgate Homes','2026-07-11 printed footer','2026-07-11','Price-sheet snapshot','Markham','Model/elevation price offer','CAD','Builder copyrighted marketing document','48 offer rows visually transcribed; grouped elevations; after-rebate prices conditional; no historical panel'),
'demand_research_2015.pdf':('Credit Conditions and Consumption House Prices and Debt: What Makes Canada Different? WP2015-40','Bank of Canada / Muellbauer St-Amant Williams','2015-11','1982Q1-2015Q1','One publication','Canada','National quarterly model','Elasticity','Bank of Canada copyright; research citation','National long-run demand; not local new-home parameter'),
}
log=json.loads((BASE/'raw/acquisition_log.json').read_text())
register=[]
for x in log:
    key=Path(x['path']).name
    title,publisher,date,period,frequency,geo,unitobs,unit,lic,limitations=meta[key]
    register.append(dict(project='B',title=title,publisher=publisher,url=x['url'],retrieved_at=x['retrieved_at'],published_effective_revision=date,reference_period=period,frequency=frequency,geography=geo,unit_of_observation=unitobs,unit_currency=unit,file_format=key.split('.')[-1],path='project_b/evidence/'+x['path'],acquisition_method='Public HTTP bulk/API or original document; see acquisition log',licence_access=lic,reliability='Primary source' if x['status']=='downloaded' else 'Unverified archival lead',limitations=limitations,status=x['status'],sha256=x.get('sha256','')))
write_csv(BASE/'source_register.csv',register)
qa=json.loads((BASE/'qa.json').read_text())
qa.update(fieldgate_offer_rows=len(rows),fieldgate_rebate_arithmetic_checked=sum(bool(r['advertised_rebate_cad']) for r in rows),verified_unit_snapshots=sum(r['evidence_class']=='directly observed' for r in obs),unverified_archive_leads=4,published_elasticity_records=len(elastic))
(BASE/'qa.json').write_text(json.dumps(qa,indent=2))
print({k:v for k,v in qa.items() if k!='hashes'})
