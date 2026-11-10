"""Independent Canadian personal-finance journalism pilots. Offline by default."""
from pathlib import Path
import streamlit as st

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='The Household Economy | Research Lab',page_icon='🍁',layout='wide')
st.markdown('''<style>
.stApp{background:#f6f4ed;color:#173a40}
h1,h2,h3{font-family:Georgia,'Times New Roman',serif!important;letter-spacing:-.025em}
h1{font-size:3.1rem!important;line-height:1.12!important;max-width:1000px}
[data-testid="stSidebar"]{background:#e7ece7;border-right:1px solid #c7d0c9}
[data-testid="stMetric"]{background:#fffdf8;padding:18px;border-top:3px solid #226573;border-radius:3px}
[data-testid="stMetricValue"]{font-family:Georgia,serif;font-size:2.1rem}
.stButton>button,.stDownloadButton>button{border-color:#226573;color:#173a40}
[data-testid="stCaptionContainer"]{color:#50636a}
.block-container{padding-top:2.1rem;padding-bottom:4rem;max-width:1420px}
.kicker{font-size:.8rem;letter-spacing:.16em;font-weight:700;color:#26717a;margin-bottom:18px}
.intro{font-family:Georgia,serif;font-size:1.45rem;line-height:1.5;max-width:850px}
@media(max-width:700px){h1{font-size:2.15rem!important}.block-container{padding-left:1rem;padding-right:1rem}}
</style>''',unsafe_allow_html=True)

def home():
    st.markdown('<div class="kicker">THE HOUSEHOLD ECONOMY / AN INDEPENDENT RESEARCH LAB</div>',unsafe_allow_html=True)
    st.title('Your money moves through a bigger system.')
    st.markdown('<p class="intro">Three investigations follow that movement: through a credit-card contract, a new-home tax rebate, and the Canadian supply chain.</p>',unsafe_allow_html=True)
    st.caption('Research snapshot · November 10, 2026 · Independently developed pilots; not commissioned or endorsed by The Globe and Mail.')
    st.divider()
    columns=st.columns(3,gap='large')
    cards=[('01 / CREDIT','The payment after the minimum','Compare interest and payoff time under documented allocation rules. Read the issuer audit to see which terms are verified.','pages/1_Credit_Cards.py','Open credit-card pilot'),
           ('02 / HOUSING','The rebate and the price','Calculate legal relief, explore who benefits in a theoretical market, and examine real Ontario price and construction data.','pages/2_Ontario_Housing.py','Open housing pilot'),
           ('03 / VALUE ADDED','The economy inside a purchase','Use official input-output multipliers to compare Canadian value added, with retail assumptions kept visible.','pages/3_Buy_Canadian.py','Open value-added pilot')]
    for col,(k,title,body,path,label) in zip(columns,cards):
        with col:
            st.caption(k);st.subheader(title);st.write(body);st.page_link(path,label=label,icon=':material/arrow_forward:')
    st.divider()
    st.subheader('Know what a number represents')
    st.markdown('**Observed documents and offers** describe published terms and asking prices. **Published statistical estimates** describe markets and industries. **Derived calculations** apply disclosed formulas. **Hypothetical scenarios** let you explore assumptions. No policy-specific causal housing estimate is claimed.')
    st.write('The collected evidence is substantial but uneven. Historical matched builder prices remain a reporting gap. Detailed retail import and margin matrices were not obtained, so the retail decomposition is a sensitivity tool rather than an observed product-content estimate.')
    st.page_link('pages/4_Methods.py',label='Read the evidence, methods and limitations',icon=':material/description:')

pages=[st.Page(home,title='Start here',icon=':material/home:'),
       st.Page('pages/1_Credit_Cards.py',title='Credit-card payments',icon=':material/credit_card:',url_path='credit'),
       st.Page('pages/2_Ontario_Housing.py',title='Ontario housing',icon=':material/apartment:',url_path='housing'),
       st.Page('pages/3_Buy_Canadian.py',title='Canadian value added',icon=':material/shopping_bag:',url_path='value-added'),
       st.Page('pages/4_Methods.py',title='Methods & evidence',icon=':material/description:',url_path='methods')]
nav=st.navigation(pages)
with st.sidebar:
    st.markdown('---');st.caption('All scenarios run locally. No account or paid data connection required. Source vintages appear on each page.')
nav.run()
