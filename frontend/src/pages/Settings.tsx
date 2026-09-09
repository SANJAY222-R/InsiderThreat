import { useEffect, useState } from "react";
import { api } from "../services/api";

export function Settings() {
  const [config, setConfig] = useState<{
    app_name: string;
    app_env: string;
    app_version: string;
    log_level: string;
    cors_origins: string;
  } | null>(null);

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        const data = await api.get<{
          app_name: string;
          app_env: string;
          app_version: string;
          log_level: string;
          cors_origins: string;
        }>("/settings/");
        setConfig(data);
      } catch {
        setConfig({
          app_name: "InsiderThreatDetection",
          app_env: "development",
          app_version: "1.0.0",
          log_level: "INFO",
          cors_origins: "http://localhost:5173",
        });
      } finally {
        // Loaded
      }
    };
    fetchSettings();
  }, []);

  return (
    <div className="space-y-8 animate-in fade-in duration-500 max-w-4xl">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">System Settings & Configuration</h1>
        <p className="text-gray-400 text-sm mt-1">
          Review core backend runtime configuration, telemetry targets, and system policies.
        </p>
      </div>

      <div className="bg-gray-900/60 backdrop-blur-md p-8 rounded-2xl border border-gray-800 shadow-xl space-y-6">
        <h2 className="text-lg font-bold text-white border-b border-gray-800 pb-3">Backend Runtime Info</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Application Name</label>
            <input
              type="text"
              readOnly
              value={config?.app_name || "InsiderThreatDetection"}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-gray-300 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Environment</label>
            <input
              type="text"
              readOnly
              value={config?.app_env || "development"}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-gray-300 font-mono capitalize"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">API Version</label>
            <input
              type="text"
              readOnly
              value={config?.app_version || "1.0.0"}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-gray-300 font-mono"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Log Level</label>
            <input
              type="text"
              readOnly
              value={config?.log_level || "INFO"}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-gray-300 font-mono uppercase"
            />
          </div>

          <div className="md:col-span-2">
            <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Allowed CORS Origins</label>
            <input
              type="text"
              readOnly
              value={config?.cors_origins || "http://localhost:5173"}
              className="w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-2.5 text-sm text-gray-300 font-mono"
            />
          </div>
        </div>
      </div>

      <div className="bg-gray-900/60 backdrop-blur-md p-8 rounded-2xl border border-gray-800 shadow-xl space-y-4">
        <h2 className="text-lg font-bold text-white border-b border-gray-800 pb-3">Security & Storage Parameters</h2>

        <div className="space-y-3 text-sm text-gray-400">
          <div className="flex justify-between py-2 border-b border-gray-800/60">
            <span>Authentication Scheme</span>
            <span className="text-white font-mono">OAuth2 Password Bearer / JWT (HS256)</span>
          </div>
          <div className="flex justify-between py-2 border-b border-gray-800/60">
            <span>Access Token TTL</span>
            <span className="text-white font-mono">30 Minutes</span>
          </div>
          <div className="flex justify-between py-2 border-b border-gray-800/60">
            <span>Refresh Token TTL</span>
            <span className="text-white font-mono">7 Days</span>
          </div>
          <div className="flex justify-between py-2">
            <span>Primary Graph Engine</span>
            <span className="text-white font-mono">Temporal Heterogeneous Graph (Neo4j / NetworkX)</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
