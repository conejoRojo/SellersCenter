import { Outlet, NavLink } from 'react-router-dom';
import { LayoutDashboard, Webhook, Users, Server, Shield } from 'lucide-react';

export default function AdminLayout() {
  const navigation = [
    { name: 'Sellers Overview', href: '/', icon: LayoutDashboard },
    { name: 'Integraciones & Webhooks', href: '/integrations', icon: Webhook },
    { name: 'Gestión de Usuarios', href: '/users', icon: Users },
    { name: 'Estado del Sistema', href: '/system', icon: Server },
  ];

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-gray-200 flex font-sans">
      {/* Sidebar */}
      <aside className="w-72 bg-[#121212] border-r border-[#222222] flex flex-col relative overflow-hidden">
        {/* Decorative Grid Background */}
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCI+PGRlZnM+PHBhdHRlcm4gaWQ9ImciIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTTAgNDBoNDBWMEgwem0yMCAyMGMtMS4xIDAtMi0uOS0yLTIyczktMiAyLTIgMiAuOSAyIDItLjkgMi0yIDJ6IiBmaWxsPSJyZ2JhKDI1NSwyNTUsMjU1LDAuMDMpIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZykiLz48L3N2Zz4=')] opacity-30 pointer-events-none"></div>
        
        <div className="p-8 relative z-10">
          <div className="flex items-center space-x-3">
            <Shield className="w-8 h-8 text-amber-500" />
            <h1 className="text-2xl font-black tracking-tight text-white">
              Aper Admin
            </h1>
          </div>
          <p className="text-xs text-amber-500/80 mt-2 font-mono uppercase tracking-widest pl-11">Superuser Access</p>
        </div>
        
        <nav className="flex-1 px-4 space-y-1 relative z-10 mt-6">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center px-4 py-3.5 rounded-xl transition-all duration-300 group ${
                  isActive
                    ? 'bg-gradient-to-r from-amber-500/10 to-orange-500/5 text-amber-400 border border-amber-500/20 shadow-[0_0_20px_rgba(245,158,11,0.05)]'
                    : 'text-gray-400 hover:bg-[#1A1A1A] hover:text-gray-200'
                }`
              }
            >
              <item.icon className={`w-5 h-5 mr-4 transition-transform duration-300 ${
                'group-hover:scale-110 group-active:scale-95'
              }`} />
              <span className="font-semibold text-sm tracking-wide">{item.name}</span>
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        {/* Glow Effects */}
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-amber-500/5 blur-[120px] rounded-full pointer-events-none"></div>

        {/* Topbar */}
        <header className="h-20 flex items-center justify-between px-10 border-b border-[#222222] bg-[#0A0A0A]/80 backdrop-blur-xl sticky top-0 z-20">
          <h2 className="text-lg font-bold text-gray-300 tracking-wide">Sync Engine Hub</h2>
          <div className="flex items-center space-x-4">
            <div className="flex flex-col items-end mr-3">
              <span className="text-sm font-bold text-white">Administrador</span>
              <span className="text-xs text-gray-500 font-mono">ID: SUPER-001</span>
            </div>
            <div className="w-11 h-11 rounded-xl bg-[#1A1A1A] border border-[#333333] flex items-center justify-center hover:bg-[#222222] transition-colors cursor-pointer group">
              <span className="font-bold text-amber-500 tracking-wider group-hover:scale-110 transition-transform">AD</span>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto p-10 z-10">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
