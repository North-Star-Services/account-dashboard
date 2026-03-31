import { DataTable } from "../components/DataTable";
import { useFetch } from "../hooks/useFetch";
import { Account } from "../types/account";
import { formatCurrency, formatDate } from "../utils/formatters";

const columns = [
  { key: "name" as const, header: "Account Name" },
  { key: "industry" as const, header: "Industry" },
  {
    key: "arr" as const,
    header: "ARR",
    render: (value: number) => formatCurrency(value),
  },
  {
    key: "health_score" as const,
    header: "Health Score",
    render: (value: number | null) => (value !== null ? String(value) : "—"),
  },
  {
    key: "last_contact_date" as const,
    header: "Last Contact",
    render: (value: string | null) => formatDate(value),
  },
  { key: "owner_name" as const, header: "Owner" },
];

export default function AccountsPage() {
  const { data, loading, error } = useFetch<Account[]>(
    "http://localhost:8000/accounts"
  );

  if (loading) return <p>Loading accounts...</p>;
  if (error) return <p style={{ color: "red" }}>Error: {error}</p>;
  if (!data) return null;

  return (
    <div>
      <h1 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>
        Account Health Dashboard
      </h1>
      <p style={{ color: "#64748b", marginBottom: "1.5rem" }}>
        {data.length} accounts
      </p>
      <DataTable data={data} columns={columns} />
    </div>
  );
}
