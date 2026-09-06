"use client";

import { useSearchParams } from "next/navigation";
import {
  FormEvent,
  Suspense,
  useEffect,
  useMemo,
  useState,
} from "react";
import AppShell from "../../components/AppShell";
import { ErrorState, LoadingState } from "../../components/PageState";
import {
  api,
  ETF,
  formatMoney,
  Portfolio,
  Transaction,
} from "../../lib/api";

function InvestmentContent() {
  const params = useSearchParams();
  const requested = params.get("etf");

  const [etfs, setEtfs] = useState<ETF[] | null>(null);
  const [portfolio, setPortfolio] = useState<Portfolio | null>(null);
  const [selected, setSelected] = useState(requested ?? "");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastTx, setLastTx] = useState<Transaction | null>(null);

  const selectedEtf = useMemo(
    () => etfs?.find((e) => e.id === selected),
    [etfs, selected]
  );

  useEffect(() => {
    Promise.all([
      api<ETF[]>("/etfs"),
      api<Portfolio>("/portfolio"),
    ])
      .then(([e, p]) => {
        setEtfs(e);
        setPortfolio(p);

        if (!selected && e[0]) {
          setSelected(e[0].id);
        }
      })
      .catch((e) => setError(e.message));
  }, []);

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();

    setError("");
    setMessage("");
    setLoading(true);

    const fd = new FormData(e.currentTarget);

    try {
      const r = await api<{
        transaction: Transaction;
        portfolio: Portfolio;
      }>("/investments", {
        method: "POST",
        body: JSON.stringify({
          etf_id: selected,
          amount: fd.get("amount"),
        }),
      });

      setPortfolio(r.portfolio);
      setLastTx(r.transaction);
      setMessage(
        "Investment completed and portfolio updated atomically."
      );
    } catch (e) {
      setError(
        e instanceof Error ? e.message : "Investment failed"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="page">
        <header className="pageHeader">
          <div>
            <p className="eyebrow">Simulated execution</p>
            <h1>ETF Investment</h1>
            <p className="muted">
              Eligibility → balance → fraud score → transaction →
              portfolio → audit record.
            </p>
          </div>
        </header>

        {error && <ErrorState message={error} />}

        {!etfs || !portfolio ? (
          <LoadingState />
        ) : (
          <section className="twoColumn investLayout">
            <form onSubmit={submit} className="panel formStack">
              <label>
                Eligible ETF
                <select
                  value={selected}
                  onChange={(e) => setSelected(e.target.value)}
                >
                  {etfs.map((e) => (
                    <option value={e.id} key={e.id}>
                      {e.ticker} — {e.name}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Investment amount (EUR)
                <input
                  required
                  name="amount"
                  type="number"
                  min="1"
                  max={portfolio.cash}
                  step="0.01"
                  placeholder="200.00"
                />
              </label>

              <div className="balanceBox">
                <span>Available cash</span>
                <strong>{formatMoney(portfolio.cash)}</strong>
              </div>

              <button
                disabled={loading || !selected}
                className="primaryButton"
              >
                {loading
                  ? "Validating & investing…"
                  : "Confirm simulated investment"}
              </button>

              {message && (
                <div className="successBanner">{message}</div>
              )}
            </form>

            <article className="panel">
              <h2>Execution controls</h2>

              <div className="controlList">
                <div>
                  <strong>1</strong>
                  <span>Country/subscription eligibility</span>
                </div>
                <div>
                  <strong>2</strong>
                  <span>Available cash validation</span>
                </div>
                <div>
                  <strong>3</strong>
                  <span>Fraud/anomaly scoring</span>
                </div>
                <div>
                  <strong>4</strong>
                  <span>Atomic database transaction</span>
                </div>
                <div>
                  <strong>5</strong>
                  <span>Audit trail creation</span>
                </div>
              </div>

              {selectedEtf && (
                <p className="muted">
                  Selected: {selectedEtf.ticker} ·{" "}
                  {selectedEtf.region}
                </p>
              )}

              {lastTx && (
                <div className="riskResult">
                  <span>Latest risk result</span>
                  <strong
                    className={`risk ${lastTx.risk_level.toLowerCase()}`}
                  >
                    {lastTx.risk_level}
                  </strong>
                  <small>{lastTx.risk_reason}</small>
                </div>
              )}
            </article>
          </section>
        )}
      </div>
    </AppShell>
  );
}

export default function InvestmentPage() {
  return (
    <Suspense fallback={<LoadingState />}>
      <InvestmentContent />
    </Suspense>
  );
}