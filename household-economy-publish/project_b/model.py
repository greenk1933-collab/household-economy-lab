"""Ontario builder-purchase statutory calculation and separate illustrative incidence.

Rule snapshot: 2026-11-10. Only a home AND land purchased from one builder,
ordinary Ontario residential use, original APS 2017-01-01 to 2027-03-31.
No rental, co-op, leased land, owner-built, assignment or non-resident tax modelling.
Sources and legal locators are in data/processed/tax_rules.csv.
"""
from datetime import date
import math

def finite_nonnegative(x, name):
    if not math.isfinite(x) or x < 0:
        raise ValueError(f'{name} must be finite and nonnegative')

def ordinary_federal(p):
    finite_nonnegative(p,'price')
    if p <= 350_000: return .018*p
    return max(0.,6300*(450_000-p)/100_000)

def ordinary_ontario(p):
    finite_nonnegative(p,'price')
    return min(24_000.,.06*p)

def enhanced_ontario(p):
    """Total ordinary + ENHR, NOT additional ENHR alone; s41(2),(2.01)."""
    base=ordinary_ontario(p)
    top=max(0.,min(.08*p,80_000)-base)
    phase=min(1.,max(0.,(1_850_000-p)/350_000))
    return base+top*phase

def first_federal(p):
    finite_nonnegative(p,'price')
    return min(.05*p,50_000.)*min(1.,max(0.,(1_500_000-p)/500_000))

def first_ontario(p):
    """s41(2.1) adds only positive top-up to ordinary rebate."""
    finite_nonnegative(p,'price')
    return max(ordinary_ontario(p), min(.08*p,80_000.)*min(1.,max(0.,(1_500_000-p)/500_000)))

def onhap_gross(p):
    finite_nonnegative(p,'price')
    return min(.05*p,50_000.)*min(1.,max(0.,(1_850_000-p)/350_000))

def land_transfer(p, toronto=False, closing=date(2026,11,10)):
    finite_nonnegative(p,'consideration')
    brackets=[(55_000,.005),(250_000,.01),(400_000,.015),(2_000_000,.02)]
    if toronto and closing>=date(2024,1,1):
        high=[.044,.0545,.065,.0755,.086] if closing>=date(2026,4,1) else [.035,.045,.055,.065,.075]
        brackets += [(3_000_000,.025),(4_000_000,high[0]),(5_000_000,high[1]),(10_000_000,high[2]),(20_000_000,high[3]),(float('inf'),high[4])]
    else: brackets += [(float('inf'),.025)]
    total=0.;lower=0.
    for upper,rate in brackets:
        total+=max(0.,min(p,upper)-lower)*rate
        if p<=upper: break
        lower=upper
    return total

def acquisition_cost(quoted_price=1_000_000., basis='exclusive', included_rebate=0.,
                     primary_eligible=True, first_time=False, original_agreement=True,
                     agreement=date(2026,6,1), construction=date(2026,7,1),
                     completion=date(2027,6,1), closing=date(2027,7,1), possession=None,
                     municipality='Other Ontario', credit_cra=True, credit_onhap=False,
                     ltt_first_time=False, closing_charges=0., after_tax_incentive=0.):
    """Nominal CAD, dates and self-certified eligibility, no assumed financing.

    `inclusive_net` adds back the documented dollar rebate before dividing by 1.13.
    Separate assignment flags change cash timing, never the total entitlement.
    Post-March-2027 APS intentionally blocked: proposed ordinary-rebate termination
    is not silently treated as consolidated law.
    """
    for n,x in [('price',quoted_price),('included rebate',included_rebate),('charges',closing_charges),('incentive',after_tax_incentive)]: finite_nonnegative(x,n)
    if not date(2017,1,1)<=agreement<=date(2027,3,31):
        raise ValueError('Supported original agreement dates: Jan 1, 2017 to Mar 31, 2027. Later ordinary-rebate transition needs review.')
    possession=possession or closing
    if completion<construction or closing<agreement or closing<completion or possession<completion:
        raise ValueError('Dates must follow construction, substantial completion and transfer/possession chronology.')
    if not original_agreement:
        raise ValueError('Assignments, cancelled/replaced agreements and material amendments need individual review; no eligibility estimate supplied.')
    if basis=='exclusive': p=quoted_price
    elif basis=='inclusive': p=quoted_price/1.13
    elif basis=='inclusive_net': p=(quoted_price+included_rebate)/1.13
    else: raise ValueError('Unknown price basis')
    if p<=0: raise ValueError('Price must be positive')
    if after_tax_incentive > p: raise ValueError('Incentive exceeds supported price')
    base_on=ordinary_ontario(p) if primary_eligible else 0.
    base_fed=ordinary_federal(p) if primary_eligible else 0.
    enhanced_ok=bool(primary_eligible and date(2026,4,1)<=agreement<=date(2027,3,31)
                     and construction<=date(2028,12,31) and completion<=date(2031,12,31)
                     and closing<=date(2032,12,31) and possession<=date(2032,12,31) and p<1_850_000)
    first_ok=bool(primary_eligible and first_time and agreement>=date(2025,3,20)
                  and construction<=date(2030,12,31) and completion<=date(2035,12,31))
    federal=max(base_fed,first_federal(p) if first_ok else 0.)
    provincial=max(base_on,enhanced_ontario(p) if enhanced_ok else 0.,first_ontario(p) if first_ok else 0.)
    onhap=max(0.,onhap_gross(p)-federal) if enhanced_ok else 0.
    # ENHR + FTHB are capped at min(8% tax,80k); enhanced dominates within overlap.
    total=provincial+federal+onhap
    cra_credit=(provincial+federal) if credit_cra else 0.
    topup_credit=onhap if credit_onhap else 0.
    ontario_ltt=max(0.,land_transfer(p)-(4000 if ltt_first_time else 0))
    toronto_ltt=max(0.,land_transfer(p,True,closing)-(4475 if ltt_first_time else 0)) if municipality=='Toronto' else 0.
    taxes=p*.13
    total_cost=p+taxes-total+ontario_ltt+toronto_ltt+closing_charges-after_tax_incentive
    cash_cost=p+taxes-cra_credit-topup_credit+ontario_ltt+toronto_ltt+closing_charges-after_tax_incentive
    no_enhanced_prov=max(base_on,first_ontario(p) if first_ok else 0.)
    return dict(price_excluding_hst=p,hst=taxes,ordinary_ontario=base_on,ordinary_federal=base_fed,
                federal_rebate=federal,ontario_rebate=provincial,onhap=onhap,total_relief=total,
                enhanced_eligible=enhanced_ok,first_eligible=first_ok,
                additional_vs_ordinary=total-base_on-base_fed,
                additional_vs_no_temporary_relief=total-no_enhanced_prov-federal,
                ontario_ltt=ontario_ltt,toronto_ltt=toronto_ltt,closing_charges=closing_charges,
                incentive=after_tax_incentive,total_cost=total_cost,closing_cash_cost=cash_cost,
                later_receivable=total-cra_credit-topup_credit,
                included_rebate_in_quote=included_rebate if basis=='inclusive_net' else 0.)

def incidence(ed=1.,es=.5,price=800_000.,quantity=100.,tax_change=-20_000.):
    """Exact interior solution for LINEAR curves calibrated at zero-wedge benchmark.

    Ed and Es are magnitudes. Elasticities apply at P0,Q0, not along entire lines.
    Negative delta means illustrative subsidy/cut; not the Ontario HST schedule.
    """
    for n,x in [('demand elasticity',ed),('supply elasticity',es),('price',price),('quantity',quantity)]: finite_nonnegative(x,n)
    if price<=0 or quantity<=0 or ed+es<=0 or not math.isfinite(tax_change): raise ValueError('Invalid or indeterminate equilibrium')
    share=es/(es+ed)
    buyer=price+share*tax_change
    seller=price-(1-share)*tax_change
    q=quantity-(ed*es/(ed+es))*quantity/price*tax_change
    if min(buyer,seller,q)<=0: raise ValueError('Shock exceeds positive interior domain of the linear model')
    return dict(buyer_share=share,producer_share=1-share,buyer_price=buyer,seller_price=seller,
                quantity=q,quantity_change=q-quantity,buyer_price_change=buyer-price,
                seller_price_change=seller-price,tax_change=tax_change,
                buyer_benefit=price-buyer,producer_benefit=seller-price)

def incidence_curves(ed,es,price,quantity,tax_change):
    # Plot forward quantity functions; zero elasticity gives vertical line naturally.
    result=incidence(ed,es,price,quantity,tax_change)
    span=max(abs(tax_change)*2,price*.15)
    prices=[max(.01,price-span)+i*(price+span-max(.01,price-span))/100 for i in range(101)]
    return dict(price=prices,
                demand=[quantity*(1-ed*(p-price)/price) for p in prices],
                supply=[quantity*(1+es*(p-price)/price) for p in prices],
                supply_after=[quantity*(1+es*(p-tax_change-price)/price) for p in prices],result=result)
