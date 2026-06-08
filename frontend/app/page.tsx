import { Activity, Bot, ShieldCheck, TrendingUp } from "lucide-react";

import { DepartmentTable } from "@/components/DepartmentTable";
import { MetricCard } from "@/components/MetricCard";
import { getWorkforceOverview } from "@/lib/api";

export default async function Home() {
  const overview = await getWorkforceOverview();

  return (
    <main className="min-h-screen bg-surface">
      <header className="border-b border-line bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <div>
            <p className="text-sm font-medium text-teal">Microsoft 365 Copilot Enterprise Agent</p>
            <h1 className="text-2xl font-semibold tracking-normal">Workforce IQ</h1>
          </div>
          <div className="flex items-center gap-2 rounded-md border border-line px-3 py-2 text-sm text-neutral-700">
            <Bot size={18} />
            App package ready
          </div>
        </div>
      </header>

      <div className="mx-auto grid max-w-7xl gap-6 px-6 py-6">
        <section className="grid gap-4 md:grid-cols-4">
          <MetricCard label="Employees" value={overview.employee_count.toString()} tone="healthy" />
          <MetricCard label="Retention" value={`${overview.retention_rate}%`} tone="healthy" />
          <MetricCard label="Attendance" value={`${overview.attendance_rate}%`} />
          <MetricCard label="High-risk profiles" value={overview.high_risk_employee_count.toString()} tone="risk" />
        </section>

        <section className="grid gap-6 lg:grid-cols-[1fr_360px]">
          <div>
            <div className="mb-3 flex items-center gap-2">
              <Activity size={18} />
              <h2 className="text-lg font-semibold tracking-normal">Department workforce health</h2>
            </div>
            <DepartmentTable departments={overview.departments} />
          </div>

          <aside className="grid gap-4">
            <section className="rounded-md border border-line bg-white p-4 shadow-sm">
              <div className="mb-3 flex items-center gap-2">
                <TrendingUp size={18} />
                <h2 className="text-base font-semibold tracking-normal">Recommended actions</h2>
              </div>
              <ul className="grid gap-3 text-sm text-neutral-700">
                {overview.recommended_actions.map((action) => (
                  <li key={action} className="rounded border border-line p-3">
                    {action}
                  </li>
                ))}
              </ul>
            </section>

            <section className="rounded-md border border-line bg-white p-4 shadow-sm">
              <div className="mb-3 flex items-center gap-2">
                <ShieldCheck size={18} />
                <h2 className="text-base font-semibold tracking-normal">Governance posture</h2>
              </div>
              <p className="text-sm text-neutral-700">{overview.data_classification}</p>
            </section>
          </aside>
        </section>
      </div>
    </main>
  );
}
