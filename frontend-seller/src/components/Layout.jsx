import { Outlet, NavLink } from 'react-router-dom';
import { Home, Package, ShoppingCart, Settings, LogOut, Bell } from 'lucide-react';

export default function Layout() {
  const navigation = [
    { name: 'Dashboard', href: '/', icon: Home },
    { name: 'Catálogo', href: '/catalog', icon: Package },
    { name: 'Órdenes', href: '/orders', icon: ShoppingCart },
    { name: 'Configuración', href: '/settings', icon: Settings },
  ];

  return (
    <div className="min-h-screen bg-[#111111] text-white flex">
      {/* Sidebar */}
      <aside className="w-64 bg-[#1A1A1A] border-r border-[#2A2A2A] flex flex-col">
        <div className="p-6">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
            SellersCenter
          </h1>
          <p className="text-sm text-gray-500 mt-1">Portal de Sellers</p>
        </div>
        
        <nav className="flex-1 px-4 space-y-2 mt-4">
          {navigation.map((item) => (
            <NavLink
              key={item.name}
              to={item.href}
              className={({ isActive }) =>
                `flex items-center px-4 py-3 rounded-xl transition-all duration-200 group ${
                  isActive
                    ? 'bg-blue-600/10 text-blue-400 border border-blue-500/20 shadow-[0_0_15px_rgba(37,99,235,0.1)]'
                    : 'text-gray-400 hover:bg-[#222222] hover:text-white'
                }`
              }
            >
              <item.icon className="w-5 h-5 mr-3 transition-transform group-hover:scale-110" />
              <span className="font-medium">{item.name}</span>
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-[#2A2A2A]">
          <button className="flex items-center w-full px-4 py-3 text-gray-400 hover:text-white hover:bg-red-500/10 hover:border-red-500/20 border border-transparent rounded-xl transition-all group">
            <LogOut className="w-5 h-5 mr-3 group-hover:text-red-400" />
            <span className="font-medium group-hover:text-red-400">Cerrar Sesión</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Topbar */}
        <header className="h-20 flex items-center justify-between px-8 border-b border-[#2A2A2A] bg-[#111111]/80 backdrop-blur-md sticky top-0 z-10">
          <h2 className="text-xl font-semibold tracking-tight text-gray-100">Panel de Control</h2>
          <div className="flex items-center space-x-6">
            <button className="relative p-2 text-gray-400 hover:text-white transition-colors">
              <Bell className="w-6 h-6" />
              <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-blue-500 rounded-full border-2 border-[#111111]"></span>
            </button>
            <div className="flex items-center space-x-3 pl-6 border-l border-[#2A2A2A]">
              <div className="flex flex-col items-end">
                <span className="text-sm font-medium text-white">Tienda Alpha</span>
                <span className="text-xs text-green-400 font-medium">Activo</span>
              </div>
              <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-500 flex items-center justify-center shadow-lg shadow-indigo-500/20">
                <span className="font-bold text-white tracking-wider">TA</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="flex-1 overflow-auto p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
