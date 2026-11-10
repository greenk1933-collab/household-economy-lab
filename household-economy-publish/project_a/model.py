"""Revolving, already-interest-bearing debt; dollars and APR fractions.

Payments occur at each synthetic month end. Interest is APR/12 on principal;
unpaid interest is held separately (no interest on interest). No purchases,
fees, instalments, grace period or default repricing. This is a scenario engine,
not a statement reconstruction. Minimum allocation is held fixed when comparing
excess allocation, so the counterfactual isolates the rule being investigated.
"""
from dataclasses import dataclass
from math import isfinite

@dataclass(frozen=True)
class Segment:
    name: str
    balance: float
    apr: float
    promo_months: int = 0
    post_promo_apr: float | None = None

def allocate(balances, amount, rates, method):
    """Nonnegative, capped allocations; funds exhausted unless debt is paid."""
    if method not in ('highest', 'lowest', 'proportional'):
        raise ValueError('Unknown allocation method')
    if len(balances) != len(rates) or any(not isfinite(v) or v < 0 for v in balances):
        raise ValueError('Invalid balances')
    if not isfinite(amount) or amount < 0:
        raise ValueError('Invalid payment')
    usable = min(amount, sum(balances))
    result = [0.0]*len(balances)
    if usable == 0:
        return result
    if method == 'proportional':
        result = [usable*b/sum(balances) for b in balances]
    else:
        remaining = usable
        for i in sorted(range(len(balances)), key=lambda i: rates[i], reverse=method=='highest'):
            result[i] = min(balances[i],remaining)
            remaining -= result[i]
    assert abs(sum(result)-usable) < 1e-7 * max(1,usable)
    assert all(-1e-8 <= a <= b+1e-8 for a,b in zip(result,balances))
    return result

def simulate(segments, payment, excess_rule='proportional', minimum_rule='interest_plus_10',
             minimum_allocation='interest_then_lowest', max_months=1200):
    if not segments or len({s.name for s in segments}) != len(segments):
        raise ValueError('At least one uniquely named balance is required')
    for s in segments:
        if not isfinite(s.balance) or s.balance < 0 or not isfinite(s.apr) or not 0 <= s.apr <= 1:
            raise ValueError('Balance must be nonnegative and APR a fraction from 0 to 1')
        if s.promo_months < 0 or (s.post_promo_apr is not None and not 0 <= s.post_promo_apr <= 1):
            raise ValueError('Invalid promotional rate')
    if not isfinite(payment) or payment < 0:
        raise ValueError('Payment must be nonnegative')
    if not isinstance(max_months,int) or max_months<1:
        raise ValueError('Maximum periods must be a positive integer')
    if minimum_rule not in ('interest_plus_10','five_percent'):
        raise ValueError('Unknown minimum rule')
    if minimum_allocation not in ('interest_then_lowest','highest'):
        raise ValueError('Unknown minimum allocation')
    if excess_rule not in ('highest','proportional'):
        raise ValueError('Unknown excess rule')
    principal=[float(s.balance) for s in segments]
    interest=[0.0]*len(segments)
    rows=[dict(month=0,balance=sum(principal),interest=0.,cumulative_interest=0.,payment=0.,minimum=0.)]
    total_interest=0.
    for month in range(1,max_months+1):
        if sum(principal)+sum(interest) < 1e-7:
            return dict(status='paid_off',months=month-1,total_interest=total_interest,rows=rows)
        rates=[s.post_promo_apr if s.post_promo_apr is not None and month>s.promo_months else s.apr for s in segments]
        charged=[p*r/12 for p,r in zip(principal,rates)]
        interest=[i+c for i,c in zip(interest,charged)]
        total_interest+=sum(charged)
        debt=sum(principal)+sum(interest)
        required=min(debt,sum(interest)+10) if minimum_rule=='interest_plus_10' else min(debt,max(10,.05*debt))
        if payment+1e-7 < required:
            return dict(status='below_minimum',months=None,total_interest=total_interest,required_payment=required,failed_month=month,rows=rows)
        paid=min(payment,debt)
        before=debt
        def pay_groups(amount,method):
            group=[p+i for p,i in zip(principal,interest)]
            amounts=allocate(group,amount,rates,method)
            for k,a in enumerate(amounts):
                interest_paid=min(interest[k],a)
                interest[k]-=interest_paid
                principal[k]=max(0,principal[k]-(a-interest_paid))
            return amounts
        if minimum_allocation=='highest':
            pay_groups(required,'highest')
        else:
            interest_pay=allocate(interest,required,rates,'lowest')
            for k,a in enumerate(interest_pay): interest[k]-=a
            amount=required-sum(interest_pay)
            principal_pay=allocate(principal,amount,rates,'lowest')
            for k,a in enumerate(principal_pay): principal[k]-=a
        excess=paid-required
        allocations=pay_groups(excess,excess_rule)
        debt=sum(principal)+sum(interest)
        assert abs(before-paid-debt)<1e-6*max(1,before)
        row=dict(month=month,balance=max(0,debt),interest=sum(charged),cumulative_interest=total_interest,payment=paid,minimum=required)
        for k,s in enumerate(segments):
            row[s.name+'_balance']=principal[k]+interest[k]
            row[s.name+'_excess_allocation']=allocations[k]
        rows.append(row)
        if debt < 1e-7:
            return dict(status='paid_off',months=month,total_interest=total_interest,rows=rows)
    return dict(status='horizon_reached',months=None,total_interest=total_interest,rows=rows)
