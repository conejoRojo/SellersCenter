import React from 'react';
import { Search, Plus, Filter } from 'lucide-react';

export default function Catalog() {
  const products = [
    { id: 1, sku: 'SKU-001', name: 'Zapatillas Deportivas X1', stock: 45, price: '$120.00', status: 'Sincronizado' },
    { id: 2, sku: 'SKU-002', name: 'Auriculares Inalámbricos Pro', stock: 12, price: '$89.99', status: 'Error' },
    { id: 3, sku: 'SKU-003', name: 'Mochila Urbana Impermeable', stock: 89, price: '$55.00', status: 'Sincronizado' },
    { id: 4, sku: 'SKU-004', name: 'Smartwatch Series 5', stock: 0, price: '$199.00', status: 'Agotado' },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white tracking-tight">Catálogo de Productos</h1>
          <p className="text-gray-400 mt-2">Gestiona tu inventario centralizado para todos los canales.</p>
        </div>
        <button className="flex items-center px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-xl shadow-[0_0_20px_rgba(79,70,229,0.3)] transition-all">
          <Plus className="w-5 h-5 mr-2" />
          Nuevo Producto
        </button>
      </div>

      <div className="bg-[#1A1A1A] rounded-2xl border border-[#2A2A2A] p-4 flex gap-4">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input 
            type="text" 
            placeholder="Buscar por nombre, SKU o categoría..." 
            className="w-full bg-[#111111] border border-[#333333] rounded-xl py-2.5 pl-10 pr-4 text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all placeholder:text-gray-600"
          />
        </div>
        <button className="flex items-center px-4 py-2.5 bg-[#222222] hover:bg-[#333333] border border-[#333333] text-white font-medium rounded-xl transition-all">
          <Filter className="w-5 h-5 mr-2 text-gray-400" />
          Filtros
        </button>
      </div>

      <div className="bg-[#1A1A1A] rounded-2xl border border-[#2A2A2A] shadow-xl overflow-hidden">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-[#111111] text-gray-400 text-xs uppercase tracking-wider">
              <th className="px-6 py-4 font-medium">Producto</th>
              <th className="px-6 py-4 font-medium">SKU</th>
              <th className="px-6 py-4 font-medium">Stock</th>
              <th className="px-6 py-4 font-medium">Precio Base</th>
              <th className="px-6 py-4 font-medium">Sincronización</th>
              <th className="px-6 py-4 font-medium text-right">Acciones</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#2A2A2A]">
            {products.map((product) => (
              <tr key={product.id} className="hover:bg-[#222222] transition-colors group">
                <td className="px-6 py-4">
                  <div className="flex items-center">
                    <div className="w-10 h-10 rounded-lg bg-[#2A2A2A] border border-[#333333] flex-shrink-0"></div>
                    <div className="ml-4">
                      <div className="text-sm font-medium text-white group-hover:text-indigo-400 transition-colors">{product.name}</div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-400 font-mono text-sm">{product.sku}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`text-sm font-semibold ${product.stock > 0 ? 'text-white' : 'text-red-400'}`}>
                    {product.stock} uns.
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-gray-300 font-medium">{product.price}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${product.status === 'Sincronizado' ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 
                      product.status === 'Error' ? 'bg-red-500/10 text-red-400 border border-red-500/20' : 
                      'bg-orange-500/10 text-orange-400 border border-orange-500/20'}`}>
                    {product.status}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button className="text-indigo-400 hover:text-indigo-300 transition-colors">Editar</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
