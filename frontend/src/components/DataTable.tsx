import { ReactNode } from "react";

interface Column<T> {
  key: keyof T;
  header: string;
  render?: (value: any, row: T) => ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
}

export function DataTable<T extends { id: number | string }>({
  data,
  columns,
}: DataTableProps<T>) {
  return (
    <table
      style={{
        width: "100%",
        borderCollapse: "collapse",
        fontSize: "0.875rem",
      }}
    >
      <thead>
        <tr>
          {columns.map((col) => (
            <th
              key={String(col.key)}
              style={{
                textAlign: "left",
                padding: "0.75rem 1rem",
                borderBottom: "2px solid #e2e8f0",
                backgroundColor: "#f8fafc",
                fontWeight: 600,
              }}
            >
              {col.header}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row) => (
          <tr key={row.id}>
            {columns.map((col) => (
              <td
                key={String(col.key)}
                style={{
                  padding: "0.5rem 1rem",
                  borderBottom: "1px solid #e2e8f0",
                }}
              >
                {col.render
                  ? col.render(row[col.key], row)
                  : String(row[col.key] ?? "")}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}
