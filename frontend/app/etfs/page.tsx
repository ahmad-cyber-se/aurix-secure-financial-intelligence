"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import { ErrorState, LoadingState } from "../../components/PageState";
import { api, ETF, User } from "../../lib/api";

export default function ETFsPage() {
  const [etfs, setEtfs] = useState<ETF[] | null>(null); const [user, setUser] = useState<User | null>(null); const [error, setError] = useState("");
  useEffect(() => { Promise.all([api<ETF[]>("/etfs"), api<User>("/users/me")]).then(([e,u]) => {setEtfs(e); setUser(u)}).catch(e => setError(e.message)); }, []);
  return <AppShell><div className="page"><header className="pageHeader"><div><p className="eyebrow">Investment products</p><h1>ETF Catalogue</h1><p className="muted">Eligibility is calculated by the backend service layer.</p></div>{user && <div className="filterBadge">{user.country} · {user.subscription_plan}</div>}</header>
    {error ? <ErrorState message={error}/> : !etfs ? <LoadingState/> : <div className="cardGrid">{etfs.map(etf => <Link href={`/etfs/${etf.id}`} className="etfCard" key={etf.id}><div className="ticker">{etf.ticker}</div><h2>{etf.name}</h2><p>{etf.provider} · {etf.region}</p><div className="etfMeta"><span>TER {(Number(etf.expense_ratio)*100).toFixed(2)}%</span><span className={`risk ${etf.risk_level.toLowerCase()}`}>{etf.risk_level}</span></div></Link>)}</div>}
  </div></AppShell>;
}
