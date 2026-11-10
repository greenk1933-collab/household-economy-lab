"""Official direct-plus-indirect fallback; CAD at stated basic prices.

No induced effects, jobs estimates, retail-share imputation or brand content claims.
"""
from math import isfinite

def checked(value,name,lower=0.,upper=None):
 value=float(value)
 if not isfinite(value) or value<lower or (upper is not None and value>upper):
  raise ValueError(f'{name} must be finite and between {lower} and {upper}')
 return value

def industry_value(amount,coefficients):
 """Apply published direct and indirect coefficients to domestic final-demand output.

 Coefficients: gdp_direct, gdp_indirect, labour_direct, labour_indirect,
 imports_direct, imports_indirect. Imports mean upstream requirements, not the
 share of retail products imported. Labour is a component of GDP, never added to it.
 """
 amount=checked(amount,'amount')
 keys=('gdp_direct','gdp_indirect','labour_direct','labour_indirect','imports_direct','imports_indirect')
 c={k:checked(coefficients[k],k) for k in keys}
 if c['gdp_direct']+c['gdp_indirect']>1.02:
  raise ValueError('Direct-plus-indirect GDP exceeds final-demand value; check units/effect selection')
 if c['labour_direct']+c['labour_indirect']>c['gdp_direct']+c['gdp_indirect']+.005:
  raise ValueError('Labour cannot exceed GDP in this model')
 out={k:amount*v for k,v in c.items()}
 out.update(amount=amount,gdp=out['gdp_direct']+out['gdp_indirect'],labour=out['labour_direct']+out['labour_indirect'],imports=out['imports_direct']+out['imports_indirect'])
 out['other_gdp']=out['gdp']-out['labour']
 out['accounting_residual']=amount-out['gdp']-out['imports']
 return out

def retail_value(amount,tax_rate,margin_share,domestic_producer_share,producer,retailer):
 """User-specified sensitivity only; no defaults constitute measured product shares.

 margin_share is share of PRE-TAX purchaser spending allocated to Canadian retail
 service output. Remaining value is manufacturer or imported finished-product
 value. Other wholesale/transport margins are not imputed; user must include them
 in a documented decomposition or use this explicitly reduced two-sector scenario.
 """
 amount=checked(amount,'amount'); tax_rate=checked(tax_rate,'tax_rate',upper=1)
 margin_share=checked(margin_share,'margin_share',upper=1)
 domestic_producer_share=checked(domestic_producer_share,'domestic_producer_share',upper=1)
 pretax=amount/(1+tax_rate)
 margins=pretax*margin_share
 producer_value=pretax-margins
 domestic=producer_value*domestic_producer_share
 final_imports=producer_value-domestic
 p=industry_value(domestic,producer); r=industry_value(margins,retailer)
 out={k:p[k]+r[k] for k in ('gdp_direct','gdp_indirect','gdp','labour_direct','labour_indirect','labour','imports','other_gdp','accounting_residual')}
 out.update(amount=amount,tax=amount-pretax,retail_output=margins,domestic_producer_output=domestic,final_imports=final_imports,producer_gdp=p['gdp'],distribution_gdp=r['gdp'])
 out['total_imports']=out['imports']+final_imports
 out['accounted_total']=out['gdp']+out['total_imports']+out['tax']+out['accounting_residual']
 return out
