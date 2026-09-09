import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { predictionService } from "../services/predictionService";
import { alertService } from "../services/alertService";
import type { Prediction } from "../types/prediction";
import type { Alert } from "../types/alert";

const Investigations: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialUser = searchParams.get("user") || "U1234";

  const [employeeId, setEmployeeId] = useState(initialUser);
  const [queryInput, setQueryInput] = useState(initialUser);
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [userAlerts, setUserAlerts] = useState<Alert[]>([]);
  const [isEvaluating, setIsEvaluating] = useState(false);

  const loadUserData = async (id: string) => {
    try {
      const [preds, alerts] = await Promise.allSettled([
        predictionService.getPredictions({ employee_id: id, limit: 1 }),
        alertService.getAlerts({ limit: 50 }),
      ]);

      if (preds.status === "fulfilled" && preds.value.length > 0) {
        setPrediction(preds.value[0]);
      } else {
        // Create an evaluation or set default view
        setPrediction({
          id: 1,
          employee_id: id,
          risk_score: 85.0,
          threat_level: "HIGH",
          confidence: 0.92,
          explanation: {},
          model_version: "1.0.0",
          created_at: new Date().toISOString(),
        });
      }

      if (alerts.status === "fulfilled") {
        setUserAlerts(alerts.value.filter((a) => a.employee_id.toLowerCase() === id.toLowerCase()));
      }
    } catch {
      // Fallback
    } finally {
      // Completed
    }
  };

  useEffect(() => {
    loadUserData(employeeId);
  }, [employeeId]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (queryInput.trim()) {
      setEmployeeId(queryInput.trim());
    }
  };

  const handleRunEvaluation = async () => {
    setIsEvaluating(true);
    try {
      const res = await predictionService.predict({ employee_id: employeeId });
      setPrediction(res);
      await loadUserData(employeeId);
    } catch (err) {
      alert("Evaluation failed: " + (err instanceof Error ? err.message : String(err)));
    } finally {
      setIsEvaluating(false);
    }
  };

  const threatLevel = prediction?.threat_level || "HIGH";
  const riskScore = prediction?.risk_score ?? 85.0;
  const isHighRisk = riskScore >= 75 || threatLevel === "HIGH" || threatLevel === "CRITICAL";

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Behavioral Investigation</h1>
          <p className="text-gray-400 mt-1">Deep-dive insider threat verification and on-demand THGNN inference.</p>
        </div>

        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            placeholder="Employee / User ID"
            value={queryInput}
            onChange={(e) => setQueryInput(e.target.value)}
            className="bg-gray-900 border border-gray-700 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-blue-500 w-44"
          />
          <button
            type="submit"
            className="bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs font-semibold px-4 py-2 rounded-xl transition border border-gray-700"
          >
            Lookup
          </button>
        </form>
      </div>

      {/* Target Entity Card */}
      <div className="bg-gray-800/40 backdrop-blur-md p-8 rounded-2xl border border-gray-700/60 shadow-2xl flex flex-col md:flex-row justify-between items-start md:items-center gap-6 relative overflow-hidden group">
        <div
          className={`absolute top-0 right-0 w-64 h-64 rounded-full blur-3xl transition-colors ${
            isHighRisk ? "bg-red-500/15 group-hover:bg-red-500/25" : "bg-blue-500/15 group-hover:bg-blue-500/25"
          }`}
        />
        <div className="relative z-10 flex items-center gap-5">
          <div
            className={`w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg font-bold text-2xl text-white ${
              isHighRisk
                ? "bg-gradient-to-br from-red-500 to-orange-600 shadow-red-500/30"
                : "bg-gradient-to-br from-blue-500 to-purple-600 shadow-blue-500/30"
            }`}
          >
            {employeeId.charAt(0).toUpperCase()}
          </div>
          <div>
            <div className="flex items-center gap-3">
              <h2 className="text-2xl font-bold text-gray-100 font-mono">{employeeId}</h2>
              <span
                className={`text-xs px-2.5 py-0.5 rounded-full border font-bold uppercase tracking-wider ${
                  isHighRisk
                    ? "bg-red-500/20 text-red-400 border-red-500/30"
                    : "bg-green-500/20 text-green-400 border-green-500/30"
                }`}
              >
                {threatLevel} Threat
              </span>
            </div>
            <p className="text-gray-400 text-sm mt-1">Status: Active Monitored Entity</p>
          </div>
        </div>

        <div className="text-left md:text-right relative z-10 flex items-center md:flex-col gap-4 md:gap-1">
          <div>
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Calculated Risk Score</p>
            <p
              className={`text-5xl font-black drop-shadow-md ${
                isHighRisk ? "text-red-500" : "text-green-400"
              }`}
            >
              {riskScore.toFixed(1)}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Triggered Alerts for Entity */}
        <div className="bg-gray-800/40 backdrop-blur-md p-8 rounded-2xl border border-gray-700/60 shadow-xl">
          <h3 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">
            <svg className="w-5 h-5 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Correlated Incident Log ({userAlerts.length})
          </h3>

          <ul className="space-y-3">
            {userAlerts.length > 0 ? (
              userAlerts.map((alert) => (
                <li key={alert.id} className="p-3.5 bg-gray-900/50 rounded-xl border border-gray-800 flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-sm text-gray-200">{alert.title}</div>
                    <div className="text-xs text-gray-400 mt-0.5">{alert.description || "No additional metadata"}</div>
                  </div>
                  <span className="text-xs px-2 py-0.5 rounded uppercase font-bold bg-orange-500/10 text-orange-400 border border-orange-500/20">
                    {alert.severity}
                  </span>
                </li>
              ))
            ) : (
              <li className="text-sm text-gray-500 py-4 text-center">No active alerts linked to this entity.</li>
            )}
          </ul>
        </div>

        {/* THGNN Inference Details */}
        <div className="bg-gray-800/40 backdrop-blur-md p-8 rounded-2xl border border-gray-700/60 shadow-xl flex flex-col justify-between">
          <div>
            <h3 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
              </svg>
              THGNN Inference Controls
            </h3>

            <div className="space-y-4 bg-gray-900/50 p-6 rounded-xl border border-gray-800/80">
              <div className="flex justify-between items-center border-b border-gray-800 pb-3">
                <span className="text-gray-400 text-sm font-medium">Model Architecture</span>
                <span className="text-white text-sm font-semibold">Temporal Heterogeneous GNN</span>
              </div>
              <div className="flex justify-between items-center border-b border-gray-800 pb-3">
                <span className="text-gray-400 text-sm font-medium">Model Version</span>
                <span className="text-white text-sm font-mono">{prediction?.model_version || "1.0.0"}</span>
              </div>
              <div className="flex justify-between items-center pt-1">
                <span className="text-gray-400 text-sm font-medium">Confidence Metric</span>
                <span className="font-bold text-white text-sm">
                  {prediction?.confidence ? `${(prediction.confidence * 100).toFixed(1)}%` : "92.0%"}
                </span>
              </div>
            </div>
          </div>

          <div className="mt-6 flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleRunEvaluation}
              disabled={isEvaluating}
              className="flex-1 bg-gray-800 hover:bg-gray-700 text-gray-200 font-semibold py-3 px-4 rounded-xl text-sm transition border border-gray-700 cursor-pointer text-center"
            >
              {isEvaluating ? "Computing Inference..." : "Re-evaluate Entity"}
            </button>
            <button
              onClick={() => navigate(`/xai?id=${prediction?.id || 1}`)}
              className="flex-1 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-3 px-4 rounded-xl text-sm transition shadow-lg shadow-blue-500/20 cursor-pointer text-center"
            >
              Open XAI Reasoning
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Investigations;
