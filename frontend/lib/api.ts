import { clearToken, getToken } from "./auth";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type User = {
  id: string;
  name: string;
  email: string;
  country: string;
  subscription_plan: "FREE" | "PREMIUM";
  kyc_status: "PENDING" | "VERIFIED" | "REJECTED";
  created_at: string;
};

export type ETF = {
  id: string;
  name: string;
  ticker: string;
  isin: string;
  provider: string;
  asset_class: string;
  region: string;
  currency: string;
  expense_ratio: string;
  risk_level: string;
};

export type Portfolio = {
  id: string;
  base_currency: string;
  total_value: string;
  gold: string;
  silver: string;
  etfs: string;
  cash: string;
  other_assets: string;
  allocations: Record<string, string>;
};

export type Transaction = {
  id: string;
  user_id: string;
  asset: string;
  type: string;
  amount: string;
  currency: string;
  status: string;
  risk_level: "LOW" | "MEDIUM" | "HIGH";
  risk_reason: string;
  created_at: string;
};

export type Insight = {
  portfolio_risk: string;
  observation: string;
  recommendation: string;
  engine: string;
};

export type AuditLog = {
  id: string;
  action: string;
  entity: string;
  entity_id: string | null;
  timestamp: string;
  ip_address: string;
  result: "SUCCESS" | "FAILURE" | "DENIED";
  details: Record<string, unknown> | null;
};

export async function api<T>(path: string, options: RequestInit = {}, authenticated = true): Promise<T> {
  const headers = new Headers(options.headers);
  if (!headers.has("Content-Type") && options.body) headers.set("Content-Type", "application/json");
  if (authenticated) {
    const token = getToken();
    if (!token) throw new Error("Authentication required");
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_URL}${path}`, {...options, headers, cache: "no-store"});
  if (!response.ok) {
    if (response.status === 401 && authenticated) clearToken();
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail ?? `Request failed (${response.status})`);
  }
  return response.json() as Promise<T>;
}

export const formatMoney = (value: string | number, currency = "EUR") =>
  new Intl.NumberFormat("en-DE", {style: "currency", currency}).format(Number(value));
