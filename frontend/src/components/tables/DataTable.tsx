/**
 * Generic Data Table
 *
 * Reusable data table component with sorting, filtering, and pagination.
 *
 * Phase 0: Stub component only.
 *
 * TODO (Phase 8): Implement with @tanstack/react-table or Shadcn DataTable.
 */

interface DataTableProps<T> {
  data: T[];
  columns: { key: string; label: string }[];
}

export function DataTable<T extends Record<string, unknown>>({
  data,
  columns,
}: DataTableProps<T>) {
  return (
    <div id="data-table" className="table-container">
      {/* TODO: Table header with sort controls */}
      {/* TODO: Table body with data rows */}
      {/* TODO: Pagination controls */}
      <p>Table: {columns.length} columns, {data.length} rows</p>
    </div>
  );
}
