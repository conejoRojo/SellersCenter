import React from 'react';
import { DollarSign, ShoppingBag, PackageSearch, Activity } from 'lucide-react';
import StatCard from '../components/StatCard';

export default function Dashboard() {
  const stats = [
    { title: 'Ventas Totales (Mes)', value: '$124,500', change: '12%', icon: DollarSign, trend: 'up' },
    { title: 'Órdenes Nuevas', value: '842', change: '5%', icon: ShoppingBag, trend: 'up' },
    { title: 'Productos Activos', value: '1,204', change: '2%', icon: PackageSearch, trend: 'up' },
    { title: 'Tasa de Conversión', value: '4.3%', change: '1.2%', icon: Activity, trend: 'down' },
  ];

  const recentOrders = [
    { id: '#ORD-0921', customer: 'Juan Pérez', items: 3, total: '$450.00', status: 'Pendiente', channel: 'PrestaShop (Canal A)' },
    { id: '#ORD-0920', customer: 'María Gómez', items: 1, total: '$120.00', status: 'Enviado', channel: 'PrestaShop (Canal B)' },
    { id: '#ORD-0919', customer: 'Carlos López', items: 5, total: '$890.00', status: 'Pagado', channel: 'PrestaShop (Canal A)' },
    { id: '#ORD-0918', customer: 'Ana Torres', items: 2, total: '$340.00', status: 'Entregado', channel: 'PrestaShop (Canal C)' },
  ];

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Bienvenido, Tienda Alpha</h1>
          <p className="text-gray-400 mt-2">Aquí tienes un resumen de tu rendimiento en todos los canales de venta.</p>
        </div>
        <button className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white font-medium rounded-xl shadow-[0_0_20px_rgba(37,99,235,0.3)] hover:shadow-[0_0_25px_rgba(37,99,235,0.5)] transition-all">
          Descargar Reporte
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => (
          <StatCard key={i} {...stat} />
        ))}
      </div>

      <div className="bg-[#1A1A1A] rounded-2xl border border-[#2A2A2A] shadow-xl overflow-hidden">
        <div className="p-6 border-b border-[#2A2A2A] flex justify-between items-center bg-[#181818]">
          <h3 className="text-xl font-semibold text-white">Órdenes Recientes</h3>
          <button className="text-blue-400 hover:text-blue-300 text-sm font-medium transition-colors">
            Ver todas →
          </button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-[#111111] text-gray-400 text-xs uppercase tracking-wider">
                <th className="px-6 py-4 font-medium">ID Órden</th>
                <th className="px-6 py-4 font-medium">Cliente</th>
                <th className="px-6 py-4 font-medium">Canal</th>
                <th className="px-6 py-4 font-medium">Total</th>
                <th className="px-6 py-4 font-medium">Estado</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#2A2A2A]">
              {recentOrders.map((order) => (
                <tr key={order.id} className="hover:bg-[#222222] transition-colors group">
                  <td className="px-6 py-4 whitespace-nowrap text-white font-medium group-hover:text-blue-400 transition-colors">
                    {order.id}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-300">{order.customer}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-400 text-sm">{order.channel}</td>
                  <td className="px-6 py-4 whitespace-nowrap text-gray-300 font-semibold">{order.total}</td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
                      ${order.status === 'Entregado' ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 
                        order.status === 'Pendiente' ? 'bg-yellow-500/10 text-yellow-400 border border-yellow-500/20' : 
                        order.status === 'Pagado' ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20' : 
                        'bg-gray-500/10 text-gray-400 border border-gray-500/20'}`}>
                      {order.status}
                    </span>
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
