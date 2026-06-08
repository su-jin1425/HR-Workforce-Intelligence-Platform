import type { DepartmentKpi } from "@/types/workforce";

const riskClass = {
  low: "bg-emerald-50 text-emerald-800",
  medium: "bg-amber-50 text-amber-800",
  high: "bg-rose-50 text-rose-800"
};

export function DepartmentTable({ departments }: { departments: DepartmentKpi[] }) {
  return (
    <div className="overflow-hidden rounded-md border border-line bg-white shadow-sm">
      <table className="w-full border-collapse text-left text-sm">
        <thead className="bg-surface text-neutral-600">
          <tr>
            <th className="px-4 py-3 font-medium">Department</th>
            <th className="px-4 py-3 font-medium">Employees</th>
            <th className="px-4 py-3 font-medium">Retention</th>
            <th className="px-4 py-3 font-medium">Attendance</th>
            <th className="px-4 py-3 font-medium">Engagement</th>
            <th className="px-4 py-3 font-medium">Risk</th>
          </tr>
        </thead>
        <tbody>
          {departments.map((department) => (
            <tr key={department.department} className="border-t border-line">
              <td className="px-4 py-3 font-medium">{department.department}</td>
              <td className="px-4 py-3">{department.employee_count}</td>
              <td className="px-4 py-3">{department.retention_rate}%</td>
              <td className="px-4 py-3">{department.attendance_rate}%</td>
              <td className="px-4 py-3">{department.engagement_score}</td>
              <td className="px-4 py-3">
                <span className={`rounded px-2 py-1 text-xs font-semibold ${riskClass[department.risk_band]}`}>
                  {department.risk_band}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
