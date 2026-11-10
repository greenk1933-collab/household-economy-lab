"""Streamlit page for the official-multiplier value-added pilot."""
from pathlib import Path
import pandas as pd
from project_c.models import industry_value,retail_value
ROOT=Path(__file__).resolve().parent

def render():
 import streamlit as st
 import plotly.graph_objects as go
 st.caption('CANADIAN VALUE ADDED  /  PUBLISHED ESTIMATES + DERIVED CALCULATIONS')
 st.title('What part of your spending becomes Canadian value added?')
 st.markdown("After U.S. tariffs reignited Canada-U.S. trade tensions in 2025, Canadians increasingly sought domestic alternatives; in February 2026, Bank of Canada researchers documented a shift in grocery spending toward products associated with Canada. But **how much Canadian economic activity does buying Canadian actually support?** Statistics Canada's **input-output data** trace the goods and services industries buy from one another, the imported inputs they use, and the value created by producers and their suppliers. I mapped its published **2022 national industry multipliers** into 12 consumer-facing categories and multiplied each industry's direct and upstream GDP and labour-income coefficients by a chosen amount of Canadian industry output. The app separately charts newer quarterly household spending and monthly trade, industry GDP and employment, and references 2024 input-output totals; **none of these newer figures is used to update the 2022 multipliers**. Compare domestic production relationships without mistaking industry estimates for the Canadian content of a specific retail purchase.")
 df=pd.read_csv(ROOT/'data/processed/category_coefficients.csv')
 allc=pd.read_csv(ROOT/'data/processed/industry_coefficients.csv').set_index('code')
 year=int(df.reference_year.max())
 st.info(f'The measured comparison uses {year} national industry coefficients, applied to domestic output delivered to final demand at basic prices. It is not an estimate of the Canadian content of a particular $100 retail basket. A separate sensitivity calculator accepts your own retail assumptions.')
 calc,compare,context,method=st.tabs(['Calculate','Compare categories','Recent context','Sources & method'])
 with calc:
  left,right=st.columns([1,1.4])
  with left:
   category=st.selectbox('Canadian producing industry',df.category,index=4,key='c_category')
   amount=st.number_input('Amount delivered to final demand (CAD)',min_value=0.,max_value=10000000.,value=100.,step=10.,key='c_amount')
   row=df[df.category.eq(category)].iloc[0].to_dict()
   st.caption(row['industry']+' · '+str(row['mapping_scope']))
   modes=['Industry output at basic prices']
   if not row['code'].startswith(('BS722','BS812','BS811')): modes.append('Retail sensitivity — my assumptions')
   mode=st.radio('Calculation basis',modes,key='c_mode')
   if mode.startswith('Retail'):
    st.warning('No observed product import or retail-margin shares were obtained. These controls are hypothetical inputs, not Statistics Canada category estimates. This reduced model has one Canadian retail margin; wholesale/transport services are not separately identified.')
    tax=st.number_input('Assumed sales tax (%)',min_value=0.,max_value=30.,value=13.,step=1.,key='c_tax')/100
    margin=st.slider('Canadian retail service share of pre-tax price (%)',0,100,20,key='c_margin')/100
    domestic=st.slider('Canadian-produced share of remaining basic value (%)',0,100,100,key='c_domestic')/100
    result=retail_value(amount,tax,margin,domestic,row,allc.loc[row['retailer_code']].to_dict())
    basis='Hypothetical retail decomposition using published industry coefficients'
   else:
    result=industry_value(amount,row); basis='Derived calculation: Canadian industry final demand at basic prices'
  with right:
   st.caption(basis.upper())
   a,b=st.columns(2);a.metric('Associated Canadian GDP',f"${result['gdp']:,.2f}");b.metric('Labour income within that GDP',f"${result['labour']:,.2f}")
   fig=go.Figure()
   for name,key,color in [('Direct value added','gdp_direct','#0D655F'),('Upstream value added','gdp_indirect','#76B5A8')]:
    fig.add_bar(x=[result[key]],y=['Canadian GDP'],orientation='h',name=name,marker_color=color,text=[f"${result[key]:,.2f}"],textposition='inside')
   fig.update_layout(barmode='stack',height=245,margin=dict(l=5,r=5,t=25,b=20),xaxis_title='Canadian dollars',legend=dict(orientation='h',y=-.5),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
   st.plotly_chart(fig,use_container_width=True)
   st.caption('Labour income is already included in GDP. Upstream GDP is value added by suppliers, not their gross sales. No induced household-spending effects or incremental job claims are included.')
   if mode.startswith('Retail'):
    detail=pd.DataFrame({'Component':['Canadian producer output','Canadian retail service output','Imported finished-product value','Sales tax','Canadian producer GDP','Canadian distribution GDP','Upstream imports','Product-tax/subsidy & rounding residual'], 'CAD':[result[k] for k in ['domestic_producer_output','retail_output','final_imports','tax','producer_gdp','distribution_gdp','imports','accounting_residual']]})
   else:
    detail=pd.DataFrame({'Component':['Direct GDP','Upstream GDP','Labour income (included in GDP)','Imports required upstream','Product-tax/subsidy & rounding residual'],'CAD':[result[k] for k in ['gdp_direct','gdp_indirect','labour','imports','accounting_residual']]})
   st.dataframe(detail,hide_index=True,use_container_width=True)
  export=pd.DataFrame([{**{'category':category,'basis':basis,'coefficient_year':year,'source':'36-10-0594-01'},**result}])
  st.download_button('Download this calculation (CSV)',export.to_csv(index=False),'value_added_scenario.csv','text/csv',key='c_export')
  st.caption('Associated value added does not mean net GDP newly created by this choice. The model holds industry technology and supply relationships fixed and does not model substitution, capacity or price responses.')
 with compare:
  st.subheader('$100 of Canadian industry output: different supply chains')
  choices=st.multiselect('Categories to compare',df.category,default=df.category.tolist(),key='c_compare')
  subset=df[df.category.isin(choices)].copy();subset['Direct GDP']=subset.gdp_direct*100;subset['Upstream GDP']=subset.gdp_indirect*100
  subset=subset.sort_values(['Direct GDP','Upstream GDP'])
  if not subset.empty:
   fig=go.Figure()
   for label,color in [('Direct GDP','#0D655F'),('Upstream GDP','#76B5A8')]:fig.add_bar(y=subset.category,x=subset[label],name=label,orientation='h',marker_color=color)
   fig.update_layout(barmode='stack',height=max(300,42*len(subset)+100),xaxis=dict(title='CAD per $100 of domestic industry final-demand output',range=[0,100]),margin=dict(l=5,r=15,t=20,b=50),legend=dict(orientation='h',y=-.18))
   st.plotly_chart(fig,use_container_width=True)
  st.caption(f'{year} coefficients. Categories are industry groupings, not matched retail products. Differences are not a ranking of brands or a causal buy-Canadian effect.')
  for ext,mime in [('svg','image/svg+xml'),('png','image/png')]:
   p=ROOT/f'exports/buy_canadian.{ext}'
   if p.exists():st.download_button(f'Download publication graphic ({ext.upper()})',p.read_bytes(),p.name,mime,key='c_img_'+ext)
 with context:
  st.subheader('Newer indicators, with their own clocks')
  st.markdown('These observed statistical series give context. They do not update the 2022 supply-chain coefficients or measure a product’s Canadian content.')
  spec={
   'Household spending':('36100124','Estimates','Current CAD millions, seasonally adjusted quarterly rates'),
   'Merchandise trade':('12100163','North American Product Classification System (NAPCS)','Current CAD millions, customs basis, unadjusted monthly'),
   'Industry GDP':('36100434','North American Industry Classification System (NAICS)','Chained 2017 CAD millions, seasonally adjusted annual rates'),
   'Industry employment':('14100022','North American Industry Classification System (NAICS)','Thousands of persons, monthly unadjusted; Canada, all genders, 15+')}
  source=st.selectbox('Context indicator',list(spec),key='c_context')
  table,dim,units=spec[source];ctx=pd.read_csv(ROOT/f'data/processed/{table}_clean.csv',dtype={'REF_DATE':str})
  cat=st.selectbox('Published category',sorted(ctx[dim].dropna().unique()),key='c_context_category_'+table)
  sub=ctx[ctx[dim].eq(cat)]
  if table=='12100163':
   trade=st.selectbox('Trade flow',sorted(sub.Trade.unique()),key='c_trade');sub=sub[sub.Trade.eq(trade)]
  fig=go.Figure(go.Scatter(x=sub.REF_DATE,y=sub.VALUE,mode='lines',line=dict(color='#0D655F',width=3),connectgaps=False))
  fig.update_layout(height=350,yaxis_title=units,xaxis_title='Reference period',margin=dict(l=5,r=10,t=20,b=30))
  st.plotly_chart(fig,use_container_width=True)
  st.caption(f'{len(sub):,} observations shown · {sub.REF_DATE.min()} to {sub.REF_DATE.max()} · Statistics Canada table {table[:2]}-{table[2:4]}-{table[4:]}-01. Quarterly dates mark the first month of the quarter. Gaps remain missing, not zero.')
  st.download_button('Download selected context series',sub.to_csv(index=False),f'context_{table}.csv','text/csv',key='c_ctx_export')
 with method:
  st.markdown(f'''**Evidence.** The coefficients are official national published estimates for **{year}**, released November 19, 2025. The public 2024 national input-output tables are advanced estimates, released April 15, 2026; they are archived as context, not substituted into these multipliers.

**Calculation.** Domestic final-demand output × (direct GDP coefficient + indirect GDP coefficient). We validate the sum against Statistics Canada’s **Simple multiplier**. Its separately named “Type I multiplier” is a ratio to the direct effect and must not be used as dollars per dollar.

**Why a retail result needs more data.** A checkout price includes taxes, distribution margins and the producer/import value. Detailed margin and domestic/import-use files are available upon request, according to the official table metadata. This pilot does not invent category shares. Its retail tab is a sensitivity model with user-specified assumptions and a single retail margin.

**Limits.** National averages, fixed coefficients, industry rather than brand coverage, no sampling confidence intervals, no observed 2026 inter-industry matrix, no causal incremental GDP or jobs. Broad display categories are editorial mappings to exact official industry codes, not a complete NAPCS-to-NAICS concordance.

[Detailed multipliers](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610059401) · [2022 multiplier release](https://www150.statcan.gc.ca/n1/daily-quotidien/251119/dq251119e-eng.htm) · [2024 IO release](https://www150.statcan.gc.ca/n1/daily-quotidien/260415/dq260415e-eng.htm) · [IO tables and margin availability](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3610008401)
''')
  st.dataframe(df[['category','code','industry','mapping_scope','reference_year']],hide_index=True,use_container_width=True)
  st.download_button('Download verified coefficient table',df.to_csv(index=False),'category_coefficients.csv','text/csv',key='c_coeff')
