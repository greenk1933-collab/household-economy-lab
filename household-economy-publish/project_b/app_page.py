from pathlib import Path
from datetime import date
import pandas as pd
from project_b.model import acquisition_cost,incidence,incidence_curves

ROOT=Path(__file__).resolve().parent
E=ROOT/'evidence/processed'
RULE_URL='https://www.canada.ca/en/revenue-agency/services/forms-publications/publications/notice346/ontario-enhanced-new-housing-rebate.html'
def money(x): return f'${x:,.0f}'

def chart_style(fig,**kwargs):
    fig.update_layout(template='plotly_white',font=dict(family='Arial',size=14,color='#183a40'),
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=15,r=20,t=45,b=25),legend=dict(orientation='h',y=-.2),**kwargs)
    return fig

def render():
    import streamlit as st
    import plotly.graph_objects as go
    import plotly.express as px
    st.caption('ONTARIO HOUSING  /  LEGAL RULES · THEORY · OBSERVED MARKETS')
    st.title('Who gets the value of new-home tax relief?')
    st.markdown("In its March 26, 2026 budget, Ontario introduced temporary relief of up to **$130,000 in HST** for eligible buyers of new homes under qualifying agreements signed from April 1, 2026, through March 31, 2027, aiming to improve affordability and support construction. But who ultimately benefits? **Supply-and-demand tax-incidence theory** explains that a tax cut's value is shared according to how strongly buyers and sellers respond to price changes; the less price-responsive side generally captures more. This tool begins with that economic model, then combines a statutory rebate and closing-cost calculator with Statistics Canada regional new-home price and construction data, published housing elasticity research, and **48 advertised model and elevation offers from one Ontario builder**. Explore the possible division of relief, while recognizing that the evidence does not establish how much developers actually captured.")
    calc,theory,observed=st.tabs(['Rebate & closing costs','Who benefits?','Regional evidence'])
    with calc:
        st.subheader('Start with the actual tax rules')
        st.caption('Rule snapshot: November 10, 2026 · Builder sale of a new home and its land, including a condominium · CAD')
        c1,c2=st.columns([1,1.25],gap='large')
        with c1:
            quote=st.number_input('Price in the builder quote (CAD)',min_value=10000.,max_value=30000000.,value=1000000.,step=10000.,key='b_price')
            basis_label=st.selectbox('What does the quote include?',['Before HST','HST included, before rebates','HST included, stated rebates already deducted'],key='b_basis')
            basis={'Before HST':'exclusive','HST included, before rebates':'inclusive','HST included, stated rebates already deducted':'inclusive_net'}[basis_label]
            included=st.number_input('Documented rebates already deducted from quote (CAD)',min_value=0.,max_value=130000.,value=24000.,step=1000.,key='b_included') if basis=='inclusive_net' else 0.
            municipality=st.selectbox('Municipality',['Other Ontario','Toronto','Ottawa','Hamilton','London','Kitchener-Waterloo','Markham','Barrie'],key='b_municipality')
            st.selectbox('Property type',['New freehold home and land','New condominium and land interest'],key='b_type')
            primary=st.checkbox('Meets ordinary primary-residence rebate conditions',value=True,key='b_primary',help='Individual purchaser, buyer or eligible relation occupies as the first resident, new/substantially renovated home and land from one builder, tax paid, application deadlines and all ordinary CRA conditions met. Not a rental purchase.')
            first=st.checkbox('Meets federal first-time buyer conditions',value=False,key='b_first',help='Age 18+, Canadian citizen/permanent resident, qualifying primary residence; neither applicant nor spouse owned a home they lived in during the current or preceding four calendar years; first occupation and no prior first-time rebate. Self-certified, not determined by this app.')
            with st.expander('Agreement, construction & transfer dates',expanded=False):
                aps=st.date_input('Original purchase agreement',date(2026,6,1),min_value=date(2017,1,1),max_value=date(2027,3,31),key='b_aps')
                start=st.date_input('Construction begins',date(2026,7,1),min_value=date(2010,1,1),max_value=date(2035,12,31),key='b_start')
                complete=st.date_input('Substantial completion',date(2027,6,1),min_value=date(2017,1,1),max_value=date(2035,12,31),key='b_complete')
                close=st.date_input('Ownership transfer / tax payable',date(2027,7,1),min_value=date(2017,1,1),max_value=date(2036,12,31),key='b_close')
                possession=st.date_input('Possession',date(2027,7,1),min_value=date(2017,1,1),max_value=date(2036,12,31),key='b_possession')
                original=st.checkbox('Original agreement; no assignment or anti-avoidance issue',True,key='b_original')
                st.caption('Dates after March 31, 2027 for a new agreement are outside this pilot: announced ordinary-rebate termination and transition rules need legal review. Owner-built, rental, co-op and leased-land cases use different rules.')
            with st.expander('Credits, incentives & closing charges'):
                cra_credit=st.checkbox('Builder credits CRA rebates at closing',True,key='b_cra_credit')
                onhap_credit=st.checkbox('Builder also credits ONHAP at closing',False,key='b_onhap_credit')
                ltt=st.checkbox('Qualifies for full first-time land-transfer-tax refunds',False,key='b_ltt_first',help='Separate lifetime ownership, spouse, citizenship/permanent residency, occupancy and application tests apply. Not the same as the federal four-year first-time definition. Assumes 100% eligible ownership.')
                charges=st.number_input('Other closing charges, including applicable tax (CAD)',0.,1000000.,0.,500.,key='b_charges')
                incentive=st.number_input('Additional after-tax cash incentive, not already in quote (CAD)',0.,1000000.,0.,1000.,key='b_incentive')
                st.caption('Add lawyer, registration, title insurance, development charges and adjustments from your documents. Toronto’s $102.56 + HST MLTT administration fee is not automatically included. Decor allowances are not cash. Incentives that change taxable consideration must instead be reflected in the price.')
        with c2:
            try:
                r=acquisition_cost(quote,basis,included,primary,first,original,aps,start,complete,close,possession,
                    municipality,cra_credit,onhap_credit,ltt,charges,incentive)
            except ValueError as error:
                st.error(str(error));r=None
            if r:
                a,b=st.columns(2)
                a.metric('Total statutory relief',money(r['total_relief']))
                b.metric('Net acquisition cost',money(r['total_cost']))
                st.caption('Derived legal calculation at your stated price; not measured economic benefit. Excludes financing and any charges not entered.')
                labels={'price_excluding_hst':'Price before HST','hst':'13% HST','ontario_rebate':'Ontario rebate (ordinary + eligible top-up)','federal_rebate':'Federal rebate (ordinary + eligible first-time top-up)','onhap':'Ontario affordability payment (net of federal rebate)','ontario_ltt':'Ontario land transfer tax after any refund','toronto_ltt':'Toronto land transfer tax after any refund','closing_charges':'Other entered closing charges','incentive':'Additional entered after-tax cash incentive'}
                table=pd.DataFrame([{'Component':label,'CAD':r[k]} for k,label in labels.items()])
                st.dataframe(table,hide_index=True,width='stretch',column_config={'CAD':st.column_config.NumberColumn(format='$%.2f')})
                st.metric('Additional relief versus ordinary rebates',money(r['additional_vs_ordinary']))
                if first: st.caption(f"Against a baseline that also includes eligible first-time relief, the temporary measure adds {money(r['additional_vs_no_temporary_relief'])}.")
                st.markdown(f"**Cash required before later rebates:** {money(r['closing_cash_cost'])}  \n**Later rebate receivable:** {money(r['later_receivable'])}")
                st.caption('Cash required is the full purchase and entered closing amount before subtracting your deposits or mortgage. Builder assignment changes timing, not the entitlement. Ontario expects direct ONHAP payments to start in early 2027; payment date is not guaranteed.')
                st.info('Enhanced-period eligibility passed.' if r['enhanced_eligible'] else 'Enhanced-period eligibility not met. The displayed result retains only other eligible relief under the selected assumptions.')
                st.download_button('Download my closing-cost calculation',pd.DataFrame([r]).to_csv(index=False),'ontario_closing_costs.csv','text/csv',key='b_cost_csv')
        st.markdown(f'[CRA Notice 346]({RULE_URL}) · [Provincial rebate regulation, s. 41](https://laws-lois.justice.gc.ca/eng/regulations/SOR-2010-151/FullText.html) · [ONHAP regulation, ss. 5–6](https://www.ontario.ca/laws/regulation/260196) · [Ontario LTT](https://www.ontario.ca/document/land-transfer-tax/calculating-land-transfer-tax) · [Toronto LTT](https://www.toronto.ca/services-payments/property-taxes-utilities/municipal-land-transfer-tax-mltt/municipal-land-transfer-tax-mltt-rates-and-fees/)')
        st.caption('This pilot does not determine personal legal eligibility. Complex ownership, assignments, non-resident taxes, application deadlines and unusual supply arrangements require the original legal documents and professional review.')
    with theory:
        st.subheader('The less responsive side gets more of a tax cut')
        st.info('HYPOTHETICAL SENSITIVITY MODEL. These sliders are not measured local elasticities. This is a uniform dollar tax change in a competitive linear market, separate from Ontario’s nonlinear HST schedule.')
        left,right=st.columns([1,1.7],gap='large')
        with left:
            ed=st.slider('Demand responsiveness |Ed|',0.,6.,1.,.05,key='b_ed',help='Larger values mean buyers change quantity more for a given percentage price change.')
            es=st.slider('Supply responsiveness Es',0.,6.,.5,.05,key='b_es',help='Larger values mean sellers change quantity more. Fixed inventory can be less responsive than long-run construction capacity.')
            p=st.number_input('Benchmark price (CAD)',min_value=10000.,max_value=10000000.,value=800000.,step=10000.,key='b_p0')
            q=st.number_input('Benchmark quantity (index)',min_value=1.,max_value=100000.,value=100.,step=10.,key='b_q0')
            dt=st.slider('Illustrative tax change per unit (CAD)',-100000,100000,-20000,1000,key='b_dt')
            horizon=st.radio('Interpretation of your chosen elasticities',['Near-term inventory','Long-run capacity'],key='b_horizon')
            st.caption('The horizon changes the interpretation, not the parameters automatically. A longer horizon does not supply a measured elasticity.')
        with right:
            try:
                curves=incidence_curves(ed,es,p,q,dt);r=curves['result']
                fig=go.Figure()
                for key,name,color,dash in [('demand','Demand','#1d6773','solid'),('supply','Supply before','#898b83','dash'),('supply_after','Supply after tax change','#b15335','solid')]:
                    fig.add_trace(go.Scatter(x=curves[key],y=curves['price'],mode='lines',name=name,line=dict(color=color,dash=dash,width=3)))
                fig.add_trace(go.Scatter(x=[q,r['quantity'],r['quantity']],y=[p,r['buyer_price'],r['seller_price']],mode='markers',name='Before / buyer / seller',marker=dict(color=['#898b83','#1d6773','#b15335'],size=11)))
                fig.add_shape(type='line',x0=r['quantity'],x1=r['quantity'],y0=r['seller_price'],y1=r['buyer_price'],line=dict(color='#262c2d',width=3,dash='dot'))
                fig.update_xaxes(title='Quantity index',range=[max(0,q*.65),max(q*1.35,r['quantity']*1.1)])
                fig.update_yaxes(title='CAD per unit',tickformat='$,.0f')
                chart_style(fig,height=440,title='One tax change, two price responses')
                st.plotly_chart(fig,width='stretch',key='b_incidence_plot')
                a,b,c=st.columns(3);a.metric('Buyer share',f"{r['buyer_share']:.1%}");b.metric('Seller share',f"{r['producer_share']:.1%}");c.metric('Quantity change',f"{r['quantity_change']:+.2f}")
                st.markdown(f"Buyer price: **{money(r['buyer_price'])}** · Seller’s net price: **{money(r['seller_price'])}**")
                st.caption(f"{horizon}. Negative tax change: buyer savings and seller gain. Positive tax change: buyer burden and seller loss. The prices differ by {money(dt)} relative to the zero-wedge benchmark.")
                st.download_button('Download this incidence scenario',pd.DataFrame([dict(ed=ed,es=es,benchmark_price=p,benchmark_quantity=q,horizon=horizon,**r)]).to_csv(index=False),'incidence_scenario.csv','text/csv',key='b_incidence_csv')
            except ValueError as error: st.warning(str(error))
        st.markdown('**From the course to the investigation.** In CECN104 Module 4, Figure 4.6 (PDF pp. 30–31) shows a tax raising the buyer’s price and lowering the seller’s net price. Figures 4.7–4.8 (pp. 32–34) explain why the less responsive side bears more. Reverse the tax change in the same competitive model and that side receives more of the benefit. Market power, buyer-specific eligibility and changing construction costs can break that simple comparison.')
        st.latex(r'\text{Buyer share}=\frac{E_s}{E_s+|E_d|},\qquad \text{Seller share}=\frac{|E_d|}{E_s+|E_d|}')
        st.caption('The formula is marginal for general demand and supply curves. The plotted finite response is exact only for the specified linear curves calibrated at a common price and quantity. Their elasticities change away from that point. Both elasticities zero is indeterminate; shocks producing nonpositive prices or quantities are blocked. A negative wedge represents an illustrative subsidy, not the actual Ontario tax bill.')
    with observed:
        st.subheader('What the regional data can tell us')
        st.warning('No policy-specific causal capture rate is identified. There is no verified matched property panel spanning the policy change. Index changes, offers and published elasticity estimates below are separate evidence.')
        prices=pd.read_csv(E/'nhpi_regional.csv')
        regions=prices.region.drop_duplicates().tolist()
        selected=st.multiselect('Compare regions',regions,default=[x for x in regions if x in ['Toronto, Ontario','Ottawa-Gatineau, Ontario part, Ontario/Quebec','London, Ontario']],key='b_regions')
        component=st.selectbox('Price-index component',prices.component.unique(),key='b_component')
        startyear=st.slider('First chart year',2017,2026,2022,key='b_year')
        view=prices[prices.region.isin(selected)&prices.component.eq(component)&(prices.period>=str(startyear))].copy()
        if not view.empty:
            view['date']=pd.to_datetime(view.period)
            fig=px.line(view,x='date',y='value',color='region',labels={'value':'New housing price index (Dec. 2016 = 100)','date':''})
            fig.add_vline(x=date(2026,4,1).isoformat(),line_dash='dot',line_color='#b15335')
            st.plotly_chart(chart_style(fig,height=420),width='stretch',key='b_nhpi_plot')
            st.caption(f'{len(view):,} published observations shown · Through {prices.period.max()} · Dotted line: enhanced APS window opens, April 1, 2026. Index excludes GST/HST, covers singles/semis/townhomes, excludes condos; not seasonally adjusted. Index levels are not comparable dollar home prices.')
        else: st.info('Select at least one region to display the price index.')
        latest=pd.read_csv(E/'nhpi_latest_comparison.csv').sort_values('year_over_year_pct')
        fig=px.bar(latest,x='year_over_year_pct',y='region',orientation='h',labels={'year_over_year_pct':'Year-over-year change (%)','region':''},color_discrete_sequence=['#1d6773'])
        st.plotly_chart(chart_style(fig,height=450,title=f"New-home price index change · {latest.period.max()}"),width='stretch',key='b_region_compare')
        st.caption('Derived from the published house-and-land index. Falling observed prices do not prove that all relief reached buyers: the missing counterfactual could have fallen more.')
        construction=pd.read_csv(E/'housing_construction_regional.csv')
        cc1,cc2=st.columns(2)
        cr=cc1.selectbox('Construction market',construction.region.unique(),index=list(construction.region.unique()).index('Toronto, Ontario') if 'Toronto, Ontario' in construction.region.unique() else 0,key='b_construction_region')
        ci=cc2.selectbox('Construction measure',construction.indicator.unique(),key='b_indicator')
        unit=st.selectbox('Housing type in construction series',construction.unit_type.unique(),key='b_unit')
        cv=construction[construction.region.eq(cr)&construction.indicator.eq(ci)&construction.unit_type.eq(unit)&(construction.period>=str(startyear))]
        fig=px.line(cv,x='period',y='value',labels={'value':'Units','period':''},color_discrete_sequence=['#b15335'])
        st.plotly_chart(chart_style(fig,height=300,title=ci+' · '+cr),width='stretch',key='b_construction_plot')
        st.caption('Monthly raw counts, not annualized and not seasonally adjusted. Starts/completions are flows; under-construction units are a stock. Do not add these measures or treat them as measured elasticities.')
        st.markdown('[StatCan NHPI 18-10-0205-01](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1810020501) · [Construction 34-10-0154-01, CMHC source](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=3410015401)')
        st.subheader('Builder evidence: what is actually advertised')
        offers=pd.read_csv(E/'developer_model_prices.csv')
        st.caption(f'{len(offers)} model/elevation offers from one Fieldgate price list; no closed transactions or repeated lot identifiers. The two price columns reflect advertised rebate treatment at the same date, not a before/after price history.')
        st.dataframe(offers[['model','elevation','area_sqft','base_price_cad','advertised_rebate_cad','after_rebate_price_cad']],hide_index=True,width='stretch')
        st.markdown('[Original Fieldgate price list](https://www.fieldgatehomes.com/upper-east/brokerportal/files/PriceList/UES-NEW-RELEASE-PRICE-LIST-AUG-12.pdf)')
        archived=pd.read_csv(E/'developer_price_observations.csv')
        with st.expander('Property-history search and unmatched archival leads'):
            st.markdown('The historical Tamarack PDF returned 404. Its search-index figures are retained only as **unverified archival leads**, excluded from published change calculations. One current offer was verified in the live builder page. A changed area measurement and unclear tax basis also prevent a clean matched comparison.')
            st.dataframe(archived[['address','observation_date','price_cad','evidence_class','comparability_note']],hide_index=True,width='stretch')
        with st.expander('Published elasticities: different scopes, not local rebate shares'):
            literature=pd.read_csv(E/'published_elasticities.csv')
            st.dataframe(literature,hide_index=True,width='stretch')
            st.caption('Confidence intervals absent from these extracted records are missing, not zero. No Toronto or Ottawa demand coefficient is invented. The national demand estimate and city supply estimates must not be combined into a measured local incidence number.')
        st.download_button('Download regional price observations',prices.to_csv(index=False),'nhpi_regional.csv','text/csv',key='b_nhpi_csv')
        st.download_button('Download observed builder offers',offers.to_csv(index=False),'builder_offers.csv','text/csv',key='b_offers_csv')
    chart=ROOT/'exports/ontario_tax_incidence.png'
    if chart.exists(): st.download_button('Download housing graphic (PNG)',chart.read_bytes(),chart.name,'image/png',key='b_png')

if __name__=='__main__':render()
