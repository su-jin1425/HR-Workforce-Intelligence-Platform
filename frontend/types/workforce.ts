export type RiskBand = "low" | "medium" | "high";

export interface DepartmentKpi {
  department: string;
  employee_count: number;
  active_count: number;
  retention_rate: number;
  average_productivity: number;
  attendance_rate: number;
  engagement_score: number;
  risk_band: RiskBand;
}

export interface WorkforceOverview {
  summary_title: string;
  as_of: string;
  employee_count: number;
  active_employee_count: number;
  retention_rate: number;
  average_productivity: number;
  attendance_rate: number;
  high_risk_employee_count: number;
  departments: DepartmentKpi[];
  recommended_actions: string[];
  data_classification: string;
}
