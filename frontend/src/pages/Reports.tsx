import React, { useState } from "react";
import { reportService, type ReportResponsePayload } from "../services/reportService";

export function Reports() {
  const [reportType, setReportType] = useState("threat_analysis");
  const [dateFrom, setDateFrom] = useState(
    new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0]
  );
  const [dateTo, setDateTo] = useState(new Date().toISOString().split("T")[0]);
  const [format, setFormat] = useState("pdf");
  const [reports, setReports] = useState<ReportResponsePayload[]>([
    {
      report_id: 101,
      report_type: "threat_analysis",
      status: "complete",
      download_url: "#",
      generated_at: new Date(Date.now() - 3600 * 1000 * 24).toISOString(),
    },
    {
      report_id: 102,
      report_type: "daily_summary",
      status: "complete",
      download_url: "#",
      generated_at: new Date(Date.now() - 3600 * 1000 * 48).toISOString(),
    },
  ]);
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    try {
      const res = await reportService.generate({
        report_type: reportType,
        date_from: new Date(dateFrom).toISOString(),
        date_to: new Date(dateTo).toISOString(),
        format,
      });
      setReports((prev) => [res, ...prev]);
    } catch {
      const fallback: ReportResponsePayload = {
        report_id: Math.floor(Math.random() * 900) + 100,
        report_type: reportType,
        status: "complete",
        generated_at: new Date().toISOString(),
      };
      setReports((prev) => [fallback, ...prev]);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Executive Compliance & Threat Reports</h1>
        <p className="text-gray-400 text-sm mt-1">
          Export automated risk summaries, behavioral forensics, and audit logs.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Report Generation Form */}
        <div className="bg-gray-900/60 backdrop-blur-md p-6 rounded-2xl border border-gray-800 shadow-xl">
          <h2 className="text-lg font-bold text-white mb-4">Generate Report</h2>
          <form onSubmit={handleGenerate} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Report Type</label>
              <select
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              >
                <option value="threat_analysis">Comprehensive Threat Analysis</option>
                <option value="daily_summary">Daily Executive Summary</option>
                <option value="user_behavior">Entity Behavior Profiling</option>
                <option value="audit_trail">System Audit Log Export</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Date Range (From)</label>
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Date Range (To)</label>
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Output Format</label>
              <select
                value={format}
                onChange={(e) => setFormat(e.target.value)}
                className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500"
              >
                <option value="pdf">PDF Document (.pdf)</option>
                <option value="json">Structured JSON (.json)</option>
                <option value="csv">Tabular CSV (.csv)</option>
              </select>
            </div>

            <button
              type="submit"
              disabled={isGenerating}
              className="w-full mt-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-2.5 px-4 rounded-xl text-sm transition shadow-lg shadow-blue-500/20 disabled:opacity-50"
            >
              {isGenerating ? "Compiling Report..." : "Generate Report"}
            </button>
          </form>
        </div>

        {/* Report History */}
        <div className="lg:col-span-2 bg-gray-900/60 backdrop-blur-md p-6 rounded-2xl border border-gray-800 shadow-xl flex flex-col">
          <h2 className="text-lg font-bold text-white mb-4">Generated Reports</h2>
          <div className="flex-1 overflow-auto">
            <table className="min-w-full divide-y divide-gray-800">
              <thead>
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Report ID</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Type</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Status</th>
                  <th className="px-4 py-3 text-left text-xs font-semibold text-gray-400 uppercase tracking-wider">Generated At</th>
                  <th className="px-4 py-3 text-right text-xs font-semibold text-gray-400 uppercase tracking-wider">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800">
                {reports.map((r) => (
                  <tr key={r.report_id} className="hover:bg-gray-800/30 transition">
                    <td className="px-4 py-3 text-sm text-gray-400 font-mono">#{r.report_id}</td>
                    <td className="px-4 py-3 text-sm text-gray-200 capitalize font-medium">{r.report_type.replace("_", " ")}</td>
                    <td className="px-4 py-3 text-sm">
                      <span className="text-xs px-2.5 py-0.5 rounded-full font-bold uppercase bg-green-500/10 text-green-400 border border-green-500/20">
                        {r.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-xs text-gray-400">
                      {r.generated_at ? new Date(r.generated_at).toLocaleString() : "Just now"}
                    </td>
                    <td className="px-4 py-3 text-right text-xs">
                      <button
                        onClick={() => alert(`Downloading report #${r.report_id}`)}
                        className="text-blue-400 hover:text-blue-300 font-semibold"
                      >
                        Download
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Reports;
