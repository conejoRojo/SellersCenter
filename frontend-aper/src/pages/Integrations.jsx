import { Webhook, RefreshCw, Database } from 'lucide-react';

export default function Integrations() {
  return (
    <div className="space-y-6 animate-in fade-in duration-700">
      <div>
        <h1 className="text-3xl font-black text-white tracking-tight">Integraciones y Webhooks</h1>
        <p className="text-gray-400 mt-2 text-sm font-medium">Panel general del motor asíncrono y colas SQS del backend.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-10">
        <div className="bg-[#121212] rounded-2xl border border-blue-500/20 shadow-[-10px_10px_30px_rgba(59,130,246,0.05)] p-8">
          <div className="flex items-center mb-6">
            <div className="p-3 bg-blue-500/10 rounded-xl mr-4">
              <Webhook className="w-8 h-8 text-blue-500" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Ingesta Webhooks</h2>
              <p className="text-xs text-blue-400/80 font-mono mt-1">Status: OK • 420 req/s</p>
            </div>
          </div>
          <div className="space-y-4">
            <div className="bg-[#0A0A0A] rounded-xl p-4 border border-[#222222] flex justify-between items-center">
              <span className="text-sm font-bold text-gray-400 uppercase tracking-widest">PrestaShop Canal A</span>
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            </div>
            <div className="bg-[#0A0A0A] rounded-xl p-4 border border-[#222222] flex justify-between items-center">
              <span className="text-sm font-bold text-gray-400 uppercase tracking-widest">PrestaShop Canal B</span>
              <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            </div>
          </div>
        </div>

        <div className="bg-[#121212] rounded-2xl border border-purple-500/20 shadow-[10px_10px_30px_rgba(168,85,247,0.05)] p-8">
          <div className="flex items-center mb-6">
            <div className="p-3 bg-purple-500/10 rounded-xl mr-4">
              <Database className="w-8 h-8 text-purple-500" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Cola de Procesamiento (SQS)</h2>
              <p className="text-xs text-purple-400/80 font-mono mt-1">Workers Activos: 12</p>
            </div>
          </div>
          <div className="flex flex-col items-center justify-center py-8">
            <RefreshCw className="w-16 h-16 text-[#222222] mb-4" />
            <p className="text-gray-500 font-medium text-center max-w-xs">
              Métricas de procesamiento en tiempo real disponibles en la Fase 12.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
