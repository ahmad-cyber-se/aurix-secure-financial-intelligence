export function LoadingState({label = "Loading secure data…"}: {label?: string}) {
  return <div className="stateCard">{label}</div>;
}

export function ErrorState({message}: {message: string}) {
  return <div className="errorBanner">{message}</div>;
}
