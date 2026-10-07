import cleanfeed as c, pandas as pd, json
def top(t,k=4): return [(a, round(r.share,3)) for a,r in t.head(k).iterrows()]
out={}
q=c.build()
naive=q.p_core&q.p_notimp
V={"golden":q.clean,
   "values present, not imputed (tie-break)":naive,
   "own totals and balance only":q.present&q.a_ng_sources&q.a_ti_ties&q.a_d_subs&q.a_balance,
   "own totals, no balance":q.present&q.a_ng_sources&q.a_ti_ties&q.a_d_subs,
   "golden, no balance check":q.present&q.a_ng_sources&q.a_ti_ties&q.a_d_subs&q.a_tie_counterpart,
   "golden, Sum(Valid DIBAs) for TI":q.present&q.a_ng_sources&q.a_ti_sumvalid&q.a_d_subs&q.a_tie_counterpart&q.a_balance}
for k,m in V.items(): t=c.table(q,m); out[k]=dict(n_at_100=int((t.share>=99.99999).sum()),top=top(t))
for lab,kw in [("counterpart within 100 MW",dict(tol_cp=100)),("counterpart within 5 MW",dict(tol_cp=5)),("all checks within 5 MW",dict(tol=5)),
               ("all checks within 1 MW",dict(tol=1)),("one-sided ties fail",dict(onesided_fails=True))]:
    qq=c.build(**kw); t=c.table(qq); out[lab]=dict(n_at_100=int((t.share>=99.99999).sum()),top=top(t))
for k,v in out.items(): print(f"{k:42s} n@100={v['n_at_100']:2d} {v['top']}")
json.dump(out,open("variants.json","w"),indent=1)
