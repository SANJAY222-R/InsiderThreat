import React, { useEffect, useState, useMemo } from "react";
import {
  reportService,
  type ReportItem,
  type ReportDetailItem,
  type ReportsDashboardSummary,
} from "../services/reportService";

export function Reports() {
  // Form State
  const [reportType, setReportType] = useState("threat_analysis");
  const [customTitle, setCustomTitle] = useState("");
  const [datePreset, setDatePreset] = useState<"24h" | "7d" | "30d" | "90d" | "custom">("7d");
  const [dateFrom, setDateFrom] = useState(
    new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString().split("T")[0]
  );
  const [dateTo, setDateTo] = useState(new Date().toISOString().split("T")[0]);
  const [format, setFormat] = useState("pdf");

  // Data & Async State
  const [reports, setReports] = useState<ReportItem[]>([]);
  const [summary, setSummary] = useState<ReportsDashboardSummary | null>(null);
  const [isLoadingList, setIsLoadingList] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isInstantDownloading, setIsInstantDownloading] = useState(false);
  const [downloadingId, setDownloadingId] = useState<number | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  // Filter & Search State
  const [filterType, setFilterType] = useState<string>("all");
  const [filterFormat, setFilterFormat] = useState<string>("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Preview Modal State
  const [previewReport, setPreviewReport] = useState<ReportDetailItem | null>(null);
  const [previewingId, setPreviewingId] = useState<number | null>(null);

  // Notifications State
  const [notification, setNotification] = useState<{
    type: "success" | "error" | "info";
    message: string;
  } | null>(null);

  const showNotification = (type: "success" | "error" | "info", message: string) => {
    setNotification({ type, message });
    setTimeout(() => {
      setNotification((prev) => (prev?.message === message ? null : prev));
    }, 5000);
  };

  // Date Preset Handler
  const handlePresetChange = (preset: "24h" | "7d" | "30d" | "90d" | "custom") => {
    setDatePreset(preset);
    const now = new Date();
    const todayStr = now.toISOString().split("T")[0];
    setDateTo(todayStr);

    let daysAgo = 7;
    if (preset === "24h") daysAgo = 1;
    else if (preset === "7d") daysAgo = 7;
    else if (preset === "30d") daysAgo = 30;
    else if (preset === "90d") daysAgo = 90;

    if (preset !== "custom") {
      const past = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000);
      setDateFrom(past.toISOString().split("T")[0]);
    }
  };

  // Initial Data Fetch
  const loadReportsAndSummary = async () => {
    setIsLoadingList(true);
    try {
      const [reportsData, summaryData] = await Promise.allSettled([
        reportService.getReports(),
        reportService.getSummary(),
      ]);

      if (reportsData.status === "fulfilled") {
        setReports(reportsData.value);
      }
      if (summaryData.status === "fulfilled") {
        setSummary(summaryData.value);
      }
    } catch {
      showNotification("error", "Unable to retrieve reports history. Please verify server connection.");
    } finally {
      setIsLoadingList(false);
    }
  };

  useEffect(() => {
    loadReportsAndSummary();
  }, []);

  // Generate & Save Report
  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsGenerating(true);
    try {
      const payload = {
        report_type: reportType,
        date_from: new Date(`${dateFrom}T00:00:00Z`).toISOString(),
        date_to: new Date(`${dateTo}T23:59:59Z`).toISOString(),
        format,
        title: customTitle.trim() || undefined,
      };

      const newReport = await reportService.generate(payload);
      setReports((prev) => [newReport, ...prev]);
      showNotification("success", `Report "${newReport.title}" generated successfully!`);
      setCustomTitle("");
      // Refresh summary
      reportService.getSummary().then(setSummary).catch(() => {});
    } catch (err: any) {
      showNotification("error", err?.message || "Failed to generate report.");
    } finally {
      setIsGenerating(false);
    }
  };

  // Instant Download without saving
  const handleInstantDownload = async () => {
    setIsInstantDownloading(true);
    try {
      const payload = {
        report_type: reportType,
        date_from: new Date(`${dateFrom}T00:00:00Z`).toISOString(),
        date_to: new Date(`${dateTo}T23:59:59Z`).toISOString(),
        format,
        title: customTitle.trim() || undefined,
      };

      await reportService.instantDownload(payload);
      showNotification("success", `Instant ${format.toUpperCase()} report streamed and downloaded!`);
    } catch (err: any) {
      showNotification("error", err?.message || "Failed to download instant report.");
    } finally {
      setIsInstantDownloading(false);
    }
  };

  // Download Existing Report
  const handleDownload = async (report: ReportItem, formatOverride?: string) => {
    setDownloadingId(report.id);
    try {
      const targetFmt = formatOverride || report.format || "pdf";
      await reportService.downloadReport(
        report.id,
        targetFmt,
        `report_${report.id}_${report.report_type}.${targetFmt}`
      );
      showNotification("success", `Downloaded Report #${report.id} (${targetFmt.toUpperCase()})`);
    } catch (err: any) {
      showNotification("error", err?.message || `Failed to download Report #${report.id}.`);
    } finally {
      setDownloadingId(null);
    }
  };

  // Open Preview Modal
  const handleOpenPreview = async (reportId: number) => {
    setPreviewingId(reportId);
    try {
      const detailed = await reportService.getReport(reportId);
      setPreviewReport(detailed);
    } catch (err: any) {
      showNotification("error", err?.message || "Failed to load report preview details.");
    } finally {
      setPreviewingId(null);
    }
  };

  // Delete Report
  const handleDeleteReport = async (reportId: number) => {
    if (!window.confirm(`Are you sure you want to delete Report #${reportId}?`)) {
      return;
    }
    setDeletingId(reportId);
    try {
      await reportService.deleteReport(reportId);
      setReports((prev) => prev.filter((r) => r.id !== reportId));
      if (previewReport?.id === reportId) {
        setPreviewReport(null);
      }
      showNotification("info", `Report #${reportId} deleted.`);
      reportService.getSummary().then(setSummary).catch(() => {});
    } catch (err: any) {
      showNotification("error", err?.message || "Failed to delete report.");
    } finally {
      setDeletingId(null);
    }
  };

  // Filtered Reports
  const filteredReports = useMemo(() => {
    return reports.filter((r) => {
      if (filterType !== "all" && r.report_type !== filterType) return false;
      if (filterFormat !== "all" && r.format !== filterFormat) return false;
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesId = `#${r.id}`.includes(q) || String(r.id).includes(q);
        const matchesTitle = r.title.toLowerCase().includes(q);
        const matchesType = r.report_type.toLowerCase().includes(q);
        const matchesAuthor = (r.created_by || "").toLowerCase().includes(q);
        if (!matchesId && !matchesTitle && !matchesType && !matchesAuthor) return false;
      }
      return true;
    });
  }, [reports, filterType, filterFormat, searchQuery]);

  // Format Helper
  const getFormatBadge = (fmt: string) => {
    switch (fmt.toLowerCase()) {
      case "pdf":
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            PDF
          </span>
        );
      case "csv":
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            CSV
          </span>
        );
      case "json":
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            JSON
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
            {fmt.toUpperCase()}
          </span>
        );
    }
  };

  const getTypeBadge = (type: string) => {
    const typeLabel = type.replace(/_/g, " ").toUpperCase();
    switch (type) {
      case "threat_analysis":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-500/15 text-red-300 border border-red-500/30">
            {typeLabel}
          </span>
        );
      case "daily_summary":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-500/15 text-blue-300 border border-blue-500/30">
            {typeLabel}
          </span>
        );
      case "user_behavior":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-500/15 text-purple-300 border border-purple-500/30">
            {typeLabel}
          </span>
        );
      case "audit_trail":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-cyan-500/15 text-cyan-300 border border-cyan-500/30">
            {typeLabel}
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-700 text-gray-300">
            {typeLabel}
          </span>
        );
    }
  };

  const getThreatLevelBadge = (level: string) => {
    const lvl = (level || "LOW").toUpperCase();
    if (lvl === "CRITICAL") {
      return <span className="px-2 py-0.5 rounded text-xs font-bold bg-red-500/20 text-red-400 border border-red-500/30">CRITICAL</span>;
    }
    if (lvl === "HIGH") {
      return <span className="px-2 py-0.5 rounded text-xs font-bold bg-orange-500/20 text-orange-400 border border-orange-500/30">HIGH</span>;
    }
    if (lvl === "MEDIUM") {
      return <span className="px-2 py-0.5 rounded text-xs font-bold bg-yellow-500/20 text-yellow-400 border border-yellow-500/30">MEDIUM</span>;
    }
    return <span className="px-2 py-0.5 rounded text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">LOW</span>;
  };

  const formatFileSize = (bytes?: number | null) => {
    if (!bytes) return "—";
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="space-y-8 animate-in fade-in duration-500 pb-12">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-gray-800/80 pb-6">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-600/10 border border-blue-500/30 rounded-xl text-blue-400 shadow-inner">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <div>
              <h1 className="text-3xl font-extrabold text-white tracking-tight">
                Executive Threat & Compliance Reports
              </h1>
              <p className="text-gray-400 text-sm mt-0.5">
                Generate, inspect, and export enterprise-grade threat intelligence and forensic audit reports.
              </p>
            </div>
          </div>
        </div>

        {/* Quick Refresh */}
        <button
          onClick={loadReportsAndSummary}
          disabled={isLoadingList}
          className="inline-flex items-center gap-2 px-3.5 py-2 bg-gray-900 hover:bg-gray-800 border border-gray-700/80 rounded-xl text-sm font-medium text-gray-300 transition shadow-sm hover:text-white disabled:opacity-50 self-start md:self-auto"
        >
          <svg
            className={`w-4 h-4 ${isLoadingList ? "animate-spin text-blue-400" : "text-gray-400"}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
            />
          </svg>
          Refresh Feed
        </button>
      </div>

      {/* Notification Toast */}
      {notification && (
        <div
          className={`p-4 rounded-xl border flex items-center justify-between text-sm shadow-lg animate-in slide-in-from-top-2 duration-300 ${
            notification.type === "success"
              ? "bg-emerald-950/70 border-emerald-500/40 text-emerald-200"
              : notification.type === "error"
              ? "bg-rose-950/70 border-rose-500/40 text-rose-200"
              : "bg-blue-950/70 border-blue-500/40 text-blue-200"
          }`}
        >
          <div className="flex items-center gap-3">
            {notification.type === "success" && (
              <svg className="w-5 h-5 text-emerald-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
              </svg>
            )}
            {notification.type === "error" && (
              <svg className="w-5 h-5 text-rose-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            )}
            {notification.type === "info" && (
              <svg className="w-5 h-5 text-blue-400 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            )}
            <span>{notification.message}</span>
          </div>
          <button
            onClick={() => setNotification(null)}
            className="text-gray-400 hover:text-white ml-4 text-xs font-semibold uppercase tracking-wider"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* KPI Overview Tiles */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-gray-900/60 backdrop-blur-md p-5 rounded-2xl border border-gray-800/80 shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-blue-500/10 rounded-full blur-2xl group-hover:bg-blue-500/20 transition duration-500" />
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Total Reports</div>
          <div className="text-2xl font-black text-white mt-1">
            {summary?.total_reports ?? reports.length}
          </div>
          <div className="text-xs text-blue-400/90 mt-1 flex items-center gap-1">
            <span>Historical archives compiled</span>
          </div>
        </div>

        <div className="bg-gray-900/60 backdrop-blur-md p-5 rounded-2xl border border-gray-800/80 shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-red-500/10 rounded-full blur-2xl group-hover:bg-red-500/20 transition duration-500" />
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Threat Analyses</div>
          <div className="text-2xl font-black text-white mt-1">
            {summary?.reports_by_type?.["threat_analysis"] ??
              reports.filter((r) => r.report_type === "threat_analysis").length}
          </div>
          <div className="text-xs text-red-400/90 mt-1 flex items-center gap-1">
            <span>Deep anomaly assessments</span>
          </div>
        </div>

        <div className="bg-gray-900/60 backdrop-blur-md p-5 rounded-2xl border border-gray-800/80 shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-purple-500/10 rounded-full blur-2xl group-hover:bg-purple-500/20 transition duration-500" />
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Behavior & Daily</div>
          <div className="text-2xl font-black text-white mt-1">
            {(summary?.reports_by_type?.["daily_summary"] ?? 0) +
              (summary?.reports_by_type?.["user_behavior"] ?? 0)}
          </div>
          <div className="text-xs text-purple-400/90 mt-1 flex items-center gap-1">
            <span>Entity profiles & summaries</span>
          </div>
        </div>

        <div className="bg-gray-900/60 backdrop-blur-md p-5 rounded-2xl border border-gray-800/80 shadow-lg relative overflow-hidden group">
          <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/10 rounded-full blur-2xl group-hover:bg-emerald-500/20 transition duration-500" />
          <div className="text-xs font-semibold text-gray-400 uppercase tracking-wider">Active Threats Monitored</div>
          <div className="text-2xl font-black text-white mt-1">
            {summary?.total_alerts ?? "—"}
          </div>
          <div className="text-xs text-emerald-400/90 mt-1 flex items-center gap-1">
            <span>{summary?.total_predictions ?? 0} graph prediction events</span>
          </div>
        </div>
      </div>

      {/* Main Grid: Report Generator + Report Library */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Generator Form Panel (4 cols) */}
        <div className="lg:col-span-4 bg-gray-900/70 backdrop-blur-md p-6 rounded-2xl border border-gray-800 shadow-xl space-y-5">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse" />
              Configure & Compile Report
            </h2>
            <p className="text-xs text-gray-400 mt-1">
              Select intelligence parameters, timeframes, and formatting for autonomous report aggregation.
            </p>
          </div>

          <form onSubmit={handleGenerate} className="space-y-4">
            {/* Report Type */}
            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                Report Focus Type
              </label>
              <select
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 transition shadow-inner"
              >
                <option value="threat_analysis">Comprehensive Threat Analysis</option>
                <option value="daily_summary">Executive Daily Threat Summary</option>
                <option value="user_behavior">Entity Behavior Profiling (UEBA)</option>
                <option value="audit_trail">System Security & Compliance Audit Log</option>
              </select>
            </div>

            {/* Custom Report Title */}
            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                Custom Title (Optional)
              </label>
              <input
                type="text"
                placeholder="e.g., Q3 High-Risk Exfiltration Review"
                value={customTitle}
                onChange={(e) => setCustomTitle(e.target.value)}
                className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3.5 py-2 text-sm text-white placeholder-gray-600 focus:outline-none focus:border-blue-500 transition shadow-inner"
              />
            </div>

            {/* Date Range Presets */}
            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                Timeframe Horizon
              </label>
              <div className="grid grid-cols-4 gap-1.5 p-1 bg-gray-950 border border-gray-800 rounded-xl">
                {(["24h", "7d", "30d", "90d"] as const).map((preset) => (
                  <button
                    key={preset}
                    type="button"
                    onClick={() => handlePresetChange(preset)}
                    className={`py-1.5 text-xs font-semibold rounded-lg transition ${
                      datePreset === preset
                        ? "bg-blue-600 text-white shadow"
                        : "text-gray-400 hover:text-white hover:bg-gray-900"
                    }`}
                  >
                    {preset.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>

            {/* Custom Date Inputs */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-[11px] font-medium text-gray-400 mb-1">From Date</label>
                <input
                  type="date"
                  value={dateFrom}
                  onChange={(e) => {
                    setDatePreset("custom");
                    setDateFrom(e.target.value);
                  }}
                  className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition"
                />
              </div>
              <div>
                <label className="block text-[11px] font-medium text-gray-400 mb-1">To Date</label>
                <input
                  type="date"
                  value={dateTo}
                  onChange={(e) => {
                    setDatePreset("custom");
                    setDateTo(e.target.value);
                  }}
                  className="w-full bg-gray-950 border border-gray-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-blue-500 transition"
                />
              </div>
            </div>

            {/* Export Format */}
            <div>
              <label className="block text-xs font-semibold text-gray-300 uppercase tracking-wider mb-1.5">
                Output Format
              </label>
              <div className="grid grid-cols-3 gap-2">
                {[
                  { id: "pdf", label: "PDF Spec", ext: ".pdf", iconColor: "text-rose-400" },
                  { id: "csv", label: "CSV Tabular", ext: ".csv", iconColor: "text-emerald-400" },
                  { id: "json", label: "JSON Raw", ext: ".json", iconColor: "text-amber-400" },
                ].map((fmt) => (
                  <button
                    key={fmt.id}
                    type="button"
                    onClick={() => setFormat(fmt.id)}
                    className={`flex flex-col items-center justify-center p-2.5 rounded-xl border text-xs font-semibold transition ${
                      format === fmt.id
                        ? "bg-blue-600/20 border-blue-500 text-white shadow-sm"
                        : "bg-gray-950 border-gray-800 text-gray-400 hover:border-gray-700 hover:text-gray-200"
                    }`}
                  >
                    <span className={`text-[13px] font-bold ${fmt.iconColor}`}>{fmt.ext}</span>
                    <span className="text-[10px] mt-0.5">{fmt.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Submit Action Buttons */}
            <div className="pt-2 space-y-2">
              <button
                type="submit"
                disabled={isGenerating || isInstantDownloading}
                className="w-full flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-2.5 px-4 rounded-xl text-sm transition shadow-lg shadow-blue-500/20 disabled:opacity-50 cursor-pointer"
              >
                {isGenerating ? (
                  <>
                    <svg className="animate-spin w-4 h-4 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                    <span>Compiling Threat Intelligence...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4" />
                    </svg>
                    <span>Generate & Save Report</span>
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={handleInstantDownload}
                disabled={isGenerating || isInstantDownloading}
                className="w-full flex items-center justify-center gap-2 bg-gray-950 hover:bg-gray-800 text-gray-300 hover:text-white border border-gray-800 font-semibold py-2 px-4 rounded-xl text-xs transition disabled:opacity-50 cursor-pointer"
              >
                {isInstantDownloading ? (
                  <>
                    <svg className="animate-spin w-3.5 h-3.5 text-blue-400" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                    </svg>
                    <span>Streaming Download...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    <span>Instant Direct Download ({format.toUpperCase()})</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Report Library Table Panel (8 cols) */}
        <div className="lg:col-span-8 bg-gray-900/70 backdrop-blur-md p-6 rounded-2xl border border-gray-800 shadow-xl space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h2 className="text-lg font-bold text-white">Generated Report Repository</h2>
              <p className="text-xs text-gray-400 mt-0.5">
                Inspect compiled threat findings, preview metrics, or download binary archives.
              </p>
            </div>

            {/* Search Box */}
            <div className="relative w-full sm:w-64">
              <svg
                className="w-4 h-4 text-gray-500 absolute left-3 top-2.5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              <input
                type="text"
                placeholder="Search reports or authors..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-gray-950 border border-gray-800 rounded-xl pl-9 pr-3 py-1.5 text-xs text-white placeholder-gray-600 focus:outline-none focus:border-blue-500 transition"
              />
            </div>
          </div>

          {/* Filters Bar */}
          <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-gray-800/60">
            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider mr-1">Type:</span>
            {[
              { id: "all", label: "All Types" },
              { id: "threat_analysis", label: "Threat Analysis" },
              { id: "daily_summary", label: "Daily Summary" },
              { id: "user_behavior", label: "Behavior Profile" },
              { id: "audit_trail", label: "Audit Trail" },
            ].map((f) => (
              <button
                key={f.id}
                onClick={() => setFilterType(f.id)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition ${
                  filterType === f.id
                    ? "bg-blue-600/30 text-blue-300 border border-blue-500/50"
                    : "bg-gray-950 text-gray-400 border border-gray-800 hover:text-gray-200"
                }`}
              >
                {f.label}
              </button>
            ))}

            <div className="h-4 w-px bg-gray-800 mx-1 hidden sm:block" />

            <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider mr-1">Format:</span>
            {[
              { id: "all", label: "All" },
              { id: "pdf", label: "PDF" },
              { id: "csv", label: "CSV" },
              { id: "json", label: "JSON" },
            ].map((fmt) => (
              <button
                key={fmt.id}
                onClick={() => setFilterFormat(fmt.id)}
                className={`px-2 py-1 rounded-lg text-xs font-medium transition ${
                  filterFormat === fmt.id
                    ? "bg-purple-600/30 text-purple-300 border border-purple-500/50"
                    : "bg-gray-950 text-gray-400 border border-gray-800 hover:text-gray-200"
                }`}
              >
                {fmt.label}
              </button>
            ))}
          </div>

          {/* Table Container */}
          <div className="overflow-x-auto rounded-xl border border-gray-800/80">
            <table className="min-w-full divide-y divide-gray-800 text-left">
              <thead className="bg-gray-950/80 text-[11px] font-bold text-gray-400 uppercase tracking-wider">
                <tr>
                  <th className="px-4 py-3">Report Details</th>
                  <th className="px-4 py-3">Type & Format</th>
                  <th className="px-4 py-3">Coverage Period</th>
                  <th className="px-4 py-3">Size & Status</th>
                  <th className="px-4 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-800/80 bg-gray-900/30 text-xs">
                {isLoadingList ? (
                  <tr>
                    <td colSpan={5} className="py-12 text-center text-gray-400">
                      <div className="flex flex-col items-center justify-center gap-2">
                        <svg className="animate-spin w-6 h-6 text-blue-500" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                        </svg>
                        <span>Loading historical intelligence reports...</span>
                      </div>
                    </td>
                  </tr>
                ) : filteredReports.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="py-12 text-center text-gray-500">
                      <div className="flex flex-col items-center justify-center gap-2">
                        <svg className="w-8 h-8 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth="1.5"
                            d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                          />
                        </svg>
                        <span>No reports found matching selected criteria.</span>
                      </div>
                    </td>
                  </tr>
                ) : (
                  filteredReports.map((r) => (
                    <tr key={r.id} className="hover:bg-gray-800/40 transition">
                      {/* Title & Author */}
                      <td className="px-4 py-3">
                        <div className="flex flex-col">
                          <span className="font-semibold text-gray-200 hover:text-blue-400 transition cursor-pointer" onClick={() => handleOpenPreview(r.id)}>
                            {r.title}
                          </span>
                          <span className="text-[11px] text-gray-400 font-mono mt-0.5">
                            ID #{r.id} • by {r.created_by || "SOC Analyst"}
                          </span>
                        </div>
                      </td>

                      {/* Type & Format */}
                      <td className="px-4 py-3">
                        <div className="flex flex-col gap-1 items-start">
                          {getTypeBadge(r.report_type)}
                          <div className="mt-0.5">{getFormatBadge(r.format)}</div>
                        </div>
                      </td>

                      {/* Coverage Window */}
                      <td className="px-4 py-3 text-gray-300 whitespace-nowrap">
                        <div className="text-[11px] text-gray-400">
                          {r.date_from ? new Date(r.date_from).toLocaleDateString() : "—"} to{" "}
                          {r.date_to ? new Date(r.date_to).toLocaleDateString() : "—"}
                        </div>
                        <div className="text-[10px] text-gray-500 mt-0.5">
                          Compiled {r.created_at ? new Date(r.created_at).toLocaleDateString() : "Recently"}
                        </div>
                      </td>

                      {/* Status & Size */}
                      <td className="px-4 py-3">
                        <div className="flex flex-col items-start gap-1">
                          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold uppercase bg-green-500/10 text-green-400 border border-green-500/20">
                            {r.status}
                          </span>
                          <span className="text-[10px] text-gray-400 font-mono">
                            {formatFileSize(r.file_size)}
                          </span>
                        </div>
                      </td>

                      {/* Actions */}
                      <td className="px-4 py-3 text-right whitespace-nowrap">
                        <div className="inline-flex items-center gap-1.5">
                          {/* Preview Button */}
                          <button
                            onClick={() => handleOpenPreview(r.id)}
                            disabled={previewingId === r.id}
                            title="Inspect & Preview Report"
                            className="p-1.5 bg-gray-950 hover:bg-gray-800 text-gray-300 hover:text-white border border-gray-800 rounded-lg transition disabled:opacity-50"
                          >
                            {previewingId === r.id ? (
                              <svg className="animate-spin w-4 h-4 text-blue-400" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                              </svg>
                            ) : (
                              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                              </svg>
                            )}
                          </button>

                          {/* Download Button */}
                          <button
                            onClick={() => handleDownload(r)}
                            disabled={downloadingId === r.id}
                            title={`Download ${r.format.toUpperCase()} File`}
                            className="inline-flex items-center gap-1 px-2.5 py-1.5 bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 hover:text-blue-200 border border-blue-500/40 rounded-lg font-semibold text-xs transition disabled:opacity-50"
                          >
                            {downloadingId === r.id ? (
                              <svg className="animate-spin w-3.5 h-3.5 text-blue-400" fill="none" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                              </svg>
                            ) : (
                              <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                              </svg>
                            )}
                            <span>Download</span>
                          </button>

                          {/* Delete Button */}
                          <button
                            onClick={() => handleDeleteReport(r.id)}
                            disabled={deletingId === r.id}
                            title="Delete Report"
                            className="p-1.5 bg-gray-950 hover:bg-rose-950/40 text-gray-400 hover:text-rose-400 border border-gray-800 hover:border-rose-800/50 rounded-lg transition disabled:opacity-50"
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Interactive Report Inspection & Preview Modal */}
      {previewReport && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="p-6 border-b border-gray-800 flex items-start justify-between gap-4 bg-gray-950/60">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-blue-400">REPORT #{previewReport.id}</span>
                  {getTypeBadge(previewReport.report_type)}
                  {getFormatBadge(previewReport.format)}
                </div>
                <h3 className="text-xl font-bold text-white tracking-tight">
                  {previewReport.title}
                </h3>
                <p className="text-xs text-gray-400">
                  Coverage: {new Date(previewReport.date_from).toLocaleDateString()} –{" "}
                  {new Date(previewReport.date_to).toLocaleDateString()} | Author:{" "}
                  {previewReport.created_by || "SOC Analyst"}
                </p>
              </div>

              <button
                onClick={() => setPreviewReport(null)}
                className="p-2 text-gray-400 hover:text-white rounded-xl bg-gray-900 hover:bg-gray-800 border border-gray-800 transition"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Modal Body */}
            <div className="p-6 overflow-y-auto space-y-6">
              {/* Executive Metrics Bar */}
              {previewReport.summary_metrics && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                    Executive Threat Metrics
                  </h4>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    <div className="bg-gray-950 p-3.5 rounded-xl border border-gray-800">
                      <div className="text-[11px] text-gray-400">Predictions Evaluated</div>
                      <div className="text-lg font-black text-white mt-0.5">
                        {previewReport.summary_metrics.total_predictions ?? 0}
                      </div>
                    </div>
                    <div className="bg-gray-950 p-3.5 rounded-xl border border-gray-800">
                      <div className="text-[11px] text-gray-400">Alerts Flagged</div>
                      <div className="text-lg font-black text-red-400 mt-0.5">
                        {previewReport.summary_metrics.total_alerts ?? 0}
                      </div>
                    </div>
                    <div className="bg-gray-950 p-3.5 rounded-xl border border-gray-800">
                      <div className="text-[11px] text-gray-400">Average Risk Score</div>
                      <div className="text-lg font-black text-amber-400 mt-0.5">
                        {previewReport.summary_metrics.avg_risk_score ?? 0.0} / 100
                      </div>
                    </div>
                    <div className="bg-gray-950 p-3.5 rounded-xl border border-gray-800">
                      <div className="text-[11px] text-gray-400">Peak Risk Score</div>
                      <div className="text-lg font-black text-rose-500 mt-0.5">
                        {previewReport.summary_metrics.max_risk_score ?? 0.0} / 100
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Top Flagged Entities Table */}
              {previewReport.data?.top_entities && previewReport.data.top_entities.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                    Top Monitored Entities & Behavioral Anomalies
                  </h4>
                  <div className="overflow-x-auto rounded-xl border border-gray-800">
                    <table className="min-w-full divide-y divide-gray-800 text-left text-xs">
                      <thead className="bg-gray-950 text-[10px] font-bold text-gray-400 uppercase tracking-wider">
                        <tr>
                          <th className="px-3 py-2">Employee ID</th>
                          <th className="px-3 py-2">Risk Score</th>
                          <th className="px-3 py-2">Threat Level</th>
                          <th className="px-3 py-2">Confidence</th>
                          <th className="px-3 py-2">Alerts</th>
                          <th className="px-3 py-2">Anomaly Drivers</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-800 bg-gray-900/40">
                        {previewReport.data.top_entities.map((entity, idx) => (
                          <tr key={idx} className="hover:bg-gray-800/30">
                            <td className="px-3 py-2 font-mono font-semibold text-gray-200">
                              {entity.employee_id}
                            </td>
                            <td className="px-3 py-2 font-bold text-amber-300">
                              {entity.max_risk_score.toFixed(1)}
                            </td>
                            <td className="px-3 py-2">
                              {getThreatLevelBadge(entity.threat_level)}
                            </td>
                            <td className="px-3 py-2 text-gray-400 font-mono">
                              {(entity.confidence * 100).toFixed(0)}%
                            </td>
                            <td className="px-3 py-2 font-semibold text-red-400">
                              {entity.alert_count}
                            </td>
                            <td className="px-3 py-2 text-gray-300 truncate max-w-xs">
                              {entity.top_indicators || "Behavioral Deviation"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}

              {/* Recent Incident Alerts */}
              {previewReport.data?.recent_alerts && previewReport.data.recent_alerts.length > 0 && (
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">
                    Incident Triage & Forensic Events
                  </h4>
                  <div className="overflow-x-auto rounded-xl border border-gray-800">
                    <table className="min-w-full divide-y divide-gray-800 text-left text-xs">
                      <thead className="bg-gray-950 text-[10px] font-bold text-gray-400 uppercase tracking-wider">
                        <tr>
                          <th className="px-3 py-2">Alert ID</th>
                          <th className="px-3 py-2">Employee</th>
                          <th className="px-3 py-2">Severity</th>
                          <th className="px-3 py-2">Status</th>
                          <th className="px-3 py-2">Incident Description</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-gray-800 bg-gray-900/40">
                        {previewReport.data.recent_alerts.slice(0, 5).map((al) => (
                          <tr key={al.id} className="hover:bg-gray-800/30">
                            <td className="px-3 py-2 font-mono text-gray-400">#{al.id}</td>
                            <td className="px-3 py-2 font-mono text-gray-200">{al.employee_id}</td>
                            <td className="px-3 py-2 font-semibold uppercase text-xs text-orange-400">
                              {al.severity}
                            </td>
                            <td className="px-3 py-2 uppercase text-[10px] font-bold text-gray-400">
                              {al.status}
                            </td>
                            <td className="px-3 py-2 text-gray-300">{al.title}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer with Multi-Format Export */}
            <div className="p-5 border-t border-gray-800 bg-gray-950/80 flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-400">Direct Export:</span>
                {(["pdf", "csv", "json"] as const).map((fmt) => (
                  <button
                    key={fmt}
                    onClick={() => handleDownload(previewReport, fmt)}
                    disabled={downloadingId === previewReport.id}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gray-900 hover:bg-gray-800 text-gray-200 hover:text-white border border-gray-700 rounded-lg text-xs font-semibold transition"
                  >
                    <svg className="w-3.5 h-3.5 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    <span>Download {fmt.toUpperCase()}</span>
                  </button>
                ))}
              </div>

              <button
                onClick={() => setPreviewReport(null)}
                className="px-4 py-2 bg-gray-800 hover:bg-gray-700 text-white rounded-xl text-xs font-bold transition"
              >
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Reports;
