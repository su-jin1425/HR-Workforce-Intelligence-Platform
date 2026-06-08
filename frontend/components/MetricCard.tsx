interface MetricCardProps {
  label: string;
  value: string;
  tone?: "neutral" | "risk" | "healthy";
}

export function MetricCard({ label, value, tone = "neutral" }: MetricCardProps) {
  const toneClass =
    tone === "risk" ? "border-coral text-coral" : tone === "healthy" ? "border-teal text-teal" : "border-line";

  return (
    <section className={`rounded-md border bg-white p-4 shadow-sm ${toneClass}`}>
      <p className="text-sm text-neutral-600">{label}</p>
      <p className="mt-2 text-3xl font-semibold tracking-normal">{value}</p>
    </section>
  );
}
