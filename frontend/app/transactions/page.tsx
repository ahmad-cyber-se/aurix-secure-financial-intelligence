"use client";

import { useEffect, useState } from "react";
import AppShell from "../../components/AppShell";
import { ErrorState, LoadingState } from "../../components/PageState";
import { api, formatMoney, Transaction } from "../../lib/api";

export default function TransactionsPage(){const [rows,setRows]=useState<Transaction[]|null>(null);const [error,setError]=useState("");useEffect(()=>{api<Transaction[]>("/transactions?limit=100").then(setRows).catch(e=>setError(e.message))},[]);return <AppShell><div className="page"><header className="pageHeader"><div><p className="eyebrow">Financial traceability</p><h1>Transaction History</h1></div></header>{error?<ErrorState message={error}/>:!rows?<LoadingState/>:<section className="panel"><div className="tableWrap"><table><thead><tr><th>Transaction ID</th><th>Asset</th><th>Type</th><th>Amount</th><th>Status</th><th>Risk</th><th>Timestamp</th></tr></thead><tbody>{rows.length===0?<tr><td colSpan={7} className="emptyCell">No transactions yet.</td></tr>:rows.map(tx=><tr key={tx.id}><td className="mono">{tx.id.slice(0,8)}…</td><td>{tx.asset}</td><td>{tx.type}</td><td>{formatMoney(tx.amount,tx.currency)}</td><td>{tx.status}</td><td><span className={`risk ${tx.risk_level.toLowerCase()}`}>{tx.risk_level}</span></td><td>{new Date(tx.created_at).toLocaleString()}</td></tr>)}</tbody></table></div></section>}</div></AppShell>}
