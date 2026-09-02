import React from 'react';

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const mockTrendData = [
  { time: '10:00', risk: 20 },
  { time: '11:00', risk: 22 },
  { time: '12:00', risk: 45 },
  { time: '13:00', risk: 85 }, // Spike
  { time: '14:00', risk: 60 },
];

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">Global Command Center</h1>
          <p className="text-gray-400 mt-1">Real-time threat monitoring powered by THGNN Intelligence.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
          </span>
          <span className="text-sm font-medium text-green-400">System Secure</span>
        </div>
      </div>
      
      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { label: 'Total Users Monitored', value: '1,248', color: 'text-blue-400', glow: 'shadow-blue-500/10' },
          { label: 'High Risk Entities', value: '12', color: 'text-red-500', glow: 'shadow-red-500/20', alert: true },
          { label: 'Active Incidents', value: '3', color: 'text-orange-400', glow: 'shadow-orange-500/20' },
          { label: 'Network Threat Level', value: '28.4', color: 'text-purple-400', glow: 'shadow-purple-500/10', suffix: '/100' },
        ].map((kpi, idx) => (
          <div key={idx} className={`bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 shadow-xl ${kpi.glow} relative overflow-hidden group hover:border-gray-600 transition-colors`}>
            {kpi.alert && <div className="absolute top-0 right-0 w-16 h-16 bg-red-500/20 blur-2xl rounded-full"></div>}
            <p className="text-sm font-medium text-gray-400 uppercase tracking-wider mb-2">{kpi.label}</p>
            <p className={`text-4xl font-extrabold ${kpi.color}`}>
              {kpi.value}
              {kpi.suffix && <span className="text-lg text-gray-500 ml-1">{kpi.suffix}</span>}
            </p>
          </div>
        ))}
      </div>

      {/* Charts Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 shadow-xl">
          <h2 className="text-lg font-bold text-gray-200 mb-6 flex items-center gap-2">
            <svg className="w-5 h-5 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" /></svg>
            Enterprise Risk Velocity
          </h2>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockTrendData}>
                <defs>
                  <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#EF4444" stopOpacity={0.8}/>
                    <stop offset="95%" stopColor="#EF4444" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" vertical={false} />
                <XAxis dataKey="time" stroke="#6B7280" tick={{fill: '#9CA3AF'}} tickLine={false} axisLine={false} />
                <YAxis stroke="#6B7280" tick={{fill: '#9CA3AF'}} tickLine={false} axisLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '12px', boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)' }} 
                  itemStyle={{ color: '#F3F4F6' }}
                />
                <Line type="monotone" dataKey="risk" stroke="#EF4444" strokeWidth={3} dot={{r: 4, fill: '#EF4444', strokeWidth: 2, stroke: '#111827'}} activeDot={{ r: 6, fill: '#EF4444', stroke: '#fff' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        <div className="bg-gray-800/40 backdrop-blur-md p-6 rounded-2xl border border-gray-700/60 shadow-xl flex flex-col">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-bold text-gray-200 flex items-center gap-2">
              <svg className="w-5 h-5 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
              Live Anomalies
            </h2>
            <button className="text-xs text-blue-400 hover:text-blue-300 font-medium">View All</button>
          </div>
          <ul className="space-y-4 flex-1 overflow-auto pr-2">
            {[
              { level: 'CRITICAL', user: 'U1234', msg: 'Anomalous USB data exfiltration pattern detected.', color: 'red' },
              { level: 'HIGH', user: 'U992', msg: 'After-hours bulk Active Directory query.', color: 'orange' },
              { level: 'LOW', user: 'SysAdmin', msg: 'Failed authentication from unknown subnet.', color: 'gray' },
              { level: 'MEDIUM', user: 'U441', msg: 'Access to restricted HR financial folders.', color: 'yellow' },
            ].map((alert, idx) => (
              <li key={idx} className={`p-4 rounded-xl border relative overflow-hidden group
                ${alert.color === 'red' ? 'bg-red-900/10 border-red-500/30 hover:border-red-500/50' : 
                  alert.color === 'orange' ? 'bg-orange-900/10 border-orange-500/30 hover:border-orange-500/50' : 
                  alert.color === 'yellow' ? 'bg-yellow-900/10 border-yellow-500/30 hover:border-yellow-500/50' :
                  'bg-gray-800/30 border-gray-700 hover:border-gray-600'} transition-all`}>
                {alert.color === 'red' && <div className="absolute left-0 top-0 bottom-0 w-1 bg-red-500 shadow-[0_0_8px_#EF4444]"></div>}
                <div className="flex items-center justify-between mb-1">
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-md 
                    ${alert.color === 'red' ? 'bg-red-500/20 text-red-400' : 
                      alert.color === 'orange' ? 'bg-orange-500/20 text-orange-400' : 
                      alert.color === 'yellow' ? 'bg-yellow-500/20 text-yellow-400' :
                      'bg-gray-700 text-gray-300'}`}>
                    {alert.level}
                  </span>
                  <span className="text-xs text-gray-500 font-mono">{alert.user}</span>
                </div>
                <p className="text-sm text-gray-300 mt-2 line-clamp-2">{alert.msg}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
