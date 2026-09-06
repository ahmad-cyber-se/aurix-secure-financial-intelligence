"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { api } from "../../lib/api";
import { setToken } from "../../lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault(); setError(""); setLoading(true);
    const data = new FormData(e.currentTarget);
    try {
      const result = await api<{access_token: string}>("/auth/login", {method: "POST", body: JSON.stringify({email: data.get("email"), password: data.get("password")})}, false);
      setToken(result.access_token);
      router.push("/dashboard");
    } catch (err) { setError(err instanceof Error ? err.message : "Login failed"); }
    finally { setLoading(false); }
  }

  return <div className="authPage"><section className="authPanel">
    <div className="authBrand">AURIX</div><p className="eyebrow">Measured Trust · Real Value · Digital Freedom</p>
    <h1>Secure financial intelligence</h1><p className="muted">Sign in to the 24-hour evaluation prototype.</p>
    {error && <div className="errorBanner">{error}</div>}
    <form onSubmit={submit} className="formStack">
      <label>Email<input required name="email" type="email" placeholder="shahan@example.com" /></label>
      <label>Password<input required name="password" type="password" minLength={8} /></label>
      <button className="primaryButton" disabled={loading}>{loading ? "Signing in…" : "Sign in"}</button>
    </form>
    <p className="authSwitch">No account? <Link href="/register">Create one</Link></p>
    <div className="simulation authSimulation">SIMULATION MODE · No real funds are processed.</div>
  </section></div>;
}
