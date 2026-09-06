"use client";

import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import { ErrorState, LoadingState } from "../../components/PageState";
import { api, formatMoney, Portfolio } from "../../lib/api";

type Asset = {id:string;asset_type:string;name:string;etf_id:string|null;current_value:string;allocation_percent:string};
export default function PortfolioPage(){const [p,setP]=useState<Portfolio|null>(null);const [assets,setAssets]=useState<Asset[]|null>(null);const [error,setError]=useState("");useEffect(()=>{Promise.all([api<Portfolio>("/portfolio"),api<{assets:Asset[]}>("/portfolio/assets")]).then(([p,a])=>{setP(p);setAssets(a.assets)}).catch(e=>setError(e.message))},[]);return <AppShell><div className="page"><header className="pageHeader"><div><p className="eyebrow">Allocation & value</p><h1>Portfolio</h1></div></header>{error?<ErrorState message={error}/>:!p||!assets?<LoadingState/>:<><section className="heroMetric"><span>Total portfolio value</span><strong>{formatMoney(p.total_value)}</strong></section><section className="panel"><div className="tableWrap"><table><thead><tr><th>Asset</th><th>Type</th><th>Value</th><th>Allocation</th></tr></thead><tbody>{assets.map(a=><tr key={a.id}><td><strong>{a.name}</strong></td><td>{a.asset_type}</td><td>{formatMoney(a.current_value)}</td><td><div className="miniBar"><i style={{width:`${a.allocation_percent}%`}}/></div>{Number(a.allocation_percent).toFixed(2)}%</td></tr>)}</tbody></table></div></section></>}</div></AppShell>}
