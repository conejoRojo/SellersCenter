import { Store, Activity, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Overview() {
  const tenants = [
    { id: 'T-001', name: 'Tienda Alpha (MK1)', status: 'active', syncRate: '99.8%', lastSync: 'Hace 2 min' },
    { id: 'T-002', name: 'Deportes Beta (MK2)', status: 'warning', syncRate: '94.2%', lastSync: 'Hace 15 min' },
    { id: 'T-003', name: 'Electro Gamma (MK3)', status: 'active', syncRate: '99.9%', lastSync: 'Hace 1 min' },
    { id: 'T-004', name: 'Moda Delta (MK1)', status: 'error', syncRate: '82.5%', lastSync: 'Hace 2 horas' },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-700">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-black text-white tracking-tight">Global Sellers Overview</h1>
          <p className="text-gray-400 mt-2 text-sm font-medium">Monitorización centralizada de todos los tenants conectados al Sync Engine.</p>
        </div>
        <button className="px-5 py-2.5 bg-amber-500 hover:bg-amber-400 text-black font-bold rounded-xl shadow-[0_0_20px_rgba(245,158,11,0.3)] transition-all">
          Añadir Seller
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-[#121212] rounded-2xl p-6 border border-[#222222] shadow-[0_8px_30px_rgb(0,0,0,0.5)] relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <Store className="w-24 h-24 text-amber-500" />
          </div>
          <h3 className="text-gray-400 font-bold text-sm uppercase tracking-wider mb-2">Total Tenants Activos</h3>
          <p className="text-4xl font-black text-white">124</p>
          <div className="mt-4 flex items-center text-sm font-semibold text-green-500">
            <span>+12 este mes</span>
          </div>
        </div>
        
        <div className="bg-[#121212] rounded-2xl p-6 border border-[#222222] shadow-[0_8px_30px_rgb(0,0,0,0.5)] relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
            <Activity className="w-24 h-24 text-blue-500" />
          </div>
          <h3 className="text-gray-400 font-bold text-sm uppercase tracking-wider mb-2">Transacciones (24h)</h3>
          <p className="text-4xl font-black text-white">45.2K</p>
          <div className="mt-4 flex items-center text-sm font-semibold text-blue-400">
            <span>99.9% Exitosas</span>
          </div>
        </div>

        <div className="bg-[#121212] rounded-2xl p-6 border border-red-500/30 shadow-[0_8px_30px_rgba(239,68,68,0.1)] relative overflow-hidden group">
          <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-40 transition-opacity">
            <AlertCircle className="w-24 h-24 text-red-500" />
          </div>
          <h3 className="text-red-400/80 font-bold text-sm uppercase tracking-wider mb-2">Alertas de Sincronización</h3>
          <p className="text-4xl font-black text-red-500">3</p>
          <div className="mt-4 flex items-center text-sm font-semibold text-red-500/80">
            <span>Requieren atención inmediata</span>
          </div>
        </div>
      </div>

      <div className="bg-[#121212] rounded-2xl border border-[#222222] shadow-2xl overflow-hidden">
        <div className="p-6 border-b border-[#222222] bg-[#0A0A0A]/50">
          <h3 className="text-lg font-bold text-gray-200">Estado Individual de Tenants</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="bg-[#0A0A0A] text-gray-500 text-xs font-bold uppercase tracking-widest border-b border-[#222222]">
                <th className="px-8 py-5">Tenant ID</th>
                <th className="px-8 py-5">Nombre Comercial</th>
                <th className="px-8 py-5">Salud Sync</th>
                <th className="px-8 py-5">Última Actividad</th>
                <th className="px-8 py-5 text-right">Acción</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#222222]">
              {tenants.map((t) => (
                <tr key={t.id} className="hover:bg-[#1A1A1A] transition-colors">
                  <td className="px-8 py-5 font-mono text-sm text-gray-400">{t.id}</td>
                  <td className="px-8 py-5 font-bold text-gray-200">{t.name}</td>
                  <td className="px-8 py-5">
                    <div className="flex items-center space-x-3">
                      {t.status === 'active' ? <CheckCircle2 className="w-5 h-5 text-green-500" /> : 
                       t.status === 'warning' ? <AlertCircle className="w-5 h-5 text-amber-500" /> : 
                       <AlertCircle className="w-5 h-5 text-red-500" />}
                      <span className={`font-mono text-sm font-bold ${
                        t.status === 'active' ? 'text-green-500' : 
                        t.status === 'warning' ? 'text-amber-500' : 'text-red-500'
                      }`}>{t.syncRate}</span>
                    </div>
                  </td>
                  <td className="px-8 py-5 text-sm text-gray-500 font-medium">{t.lastSync}</td>
                  <td className="px-8 py-5 text-right">
                    <button className="text-amber-500 hover:text-amber-400 font-bold text-sm tracking-wide transition-colors">
                      Inspeccionar Logs
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
