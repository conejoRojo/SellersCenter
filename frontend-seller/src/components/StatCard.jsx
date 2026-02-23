import React from 'react';

export default function StatCard({ title, value, change, icon: Icon, trend }) {
  const isPositive = trend === 'up';
  
  return (
    <div className="bg-[#1A1A1A] rounded-2xl p-6 border border-[#2A2A2A] shadow-xl hover:border-[#3A3A3A] transition-all duration-300 group">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-gray-400 font-medium tracking-wide text-sm">{title}</h3>
        <div className="p-3 bg-[#222222] rounded-xl group-hover:bg-blue-600/10 group-hover:text-blue-500 transition-colors">
          <Icon className="w-5 h-5" />
        </div>
      </div>
      
      <div className="flex items-end space-x-4">
        <h2 className="text-3xl font-bold text-white tracking-tight">{value}</h2>
        {change && (
          <span className={`flex items-center text-sm font-semibold pb-1 ${isPositive ? 'text-green-400' : 'text-red-400'}`}>
            {isPositive ? '↑' : '↓'} {change}
          </span>
        )}
      </div>
      
      <div className="mt-4 w-full bg-[#222222] h-1.5 rounded-full overflow-hidden">
        <div 
          className="bg-gradient-to-r from-blue-500 to-indigo-500 h-full rounded-full" 
          style={{ width: '70%' }}
        />
      </div>
    </div>
  );
}
