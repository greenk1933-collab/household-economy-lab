from pathlib import Path
import csv,hashlib,json,unittest
BASE=Path(__file__).resolve().parent
def rows(name):
    with (BASE/'processed'/name).open(encoding='utf-8') as f:
        return list(csv.DictReader(f))
class EvidenceTests(unittest.TestCase):
    def test_source_hashes(self):
        with (BASE/'source_register.csv').open(encoding='utf-8') as f:
            register=list(csv.DictReader(f))
        for r in register:
            if r['status']=='downloaded':
                p=BASE/'raw'/Path(r['path']).name
                self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['sha256'])
    def test_prices_not_duplicate(self):
        r=rows('nhpi_regional.csv');self.assertEqual(len(r),len({(v['period'],v['region'],v['component']) for v in r}))
        self.assertTrue(all(float(v['value'])>0 for v in r))
    def test_fieldgate_arithmetic(self):
        r=rows('developer_model_prices.csv');self.assertEqual(len(r),48)
        eligible=[v for v in r if v['advertised_rebate_cad']];self.assertEqual(len(eligible),33)
        for v in eligible:self.assertEqual(int(v['base_price_cad'])-int(v['advertised_rebate_cad']),int(v['after_rebate_price_cad']))
    def test_archival_quarantine(self):
        r=rows('developer_price_observations.csv')
        self.assertEqual(sum(v['evidence_class']=='unverified archival lead' for v in r),4)
        self.assertEqual(sum(v['evidence_class']=='directly observed' for v in r),1)
    def test_latest_change(self):
        for v in rows('nhpi_latest_comparison.csv'):
            self.assertAlmostEqual(float(v['year_over_year_pct']),100*(float(v['nhpi'])/float(v['previous_year_index'])-1))
    def test_demand_separate(self):
        demand=[v for v in rows('published_elasticities.csv') if v['parameter']=='demand']
        self.assertEqual(len(demand),1);self.assertEqual(demand[0]['region'],'Canada');self.assertLess(float(demand[0]['estimate']),0)
if __name__=='__main__':unittest.main()
