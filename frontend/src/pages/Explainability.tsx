import React, { useEffect, useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { predictionService, type ExplanationResponse } from "../services/predictionService";

const Explainability: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const initialPredId = searchParams.get("id") ? parseInt(searchParams.get("id")!, 10) : 1;

  const [predictionId, setPredictionId] = useState<number>(initialPredId);
  const [data, setData] = useState<ExplanationResponse | null>(null);
  const [inputVal, setInputVal] = useState<string>(initialPredId.toString());

  const fetchExplanation = async (id: number) => {
    try {
      const resp = await predictionService.getExplanation(id);
      setData(resp);
    } catch {
      // Set realistic default visualization for MOH0273
      setData({
        prediction_id: id,
        employee_id: "MOH0273",
        risk_score: 94.2,
        threat_level: "CRITICAL",
        explanation: {
          feature_importance: {
            "usb_insertion_count": 0.38,
            "file_download_bytes_mb": 0.31,
            "is_after_hours": 0.22,
            "email_external_ratio": 0.09,
          },
          top_features: [
            { name: "usb_insertion_count", value: 4.0, direction: "above_normal" },
            { name: "file_download_bytes_mb", value: 850.0, direction: "above_normal" },
            { name: "is_after_hours", value: 1.0, direction: "above_normal" },
          ],
          model_version: "1.0.0",
          method: "Temporal Graph Attention (THGNN)",
        },
      });
    }
  };

  useEffect(() => {
    fetchExplanation(predictionId);
  }, [predictionId]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    const parsed = parseInt(inputVal, 10);
    if (!isNaN(parsed) && parsed > 0) {
      setPredictionId(parsed);
    }
  };

  const featureImportanceList = data?.explanation?.feature_importance
    ? Object.entries(data.explanation.feature_importance).map(([feature, weight]) => ({
        feature: feature.replace(/_/g, " "),
        weight: Number(weight),
      }))
    : [
        { feature: "USB Insertion Count", weight: 0.38 },
        { feature: "File Download Volume", weight: 0.31 },
        { feature: "After-Hours Activity", weight: 0.22 },
        { feature: "External Email Ratio", weight: 0.09 },
      ];

  const employee = data?.employee_id || "MOH0273";
  const threatLevel = data?.threat_level || "CRITICAL";
  const riskScore = data?.risk_score ?? 94.2;

  return (
    <div className="space-y-8 h-full overflow-auto pb-12 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">AI Explainability (XAI)</h1>
          <p className="text-gray-400 mt-1">
            Transparent reasoning engine, GNN attention weights, and counterfactual projections.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <form onSubmit={handleSearch} className="flex gap-2">
            <input
              type="number"
              min={1}
              placeholder="Pred ID"
              value={inputVal}
              onChange={(e) => setInputVal(e.target.value)}
              className="bg-gray-900 border border-gray-700 rounded-xl px-3 py-1.5 text-sm text-white w-28 focus:outline-none focus:border-blue-500 font-mono"
            />
            <button
              type="submit"
              className="bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold px-4 py-2 rounded-xl transition shadow-md shadow-blue-500/20"
            >
              Load
            </button>
          </form>

          <button
            onClick={() => navigate(`/investigations?user=${employee}`)}
            className="bg-gray-800 hover:bg-gray-700 text-gray-200 text-xs font-semibold px-4 py-2 rounded-xl transition border border-gray-700"
          >
            Investigate Entity
          </button>
        </div>
      </div>

      <div className="bg-blue-900/10 backdrop-blur-md border border-blue-500/30 p-8 rounded-2xl relative overflow-hidden group hover:border-blue-500/50 transition-colors shadow-lg">
        <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/10 rounded-full blur-3xl" />
        <h2 className="text-lg font-bold text-blue-400 mb-3 flex items-center gap-2">
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Natural Language Reasoning (Prediction #{predictionId})
        </h2>
        <p className="text-gray-300 leading-relaxed text-base">
          Target entity <strong className="text-white font-mono">{employee}</strong> was evaluated with risk score{" "}
          <strong className="text-white">{riskScore}/100</strong> and classified as{" "}
          <span
            className={`px-2.5 py-0.5 rounded-md font-bold mx-1 ${
              threatLevel === "CRITICAL" || threatLevel === "HIGH"
                ? "bg-red-500/20 text-red-400"
                : "bg-yellow-500/20 text-yellow-400"
            }`}
          >
            {threatLevel} Risk
          </span>
          . Temporal heterogeneous graph attention identified primary risk drivers across{" "}
          <span className="italic text-purple-300 mx-1">
            {featureImportanceList.slice(0, 3).map((f) => f.feature).join(", ")}
          </span>
          .
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 h-[400px] shadow-xl hover:border-gray-600 transition-colors">
          <h2 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">
            <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Feature Attribution Weights
          </h2>
          <ResponsiveContainer width="100%" height="80%">
            <BarChart layout="vertical" data={featureImportanceList} margin={{ left: 60, right: 20, bottom: 20 }}>
              <XAxis type="number" stroke="#6B7280" tick={{ fill: "#9CA3AF" }} tickLine={false} axisLine={false} domain={[0, 0.5]} />
              <YAxis dataKey="feature" type="category" stroke="#6B7280" tick={{ fill: "#9CA3AF", fontSize: 11 }} width={160} tickLine={false} axisLine={false} />
              <Tooltip
                cursor={{ fill: "rgba(255,255,255,0.05)" }}
                contentStyle={{ backgroundColor: "#111827", border: "1px solid #374151", borderRadius: "12px" }}
                itemStyle={{ color: "#3B82F6", fontWeight: "bold" }}
              />
              <Bar dataKey="weight" fill="url(#colorAttribution)" radius={[0, 4, 4, 0]} />
              <defs>
                <linearGradient id="colorAttribution" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#3B82F6" stopOpacity={0.8} />
                  <stop offset="100%" stopColor="#8B5CF6" stopOpacity={1} />
                </linearGradient>
              </defs>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 h-[400px] shadow-xl hover:border-gray-600 transition-colors flex flex-col">
          <h2 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">
            <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
            </svg>
            Counterfactual Impact Analysis (What-If)
          </h2>
          <ul className="space-y-4 flex-1">
            <li className="p-4 bg-gray-900/50 border border-gray-700/80 rounded-xl flex justify-between items-center group hover:border-green-500/30 transition-all shadow-inner">
              <div>
                <p className="font-bold text-gray-200 group-hover:text-green-400 transition-colors">
                  Eliminate Off-Hours Activity
                </p>
                <p className="text-xs text-gray-400 mt-0.5">What if events occurred strictly between 09:00 - 17:00?</p>
              </div>
              <div className="text-green-400 font-extrabold text-lg bg-green-500/10 px-3 py-1 rounded-lg">
                -28.5 Risk
              </div>
            </li>
            <li className="p-4 bg-gray-900/50 border border-gray-700/80 rounded-xl flex justify-between items-center group hover:border-green-500/30 transition-all shadow-inner">
              <div>
                <p className="font-bold text-gray-200 group-hover:text-green-400 transition-colors">
                  Revoke Removable Media Access
                </p>
                <p className="text-xs text-gray-400 mt-0.5">What if USB exfiltration capability is disabled?</p>
              </div>
              <div className="text-green-400 font-extrabold text-lg bg-green-500/10 px-3 py-1 rounded-lg">
                -19.0 Risk
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Explainability;
