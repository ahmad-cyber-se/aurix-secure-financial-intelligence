"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import AppShell from "../../../components/AppShell";
import { ErrorState, LoadingState } from "../../../components/PageState";
import { api, ETF } from "../../../lib/api";

export default function ETFDetailsPage() {
  const {id} = useParams<{id: string}>(); const [etf,setEtf]=useState<ETF|null>(null); const [error,setError]=useState("");
  useEffect(() => { if(id) api<ETF>(`/etfs/${id}`).then(setEtf).catch(e=>setError(e.message)); }, [id]);
  return <AppShell><div className="page"><header className="pageHeader"><div><p className="eyebrow">ETF details</p><h1>{etf?.name ?? "Investment product"}</h1></div><Link className="secondaryButton" href="/etfs">Back to catalogue</Link></header>
  {error ? <ErrorState message={error}/> : !etf ? <LoadingState/> : <><section className="detailHero"><div className="ticker large">{etf.ticker}</div><div><h2>{etf.name}</h2><p>{etf.provider}</p></div><span className={`risk ${etf.risk_level.toLowerCase()}`}>{etf.risk_level} RISK</span></section><section className="detailGrid">{[["ISIN",etf.isin],["Asset class",etf.asset_class],["Region",etf.region],["Currency",etf.currency],["Expense ratio",`${(Number(etf.expense_ratio)*100).toFixed(2)}%`],["Provider",etf.provider]].map(([k,v])=><div key={k}><span>{k}</span><strong>{v}</strong></div>)}</section><Link className="primaryButton inlineButton" href={`/investment?etf=${etf.id}`}>Invest in this ETF</Link></>}
  </div></AppShell>;
}
