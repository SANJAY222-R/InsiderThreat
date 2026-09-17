import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";
import { reportService, type DashboardSummary } from "../services/reportService";
import { alertService } from "../services/alertService";
import { predictionService } from "../services/predictionService";
import { useWebSocket } from "../hooks/useWebSocket";
import type { Alert } from "../types/alert";
import type { Prediction } from "../types/prediction";

const Dashboard: React.FC = () => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [predictions, setPredictions] = useState<Prediction[]>([]);

  // Connect to live WebSocket
  const { isConnected } = useWebSocket(undefined, {
    onMessage: (msg) => {
      if (typeof msg === "object" && msg !== null) {
        const payload = msg as Record<string, any>;
        if (payload.type === "threat_prediction") {
          const newPred: Prediction = {
            id: Date.now(),
            employee_id: payload.employee_id,
            risk_score: payload.risk_score,
            threat_level: payload.threat_level,
            confidence: payload.confidence,
            explanation: { top_features: payload.top_features || [] },
            model_version: "v2.4.0",
            created_at: payload.timestamp || new Date().toISOString(),
          };
          setPredictions((prev) => [newPred, ...prev.slice(0, 9)]);

          if (payload.alert) {
            const newAlert: Alert = {
              id: Date.now(),
              employee_id: payload.employee_id,
              severity: (payload.alert.severity || "medium").toLowerCase(),
              status: "open",
              title: payload.alert.title,
              description: payload.alert.description,
              created_at: payload.timestamp || new Date().toISOString(),
            };
            setAlerts((prev) => [newAlert, ...prev.slice(0, 19)]);
          }
        } else if ("title" in payload) {
          setAlerts((prev) => [payload as Alert, ...prev.slice(0, 19)]);
        }
      }
    },
  });

  const loadData = async () => {
    try {
      const [summaryData, alertsData, predictionsData] = await Promise.allSettled([
        reportService.getSummary(),
        alertService.getAlerts({ limit: 10 }),
        predictionService.getPredictions({ limit: 10 }),
      ]);

      if (summaryData.status === "fulfilled") {
        setSummary(summaryData.value);
      }
      if (alertsData.status === "fulfilled") {
        setAlerts(alertsData.value);
      }
      if (predictionsData.status === "fulfilled") {
        setPredictions(predictionsData.value);
      }
    } catch {
      // Fallback state will be displayed
    } finally {
      // Data loaded
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const chartData = predictions.length > 0
    ? predictions.slice(0, 8).reverse().map((p, idx) => ({
        time: p.created_at ? new Date(p.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : `T-${idx}`,
        risk: p.risk_score,
      }))
    : [
        { time: "10:00", risk: 20 },
        { time: "11:00", risk: 22 },
        { time: "12:00", risk: 45 },
        { time: "13:00", risk: 85 },
        { time: "14:00", risk: 60 },
      ];

  const totalPredictions = summary?.total_predictions ?? predictions.length ?? 0;
  const totalAlerts = summary?.total_alerts ?? alerts.length ?? 0;
  const criticalCount = summary?.alerts_by_severity?.["critical"] ?? alerts.filter((a) => a.severity === "critical").length ?? 0;

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Global Command Center</h1>
          <p className="text-gray-400 mt-1">Real-time threat monitoring powered by THGNN Intelligence.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            <span
              className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                isConnected ? "bg-green-400" : "bg-yellow-400"
              }`}
            />
            <span
              className={`relative inline-flex rounded-full h-3 w-3 ${
                isConnected ? "bg-green-500" : "bg-yellow-500"
              }`}
            />
          </span>
          <span className={`text-sm font-medium ${isConnected ? "text-green-400" : "text-yellow-400"}`}>
            {isConnected ? "Live Stream Connected" : "Polling Mode"}
          </span>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          {
            label: "Total Threat Predictions",
            value: totalPredictions.toString(),
            color: "text-blue-400",
            glow: "shadow-blue-500/10",
          },
          {
            label: "Active Alerts",
            value: totalAlerts.toString(),
            color: "text-orange-400",
            glow: "shadow-orange-500/20",
          },
          {
            label: "Critical Incidents",
            value: criticalCount.toString(),
            color: "text-red-500",
            glow: "shadow-red-500/20",
            alert: criticalCount > 0,
          },
          {
            label: "Model Health",
            value: "99.4%",
            color: "text-purple-400",
            glow: "shadow-purple-500/10",
          },
        ].map((kpi, idx) => (
          <div
            key={idx}
            className={`bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 shadow-xl ${kpi.glow} relative overflow-hidden group hover:border-gray-600 transition-colors`}
          >
            {kpi.alert && <div className="absolute top-0 right-0 w-16 h-16 bg-red-500/20 blur-2xl rounded-full" />}
            <p className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">{kpi.label}</p>
            <p className={`text-4xl font-extrabold ${kpi.color}`}>{kpi.value}</p>
          </div>
        ))}
      </div>

      {/* Charts Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 shadow-xl">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-gray-200 flex items-center gap-2">
              <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              </svg>
              Enterprise Risk Velocity
            </h2>
            <button
              onClick={loadData}
              className="text-xs text-gray-400 hover:text-white bg-gray-700/50 hover:bg-gray-700 px-3 py-1.5 rounded-lg transition-colors"
            >
              Refresh
            </button>
          </div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <defs>
                  <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#EF4444" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#EF4444" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                <XAxis dataKey="time" stroke="#6B7280" tick={{ fill: "#9CA3AF" }} tickLine={false} axisLine={false} />
                <YAxis stroke="#6B7280" tick={{ fill: "#9CA3AF" }} tickLine={false} axisLine={false} domain={[0, 100]} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "#111827",
                    border: "1px solid #374151",
                    borderRadius: "12px",
                    boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)",
                  }}
                  itemStyle={{ color: "#F3F4F6" }}
                />
                <Line
                  type="monotone"
                  dataKey="risk"
                  stroke="#EF4444"
                  strokeWidth={3}
                  dot={{ r: 4, fill: "#EF4444", strokeWidth: 2, stroke: "#111827" }}
                  activeDot={{ r: 6, fill: "#EF4444", stroke: "#fff" }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 shadow-xl flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-gray-200 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Live Anomalies
            </h2>
            <Link to="/alerts" className="text-xs text-blue-400 hover:text-blue-300 font-medium">
              View All
            </Link>
          </div>
          <ul className="space-y-3 flex-1 overflow-auto pr-2 max-h-80">
            {alerts.length > 0 ? (
              alerts.map((alert) => {
                const isCrit = alert.severity === "critical";
                const isHigh = alert.severity === "high";
                const isMed = alert.severity === "medium";

                return (
                  <li
                    key={alert.id}
                    className={`p-4 rounded-xl border relative overflow-hidden transition-all ${
                      isCrit
                        ? "bg-red-900/10 border-red-500/30 hover:border-red-500/50"
                        : isHigh
                        ? "bg-orange-900/10 border-orange-500/30 hover:border-orange-500/50"
                        : isMed
                        ? "bg-yellow-900/10 border-yellow-500/30 hover:border-yellow-500/50"
                        : "bg-gray-800/30 border-gray-700 hover:border-gray-600"
                    }`}
                  >
                    {isCrit && <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500 shadow-[0_0_8px_#EF4444]" />}
                    <div className="flex items-center justify-between mb-1">
                      <span
                        className={`text-xs font-bold px-2 py-0.5 rounded-md uppercase ${
                          isCrit
                            ? "bg-red-500/20 text-red-400"
                            : isHigh
                            ? "bg-orange-500/20 text-orange-400"
                            : isMed
                            ? "bg-yellow-500/20 text-yellow-400"
                            : "bg-gray-700 text-gray-300"
                        }`}
                      >
                        {alert.severity}
                      </span>
                      <span className="text-xs text-gray-400 font-mono">{alert.employee_id}</span>
                    </div>
                    <p className="text-sm text-gray-200 mt-1 font-medium">{alert.title}</p>
                    {alert.description && <p className="text-xs text-gray-400 mt-0.5 line-clamp-1">{alert.description}</p>}
                  </li>
                );
              })
            ) : (
              <div className="text-center py-12 text-gray-500 text-sm">
                No active anomalies detected
              </div>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
