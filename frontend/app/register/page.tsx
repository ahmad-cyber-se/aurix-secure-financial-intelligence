"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { api } from "../../lib/api";
import { setToken } from "../../lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault(); setError(""); setLoading(true);
    const data = new FormData(e.currentTarget);
    try {
      const result = await api<{access_token: string}>("/auth/register", {method: "POST", body: JSON.stringify({name: data.get("name"), email: data.get("email"), password: data.get("password"), country: data.get("country"), subscription_plan: data.get("subscription_plan")})}, false);
      setToken(result.access_token);
      router.push("/dashboard");
    } catch (err) { setError(err instanceof Error ? err.message : "Registration failed"); }
    finally { setLoading(false); }
  }

  return <div className="authPage"><section className="authPanel wideAuth">
    <div className="authBrand">AURIX</div><p className="eyebrow">Create secure profile</p><h1>Registration</h1>
    {error && <div className="errorBanner">{error}</div>}
    <form onSubmit={submit} className="formGrid">
      <label>Full name<input required name="name" minLength={2} defaultValue="Shahan" /></label>
      <label>Email<input required name="email" type="email" /></label>
      <label>Password<input required name="password" type="password" minLength={8} /></label>
      <label>Country<select required name="country" defaultValue="Germany"><option>Germany</option><option>UAE</option></select></label>
      <label>Subscription<select required name="subscription_plan" defaultValue="FREE"><option value="FREE">FREE</option><option value="PREMIUM">PREMIUM</option></select></label>
      <div className="formAction"><button className="primaryButton" disabled={loading}>{loading ? "Creating…" : "Create account"}</button></div>
    </form>
    <p className="authSwitch">Already registered? <Link href="/login">Sign in</Link></p>
  </section></div>;
}
