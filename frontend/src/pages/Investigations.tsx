import React from 'react';

const Investigations: React.FC = () => {
  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-right-8 duration-500">
      <div className="flex justify-between items-end mb-6">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">User Investigation</h1>
          <p className="text-gray-400 mt-1">Deep-dive behavioral profiling and threat verification.</p>
        </div>
      </div>
      
      <div className="bg-gray-800/40 backdrop-blur-md p-8 rounded-2xl border border-gray-700/60 shadow-2xl flex justify-between items-center relative overflow-hidden group">
        <div className="absolute top-0 right-0 w-64 h-64 bg-red-500/10 rounded-full blur-3xl group-hover:bg-red-500/20 transition-colors"></div>
        <div className="relative z-10">
          <div className="flex items-center gap-4 mb-2">
            <div className="w-16 h-16 rounded-full bg-gradient-to-br from-red-500 to-orange-600 flex items-center justify-center shadow-lg shadow-red-500/30">
              <span className="text-2xl font-bold text-white">U</span>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-100 flex items-center gap-2">
                User: U1234
                <span className="bg-red-500/20 text-red-400 text-xs px-2 py-0.5 rounded-full border border-red-500/30 font-bold uppercase tracking-wider">Targeted</span>
              </h2>
              <p className="text-gray-400 font-medium">Department: Engineering / Clearance: Level 2</p>
            </div>
          </div>
        </div>
        <div className="text-right relative z-10">
          <p className="text-sm font-semibold text-gray-400 uppercase tracking-wider mb-1">Current Risk Score</p>
          <p className="text-6xl font-black text-red-500 drop-shadow-[0_0_15px_rgba(239,68,68,0.5)]">85.0</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gray-800/40 backdrop-blur-md p-8 rounded-2xl border border-gray-700/60 shadow-xl hover:border-gray-600 transition-all">
          <h3 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">
            <svg className="w-5 h-5 text-orange-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
            Anomalous Behavior Summary
          </h3>
          <ul className="space-y-4">
            {[
              "Abnormal Login Time (03:00 AM) - Outside historical bounds",
              "Excessive File Access (120 files/session) - Financial Drive",
              "Unauthorized USB Insertion (Device ID: USB01)"
            ].map((item, idx) => (
              <li key={idx} className="flex items-start gap-3 p-3 bg-gray-900/50 rounded-xl border border-gray-800/80">
                <div className="mt-1 w-2 h-2 rounded-full bg-orange-500 shadow-[0_0_8px_#f97316]"></div>
                <span className="text-gray-300 font-medium leading-snug">{item}</span>
              </li>
            ))}
          </ul>
        </div>
        
        <div className="bg-gray-800/40 backdrop-blur-md p-8 rounded-2xl border border-gray-700/60 shadow-xl flex flex-col justify-between hover:border-gray-600 transition-all">
          <div>
            <h3 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" /></svg>
              THGNN Inference
            </h3>
            <div className="space-y-4 bg-gray-900/50 p-6 rounded-xl border border-gray-800/80">
              <div className="flex justify-between items-center border-b border-gray-700 pb-3">
                <span className="text-gray-400 font-medium">Threat Classification</span>
                <span className="font-extrabold text-red-500 bg-red-500/10 px-3 py-1 rounded-lg">HIGH</span>
              </div>
              <div className="flex justify-between items-center pt-1">
                <span className="text-gray-400 font-medium">Model Confidence</span>
                <span className="font-bold text-white text-lg">92%</span>
              </div>
            </div>
          </div>
          
          <div className="mt-6 text-right">
            <button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-bold py-3 px-6 rounded-xl text-sm transition-all shadow-lg shadow-blue-500/20 hover:shadow-blue-500/40 w-full sm:w-auto">
              Open XAI Reasoning Engine
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Investigations;
