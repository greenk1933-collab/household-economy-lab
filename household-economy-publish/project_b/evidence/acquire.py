"""Refresh primary housing evidence. Python stdlib; no private credentials."""
from pathlib import Path
import urllib.request, json, hashlib, datetime, time

BASE = Path(__file__).resolve().parent
SOURCES = {
 '18100205-eng.zip': 'https://www150.statcan.gc.ca/n1/tbl/csv/18100205-eng.zip',
 '34100154-eng.zip': 'https://www150.statcan.gc.ca/n1/tbl/csv/34100154-eng.zip',
 'supply_elasticities_2021.pdf': 'https://www.bankofcanada.ca/wp-content/uploads/2021/09/san2021-21.pdf',
 'tamarack_2025.pdf': 'https://www.tamarackhomes.com/wp-content/uploads/participants-database/findlay_creek_-_under_construction_townhomes_-_11-12-2025_fall_promo_2.pdf',
 'tamarack_131_kerala.html': 'https://tamarackhomes.com/ottawa/findlay-creek-village/lots/findlay-creek-block-48-1049/',
 'nhpi_metadata.html': 'https://www23.statcan.gc.ca/imdb/p2SV.pl?Function=getSurvey&SDDS=2310',
 'mattamy_rebate_basis.html': 'https://mattamyhomes.com/promos/government-rebates',
 'upper_east_2026.pdf': 'https://www.fieldgatehomes.com/upper-east/brokerportal/files/PriceList/UES-NEW-RELEASE-PRICE-LIST-AUG-12.pdf',
 'demand_research_2015.pdf': 'https://www.oar-rao.bank-banque-canada.ca/record/6599/files/wp2015-40.pdf',
}

def main():
    (BASE/'raw').mkdir(exist_ok=True)
    logs=[]
    for name,url in SOURCES.items():
        record=dict(url=url,path='raw/'+name,retrieved_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
        try:
            data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'PersonalFinanceResearch/1.0'}),timeout=60).read()
            (BASE/'raw'/name).write_bytes(data)
            record.update(status='downloaded',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
        except Exception as e: record.update(status='unavailable',error=str(e))
        logs.append(record)
        print(name,record['status'],flush=True)
        (BASE/'raw'/'acquisition_log.json').write_text(json.dumps(logs,indent=2),encoding='utf-8')
        time.sleep(.3)

if __name__=='__main__': main()
