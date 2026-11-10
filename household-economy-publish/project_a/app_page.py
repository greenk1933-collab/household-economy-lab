from pathlib import Path
import json
from .model import Segment,simulate
BASE=Path(__file__).parent

def render():
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go
    st.caption('CONTRACT AUDIT / CANADA / VERIFIED NOVEMBER 10, 2026')
    st.title('Where does your credit-card payment really go?')
    st.markdown("On November 5, 2026, Canada's federal government announced in Budget 2026 that it would consult on requiring credit-card payments above the minimum to pay down the highest-interest balance first across Canada, as Quebec already requires, to help borrowers reduce interest costs. I reviewed **24 card-family and jurisdiction records across 11 issuers: RBC, TD, BMO, CIBC, Scotiabank, National Bank, Tangerine, Simplii, PC Financial, Canadian Tire Bank and Desjardins.** Most audited issuers allocate excess payments proportionally outside Quebec, while Desjardins uses highest-rate-first there too. Using verified Tangerine card terms, this calculator holds the payment fixed and compares both rules. In an illustrative $11,000 debt scenario, highest-rate-first saves **$95.16 in interest**. Change the balances, rates and payments to test the effect on your own repayment path.")
    audit=pd.read_csv(BASE/'data/processed/issuer_audit.csv')
    enabled=audit[audit.simulation_enabled.astype(str).str.lower().eq('true')].copy()
    enabled['choice']=enabled.issuer+' — '+enabled.card
    tab,review=st.tabs(['Repayment calculator','Institution audit'])
    with tab:
        c1,c2=st.columns(2)
        with c1:
            product=st.selectbox('Verified issuer / product',enabled.choice.drop_duplicates().tolist())
        with c2: region=st.selectbox('Jurisdiction',enabled.loc[enabled.choice.eq(product),'jurisdiction'].tolist())
        contract=enabled[enabled.choice.eq(product)&enabled.jurisdiction.eq(region)].iloc[0]
        q=region=='Quebec'
        st.info(('Quebec: payments go to highest-rate balances first.' if q else 'Outside Quebec: minimum pays interest and fees first, then lowest-rate principal; excess is proportional to the remaining balances.')+' Documented in Tangerine agreement §20; minimum in matched disclosure. Only products with verified rate and minimum disclosures are enabled.')
        cols=st.columns(3)
        with cols[0]: purchases=st.number_input('Interest-bearing purchases ($)',0.,1000000.,5000.,100.,key='a_purchases');apr=st.number_input('Purchase APR (%)',0.,100.,round(float(contract.purchase_apr)*100,2),.01,key='a_apr')
        with cols[1]: cash=st.number_input('Cash-advance balance ($)',0.,1000000.,1000.,100.,key='a_cash');capr=st.number_input('Cash-advance APR (%)',0.,100.,round(float(contract.cash_apr)*100,2),.01,key='a_cashapr')
        with cols[2]: transfer=st.number_input('Transfer balance ($)',0.,1000000.,5000.,100.,key='a_transfer');tapr=st.number_input('Transfer APR for initial period (%)',0.,100.,1.95,.01,key='a_tapr')
        cols=st.columns(3)
        with cols[0]: expiry=st.number_input('Initial transfer-rate periods remaining',0,120,6,key='a_expiry')
        with cols[1]: after=st.number_input('Transfer APR after expiry (%)',0.,100.,22.95,.01,key='a_after')
        with cols[2]: payment=st.number_input('Fixed payment each month ($)',0.,1000000.,600.,25.,key='a_payment')
        st.caption('Published standard APR defaults; edits are your scenario assumptions. Six periods represents an eligible 1.95% introductory offer; an existing transfer may have fewer periods remaining. Set zero periods to start at the post-expiry rate.')
        ss=[Segment('Purchases',purchases,apr/100),Segment('Cash',cash,capr/100),Segment('Transfer',transfer,tapr/100,int(expiry),after/100)]
        opts=dict(minimum_rule='five_percent' if q else 'interest_plus_10',minimum_allocation='highest' if q else 'interest_then_lowest')
        actual=simulate(ss,payment,excess_rule=contract.allocation_of_excess,**opts)
        alternative=simulate(ss,payment,excess_rule='highest',**opts)
        valid=actual['status']=='paid_off' and alternative['status']=='paid_off'
        if not valid:
            for label,result in [('Contract rule',actual),('Highest-rate-first excess',alternative)]:
                if result['status']=='below_minimum':st.error(f"{label}: payment is below the required ${result['required_payment']:,.2f} in period {result['failed_month']}. Projection stops before that payment; default fees and rate changes are not simulated.")
                elif result['status']=='horizon_reached':st.warning(f'{label}: debt remains after 1,200 periods. No payoff date is reported.')
        else:
            c1,c2,c3=st.columns(3)
            c1.metric('Contract-rule interest',f"${actual['total_interest']:,.2f}",f"{actual['months']} months",delta_color='off')
            c2.metric('Highest-first interest',f"${alternative['total_interest']:,.2f}",f"{alternative['months']} months",delta_color='off')
            c3.metric('Interest difference',f"${actual['total_interest']-alternative['total_interest']:,.2f}")
        fig=go.Figure()
        frames=[]
        for label,color,result in [('Contract rule','#ac452d',actual),('Highest-rate-first excess','#006b67',alternative)]:
            df=pd.DataFrame(result['rows']);df['scenario']=label;frames.append(df)
            fig.add_trace(go.Scatter(x=df.month,y=df.balance,name=label,line=dict(color=color,width=3),hovertemplate='Month %{x}<br>Debt $%{y:,.2f}<extra>%{fullData.name}</extra>'))
        fig.update_layout(title='One payment, two repayment paths',xaxis_title='Synthetic monthly period',yaxis_title='Remaining debt (CAD)',height=400,legend=dict(orientation='h',y=1.12),margin=dict(l=20,r=20,b=30,t=65),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig,width='stretch',key='a_chart')
        st.download_button('Download this comparison (CSV)',pd.concat(frames).to_csv(index=False),'credit_scenario.csv','text/csv',key='a_csv')
        with st.expander('How the calculation works and what it leaves out'):
            st.markdown('**Derived scenario, not an exact statement forecast.** All starting purchases are already interest bearing. Each synthetic month charges APR ÷ 12 on principal, then receives one payment. Interest is tracked separately and never charged interest. The minimum rule is applied first; only excess allocation changes in the counterfactual. Quebec uses a 5% minimum with a $10 floor. Other provinces use interest plus $10. Payments below the minimum stop the calculation. No new purchases, transaction dates, grace periods, fees, insurance, instalments, arrears, missed-payment repricing or account-specific overrides. Include any existing transfer fee in your starting debt if appropriate; new transfer fees are excluded. Dollar rounding occurs for display only. World Elite annual fees are not added.')
        st.markdown('[Tangerine agreement, APRs and minimum formulas](https://www.tangerine.ca/en/legal/credit-card-cardholder-agreement) · Agreement effective April 22, 2026; Money-Back rate disclosure dated October 3, 2024, World Elite dated April 22, 2026. Retrieved November 10, 2026.')
        st.markdown('**Policy status:** Budget 2026 announces an intention to consult on requiring highest-rate-first excess payments. It does not establish an enacted nationwide change. The retrieved Bank Act §627.35 still permits either method. [Budget 2026](https://budget.canada.ca/2026/report-rapport/chap3-en.html) · [Bank Act](https://laws-lois.justice.gc.ca/eng/acts/B-1.01/section-627.35.html)')
    with review:
        st.subheader('Read the clause, then check its amendments')
        st.write(f'{len(audit)} product-family/jurisdiction records across {audit.issuer.nunique()} issuer brands. Shared agreements are not counted as independent cards or a representative market census. Blank APRs mean the product disclosure was not verified.')
        st.dataframe(audit[['issuer','card','jurisdiction','allocation_of_excess','rule_confidence','clause_or_page','agreement_url']],hide_index=True,width='stretch',column_config={'agreement_url':st.column_config.LinkColumn('Primary agreement')})
        st.warning('National Bank’s retrieved base PDF gives proportional allocation but does not resolve later Quebec amendments. Its Quebec rule remains unresolved. Scotiabank’s Quebec amendment must be read with its March 2025 base agreement. No unverified institution-specific simulation is offered.')
        st.markdown('**RBC comparison:** §8 of the January 2026 agreement specifies highest-rate-first payments in Quebec (without instalment plans), and proportional excess allocation elsewhere. Product disclosures remain account specific. [RBC agreement](https://www.rbcroyalbank.com/credit-cards/cardholders/additional-documents/rbc-royal-bank-credit-card-agreement.pdf)')
        st.download_button('Download the full coded audit',audit.to_csv(index=False),'issuer_audit.csv','text/csv',key='a_audit_csv')
        chart=BASE/'exports/credit_cards.png'
        if chart.exists():st.download_button('Download the static graphic (PNG)',chart.read_bytes(),'credit_cards.png','image/png',key='a_png')
