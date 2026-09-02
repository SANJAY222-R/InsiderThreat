import React from 'react';
import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export const MainLayout: React.FC = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItemClass = (path: string) => 
    `block py-3 px-4 rounded-xl transition-all duration-300 ${location.pathname === path ? 'bg-gradient-to-r from-blue-600/40 to-purple-600/40 border border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.3)] text-white' : 'text-gray-400 hover:bg-gray-800/50 hover:text-white hover:border-gray-700 border border-transparent'}`;

  return (
    <div className="flex h-screen bg-[#0B0F19] text-gray-200 overflow-hidden font-sans relative">
      {/* Subtle Background Glows */}
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      {/* Sidebar - Glassmorphic */}
      <aside className="w-72 bg-gray-900/60 backdrop-blur-xl flex flex-col border-r border-gray-800/60 z-10">
        <div className="p-6 flex items-center gap-3 border-b border-gray-800/60">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
            <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" /></svg>
          </div>
          <h1 className="text-xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400 tracking-wide">SOC Nexus</h1>
        </div>
        <nav className="flex-1 p-4 space-y-3 mt-4">
          <Link to="/" className={navItemClass('/')}>Dashboard</Link>
          <Link to="/investigations" className={navItemClass('/investigations')}>Investigations</Link>
          <Link to="/graph" className={navItemClass('/graph')}>Enterprise Graph</Link>
          <Link to="/xai" className={navItemClass('/xai')}>Explainable AI</Link>
          <Link to="/alerts" className={navItemClass('/alerts')}>Alerts</Link>
        </nav>
        <div className="p-6 border-t border-gray-800/60">
          <button onClick={handleLogout} className="w-full py-3 bg-gray-800/80 hover:bg-red-600/20 border border-gray-700 hover:border-red-500/50 hover:text-red-400 text-gray-300 rounded-xl text-sm font-semibold transition-all duration-300 shadow-md">
            Logout Session
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative z-10">
        {/* Top Navbar */}
        <header className="h-20 bg-gray-900/40 backdrop-blur-md border-b border-gray-800/60 flex items-center justify-between px-8">
          <div className="flex-1 max-w-2xl relative group">
            <div className="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none">
               <svg className="w-5 h-5 text-gray-500 group-focus-within:text-blue-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <input 
              type="text" 
              placeholder="Search users, IPs, assets, or risk signatures..." 
              className="w-full bg-gray-900/80 border border-gray-700/80 rounded-2xl pl-12 pr-4 py-2.5 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-blue-500/70 focus:ring-1 focus:ring-blue-500/50 transition-all shadow-inner"
            />
          </div>
          <div className="flex items-center space-x-6">
            <button className="relative p-2 text-gray-400 hover:text-blue-400 transition-colors">
              <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(239,68,68,0.8)]"></span>
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
            </button>
            <div className="flex items-center gap-3 pl-6 border-l border-gray-800">
              <div className="w-10 h-10 bg-gradient-to-br from-gray-700 to-gray-800 border border-gray-600 rounded-full flex items-center justify-center text-sm font-bold shadow-lg">
                SA
              </div>
              <div className="hidden md:block">
                <p className="text-sm font-semibold text-gray-200">System Admin</p>
                <p className="text-xs text-gray-500">Tier 3 Analyst</p>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-8 pt-10 pb-20">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
