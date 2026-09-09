import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { alertService } from "../services/alertService";
import type { Alert } from "../types/alert";

const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>("");
  const [severityFilter, setSeverityFilter] = useState<string>("");
  const [search, setSearch] = useState("");
  const [isCreating, setIsCreating] = useState(false);
  const [newAlert, setNewAlert] = useState({
    employee_id: "",
    title: "",
    severity: "medium",
    description: "",
  });

  const fetchAlerts = async () => {
    setIsLoading(true);
    try {
      const data = await alertService.getAlerts({
        status: statusFilter || undefined,
        severity: severityFilter || undefined,
        limit: 100,
      });
      setAlerts(data);
    } catch {
      // Fallback
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, [statusFilter, severityFilter]);

  const handleResolve = async (id: number) => {
    try {
      const updated = await alertService.updateAlert(id, { status: "resolved" });
      setAlerts((prev) => prev.map((a) => (a.id === id ? updated : a)));
    } catch (err) {
      alert("Failed to resolve alert: " + (err instanceof Error ? err.message : String(err)));
    }
  };

  const handleInvestigate = async (id: number) => {
    try {
      const updated = await alertService.updateAlert(id, { status: "investigating" });
      setAlerts((prev) => prev.map((a) => (a.id === id ? updated : a)));
    } catch (err) {
      alert("Failed to update alert: " + (err instanceof Error ? err.message : String(err)));
    }
  };

  const handleCreateAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const created = await alertService.createAlert(newAlert);
      setAlerts((prev) => [created, ...prev]);
      setIsCreating(false);
      setNewAlert({ employee_id: "", title: "", severity: "medium", description: "" });
    } catch (err) {
      alert("Failed to create alert: " + (err instanceof Error ? err.message : String(err)));
    }
  };

  const filteredAlerts = alerts.filter((a) => {
    if (!search) return true;
    const q = search.toLowerCase();
    return (
      a.employee_id.toLowerCase().includes(q) ||
      a.title.toLowerCase().includes(q) ||
      (a.description && a.description.toLowerCase().includes(q))
    );
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Alert Management</h1>
          <p className="text-gray-400 text-sm mt-1">Review, triage, and escalate security alerts across the organization.</p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setIsCreating(true)}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 px-4 py-2 rounded-xl text-white text-sm font-semibold shadow-lg shadow-blue-500/20 transition-all cursor-pointer"
          >
            + Create Alert
          </button>
        </div>
      </div>

      {/* Create Alert Modal */}
      {isCreating && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 max-w-lg w-full shadow-2xl">
            <h2 className="text-xl font-bold text-white mb-4">Create New Security Alert</h2>
            <form onSubmit={handleCreateAlert} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Employee ID</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. EMP-1042"
                  value={newAlert.employee_id}
                  onChange={(e) => setNewAlert({ ...newAlert, employee_id: e.target.value })}
                  className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Title</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Abnormal After-Hours File Exfiltration"
                  value={newAlert.title}
                  onChange={(e) => setNewAlert({ ...newAlert, title: e.target.value })}
                  className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Severity</label>
                <select
                  value={newAlert.severity}
                  onChange={(e) => setNewAlert({ ...newAlert, severity: e.target.value })}
                  className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Description</label>
                <textarea
                  rows={3}
                  placeholder="Provide context or event details..."
                  value={newAlert.description}
                  onChange={(e) => setNewAlert({ ...newAlert, description: e.target.value })}
                  className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-white text-sm focus:outline-none focus:border-blue-500"
                />
              </div>
              <div className="flex justify-end gap-3 pt-2">
                <button
                  type="button"
                  onClick={() => setIsCreating(false)}
                  className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm font-medium rounded-xl transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white text-sm font-semibold rounded-xl transition shadow-lg shadow-blue-500/20"
                >
                  Save Alert
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Filters & Search */}
      <div className="flex flex-wrap gap-3 items-center bg-gray-900/60 p-4 rounded-2xl border border-gray-800/80">
        <input
          type="text"
          placeholder="Filter by employee or keyword..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="bg-gray-950 border border-gray-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500 flex-1 min-w-[200px]"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-blue-500"
        >
          <option value="">All Statuses</option>
          <option value="open">Open</option>
          <option value="investigating">Investigating</option>
          <option value="resolved">Resolved</option>
          <option value="false_positive">False Positive</option>
        </select>
        <select
          value={severityFilter}
          onChange={(e) => setSeverityFilter(e.target.value)}
          className="bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-sm text-gray-300 focus:outline-none focus:border-blue-500"
        >
          <option value="">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>
      </div>

      {/* Alerts Table */}
      <div className="bg-gray-900/50 backdrop-blur-md rounded-2xl border border-gray-800/80 overflow-hidden shadow-xl">
        <table className="min-w-full divide-y divide-gray-800">
          <thead className="bg-gray-950/70">
            <tr>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">ID</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Severity</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Target Employee</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Title</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3.5 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Created</th>
              <th className="px-6 py-3.5 text-right text-xs font-semibold text-gray-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/60">
            {isLoading ? (
              <tr>
                <td colSpan={7} className="px-6 py-12 text-center text-gray-500">
                  Loading alerts...
                </td>
              </tr>
            ) : filteredAlerts.length > 0 ? (
              filteredAlerts.map((alert) => {
                const isCrit = alert.severity === "critical";
                const isHigh = alert.severity === "high";
                const isMed = alert.severity === "medium";

                return (
                  <tr key={alert.id} className="hover:bg-gray-800/30 transition-colors">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400 font-mono">#{alert.id}</td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span
                        className={`px-2.5 py-1 text-xs font-bold rounded-lg uppercase tracking-wide ${
                          isCrit
                            ? "bg-red-500/20 text-red-400 border border-red-500/30"
                            : isHigh
                            ? "bg-orange-500/20 text-orange-400 border border-orange-500/30"
                            : isMed
                            ? "bg-yellow-500/20 text-yellow-400 border border-yellow-500/30"
                            : "bg-gray-800 text-gray-300 border border-gray-700"
                        }`}
                      >
                        {alert.severity}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-blue-400 font-mono">
                      {alert.employee_id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-200">
                      <div className="font-medium">{alert.title}</div>
                      {alert.description && <div className="text-xs text-gray-400 mt-0.5">{alert.description}</div>}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm">
                      <span
                        className={`text-xs px-2.5 py-1 rounded-md font-medium uppercase ${
                          alert.status === "resolved"
                            ? "bg-green-500/10 text-green-400 border border-green-500/20"
                            : alert.status === "investigating"
                            ? "bg-blue-500/10 text-blue-400 border border-blue-500/20"
                            : "bg-gray-800 text-gray-300 border border-gray-700"
                        }`}
                      >
                        {alert.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-xs text-gray-400">
                      {alert.created_at ? new Date(alert.created_at).toLocaleString() : "Recently"}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-right space-x-2">
                      <Link
                        to={`/investigations?user=${alert.employee_id}`}
                        className="text-blue-400 hover:text-blue-300 text-xs font-semibold px-2 py-1 rounded hover:bg-blue-500/10 transition"
                      >
                        Investigate
                      </Link>
                      {alert.status !== "resolved" && (
                        <button
                          onClick={() => handleResolve(alert.id)}
                          className="text-green-400 hover:text-green-300 text-xs font-semibold px-2 py-1 rounded hover:bg-green-500/10 transition"
                        >
                          Resolve
                        </button>
                      )}
                      {alert.status === "open" && (
                        <button
                          onClick={() => handleInvestigate(alert.id)}
                          className="text-yellow-400 hover:text-yellow-300 text-xs font-semibold px-2 py-1 rounded hover:bg-yellow-500/10 transition"
                        >
                          Triage
                        </button>
                      )}
                    </td>
                  </tr>
                );
              })
            ) : (
              <tr>
                <td colSpan={7} className="px-6 py-12 text-center text-gray-500">
                  No alerts matching filters
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Alerts;
