
export default function Orders() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold text-white tracking-tight">Gestión de Órdenes</h1>
        <p className="text-gray-400 mt-2">Administra y procesa los pedidos provenientes de todos tus canales.</p>
      </div>
      
      <div className="bg-[#1A1A1A] rounded-2xl border border-[#2A2A2A] p-12 flex flex-col items-center justify-center text-center">
        <div className="w-16 h-16 bg-[#222222] rounded-full flex items-center justify-center mb-4">
          <span className="text-2xl">📦</span>
        </div>
        <h3 className="text-xl font-medium text-white mb-2">Sección en Construcción</h3>
        <p className="text-gray-400 max-w-md">
          Próximamente podrás ver el detalle completo de los pedidos, imprimir etiquetas de envío y gestionar devoluciones desde aquí.
        </p>
      </div>
    </div>
  );
}
