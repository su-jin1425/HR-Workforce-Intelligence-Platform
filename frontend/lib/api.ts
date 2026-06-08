import type { WorkforceOverview } from "@/types/workforce";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getWorkforceOverview(): Promise<WorkforceOverview> {
  const response = await fetch(`${API_URL}/api/v1/analytics/overview?seed_demo_data=true`, {
    cache: "no-store"
  });
  if (!response.ok) {
    throw new Error(`Failed to load workforce overview: ${response.status}`);
  }
  return response.json();
}
