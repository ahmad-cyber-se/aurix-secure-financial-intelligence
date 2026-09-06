"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ReactNode, useEffect, useState } from "react";
import { api, User } from "../lib/api";
import { clearToken, getToken } from "../lib/auth";

const nav = [
  ["/dashboard", "Dashboard"],
  ["/etfs", "ETF Catalogue"],
  ["/investment", "Investment"],
  ["/portfolio", "Portfolio"],
  ["/transactions", "Transactions"],
  ["/profile", "Profile"],
  ["/security", "Security / Activity"],
];

export default function AppShell({children}: {children: ReactNode}) {
  const pathname = usePathname();
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (!getToken()) {
      router.replace("/login");
      return;
    }
    api<User>("/users/me").then(setUser).catch(() => router.replace("/login"));
  }, [router]);

  async function logout() {
    try { await api("/auth/logout", {method: "POST"}); } catch {}
    clearToken();
    router.replace("/login");
  }

  return (
    <div className="appFrame">
      <aside className="sidebar">
        <div>
          <Link href="/dashboard" className="brand">AURIX</Link>
          <div className="brandSub">Secure Financial Intelligence</div>
        </div>
        <nav>
          {nav.map(([href, label]) => (
            <Link key={href} href={href} className={pathname === href || pathname.startsWith(`${href}/`) ? "navLink active" : "navLink"}>
              {label}
            </Link>
          ))}
        </nav>
        <div className="sideFooter">
          <div className="simulation">SIMULATION MODE</div>
          <div className="sideUser">{user?.name ?? "Loading…"}<small>{user?.subscription_plan} · {user?.country}</small></div>
          <button className="ghostButton" onClick={logout}>Logout</button>
        </div>
      </aside>
      <main className="mainContent">{children}</main>
    </div>
  );
}
