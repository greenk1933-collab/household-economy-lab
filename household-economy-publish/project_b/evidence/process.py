"""Deterministic clean regional panels from original Statistics Canada bulk CSVs."""
from pathlib import Path
import csv, io, zipfile, json, hashlib
BASE=Path(__file__).resolve().parent

def read_cube(table):
    with zipfile.ZipFile(BASE/'raw'/f'{table}-eng.zip') as z:
        with z.open(table+'.csv') as f:
            return list(csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig')))

def save(name,rows,columns):
    with (BASE/'processed'/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)

def main():
    nhpi=read_cube('18100205'); starts=read_cube('34100154')
    out=[]
    for r in nhpi:
        if not (r['GEO']=='Ontario' or r['GEO'].endswith(', Ontario') or r['GEO']=='Ottawa-Gatineau, Ontario part, Ontario/Quebec'):continue
        if r['REF_DATE']<'2016-12':continue
        out.append(dict(period=r['REF_DATE'],region=r['GEO'],component=r['New housing price indexes'],value=r['VALUE'],unit=r['UOM'],status=r['STATUS'],vector=r['VECTOR'],evidence_class='published estimate',source_table='18-10-0205-01'))
    assert len({(r['period'],r['region'],r['component']) for r in out})==len(out)
    assert all(float(r['value'])>0 for r in out if r['value'])
    save('nhpi_regional.csv',out,['period','region','component','value','unit','status','vector','evidence_class','source_table'])
    out2=[]
    for r in starts:
        if not (r['GEO'].endswith(', Ontario') or r['GEO']=='Ottawa-Gatineau, Ontario part, Ontario/Quebec'):continue
        if r['REF_DATE']<'2016-12':continue
        out2.append(dict(period=r['REF_DATE'],region=r['GEO'],indicator=r['Housing estimates'],unit_type=r['Type of unit'],value=r['VALUE'],unit=r['UOM'],status=r['STATUS'],vector=r['VECTOR'],evidence_class='published estimate',source_table='34-10-0154-01'))
    assert len({(r['period'],r['region'],r['indicator'],r['unit_type']) for r in out2})==len(out2)
    assert all(float(r['value'])>=0 for r in out2 if r['value'])
    save('housing_construction_regional.csv',out2,['period','region','indicator','unit_type','value','unit','status','vector','evidence_class','source_table'])
    latest=max(r['period'] for r in out)
    mapping={(r['region'],r['period']):r for r in out if r['component']=='Total (house and land)'}
    cross=[]
    for (region,period),r in mapping.items():
        if period!=latest or not r['value']:continue
        previous=f'{int(period[:4])-1}{period[4:]}'
        b=mapping.get((region,previous))
        cross.append(dict(region=region,period=period,nhpi=float(r['value']),previous_year_index=float(b['value']) if b and b['value'] else '',year_over_year_pct=(float(r['value'])/float(b['value'])-1)*100 if b and b['value'] else '',evidence_class='derived calculation'))
    save('nhpi_latest_comparison.csv',cross,['region','period','nhpi','previous_year_index','year_over_year_pct','evidence_class'])
    qa=dict(nhpi_source_rows=len(nhpi),construction_source_rows=len(starts),nhpi_clean_rows=len(out),construction_clean_rows=len(out2),nhpi_regions=len(set(r['region'] for r in out)),construction_regions=len(set(r['region'] for r in out2)),nhpi_start=min(r['period'] for r in out),nhpi_end=latest,construction_end=max(r['period'] for r in out2),missing_nhpi=sum(not r['value'] for r in out),missing_construction=sum(not r['value'] for r in out2),duplicate_keys=0,nonpositive_nhpi=0,negative_construction=0,hashes={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted((BASE/'raw').iterdir()) if x.is_file()})
    (BASE/'qa.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
    print(json.dumps(qa,indent=2));print(cross)

if __name__=='__main__': main()
