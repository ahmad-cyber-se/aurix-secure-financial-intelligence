"use client";

import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import { ErrorState, LoadingState } from "../../components/PageState";
import { api, formatMoney, Insight, Portfolio, Transaction, User } from "../../lib/api";

export default function DashboardPage() {
  const [data, setData] = useState<{user: User; portfolio: Portfolio; transactions: Transaction[]; insight: Insight} | null>(null);
  const [error, setError] = useState("");
  useEffect(() => { Promise.all([api<User>("/users/me"), api<Portfolio>("/portfolio"), api<Transaction[]>("/transactions?limit=5"), api<Insight>("/portfolio/insights")])
    .then(([user, portfolio, transactions, insight]) => setData({user, portfolio, transactions, insight})).catch(e => setError(e.message)); }, []);

  return <AppShell><div className="page"><header className="pageHeader"><div><p className="eyebrow">Financial overview</p><h1>{data ? `Welcome, ${data.user.name}` : "Dashboard"}</h1></div><div className="simulation">SIMULATION MODE</div></header>
    {error ? <ErrorState message={error}/> : !data ? <LoadingState/> : <>
      <section className="heroMetric"><span>Portfolio Value</span><strong>{formatMoney(data.portfolio.total_value)}</strong><small>As of current simulated balances</small></section>
      <section className="metricGrid">
        {[["Gold", data.portfolio.gold, data.portfolio.allocations.GOLD], ["Silver", data.portfolio.silver, data.portfolio.allocations.SILVER], ["ETFs", data.portfolio.etfs, data.portfolio.allocations.ETF], ["Cash", data.portfolio.cash, data.portfolio.allocations.CASH]].map(([name,value,pct]) => <article className="metricCard" key={name as string}><span>{name}</span><strong>{formatMoney(value as string)}</strong><div className="allocationLine"><i style={{width: `${pct}%`}}/><span>{Number(pct).toFixed(0)}%</span></div></article>)}
      </section>
      <section className="twoColumn"><article className="panel"><div className="panelTitle"><h2>Recent transactions</h2><span>Latest 5</span></div>{data.transactions.length === 0 ? <p className="muted">No transactions yet.</p> : <div className="compactList">{data.transactions.map(tx => <div key={tx.id}><div><strong>{tx.asset}</strong><small>{tx.type} · {new Date(tx.created_at).toLocaleString()}</small></div><div className="right"><strong>{formatMoney(tx.amount, tx.currency)}</strong><span className={`risk ${tx.risk_level.toLowerCase()}`}>{tx.risk_level}</span></div></div>)}</div>}</article>
      <article className="panel insightPanel"><div className="panelTitle"><h2>AI Financial Insight</h2><span>{data.insight.engine}</span></div><div className="riskHeadline">Portfolio Risk: <strong>{data.insight.portfolio_risk}</strong></div><p>{data.insight.observation}</p><p className="recommendation">{data.insight.recommendation}</p><small className="muted">This prototype uses deterministic rules and does not call a real AI model.</small></article></section>
    </>}
  </div></AppShell>;
}
