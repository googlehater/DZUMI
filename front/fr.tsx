import React, { useEffect, useState } from "react";

// Minimal pleasant frontend for Orders/Items/Users
// - Uses fetch to talk to the API endpoints assumed in backend
// - Tailwind classes used for styling (no imports required if your project already has Tailwind)
// - Default export a React component

export default function App() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(0);
  const [limit, setLimit] = useState(10);
  const [newOrder, setNewOrder] = useState({ user_id: "", object_id: "", system_type_id: "", description: "", comment: "" });
  const [error, setError] = useState(null);

  const API_BASE = "/api/v1";

  useEffect(() => {
    fetchOrders();
  }, [page, limit]);

  async function fetchOrders() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/orders?skip=${page * limit}&limit=${limit}`);
      if (!res.ok) throw new Error(`Ошибка: ${res.status}`);
      const data = await res.json();
      setOrders(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function createOrder(e) {
    e.preventDefault();
    setError(null);
    try {
      const payload = {
        user_id: Number(newOrder.user_id),
        object_id: Number(newOrder.object_id),
        system_type_id: Number(newOrder.system_type_id),
        description: newOrder.description,
        comment: newOrder.comment || undefined,
      };

      const res = await fetch(`${API_BASE}/orders/order`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const text = await res.text();
        throw new Error(`${res.status} ${text}`);
      }
      // clear and refresh
      setNewOrder({ user_id: "", object_id: "", system_type_id: "", description: "", comment: "" });
      fetchOrders();
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 p-6 font-sans">
      <div className="max-w-5xl mx-auto">
        <header className="mb-6">
          <h1 className="text-3xl font-semibold">Панель заказов</h1>
          <p className="text-sm text-slate-600">Минимальный фронтенд для управления заказами и добавления товаров</p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-4 rounded-2xl shadow-sm">
            <h2 className="text-lg font-medium mb-3">Создать заказ</h2>
            <form onSubmit={createOrder} className="space-y-3">
              <div>
                <label className="block text-sm text-slate-700">User ID</label>
                <input value={newOrder.user_id} onChange={(e)=>setNewOrder({...newOrder, user_id:e.target.value})} className="mt-1 block w-full rounded-lg border p-2" placeholder="Напр. 1" />
              </div>
              <div>
                <label className="block text-sm text-slate-700">Object ID</label>
                <input value={newOrder.object_id} onChange={(e)=>setNewOrder({...newOrder, object_id:e.target.value})} className="mt-1 block w-full rounded-lg border p-2" placeholder="Напр. 10" />
              </div>
              <div>
                <label className="block text-sm text-slate-700">System Type ID</label>
                <input value={newOrder.system_type_id} onChange={(e)=>setNewOrder({...newOrder, system_type_id:e.target.value})} className="mt-1 block w-full rounded-lg border p-2" placeholder="Напр. 2" />
              </div>
              <div>
                <label className="block text-sm text-slate-700">Описание</label>
                <textarea value={newOrder.description} onChange={(e)=>setNewOrder({...newOrder, description:e.target.value})} className="mt-1 block w-full rounded-lg border p-2" rows={3} />
              </div>
              <div>
                <label className="block text-sm text-slate-700">Комментарий (необязательно)</label>
                <input value={newOrder.comment} onChange={(e)=>setNewOrder({...newOrder, comment:e.target.value})} className="mt-1 block w-full rounded-lg border p-2" />
              </div>
              <div className="flex gap-2">
                <button type="submit" className="px-4 py-2 rounded-xl bg-indigo-600 text-white">Создать</button>
                <button type="button" onClick={()=>setNewOrder({ user_id: "", object_id: "", system_type_id: "", description: "", comment: "" })} className="px-4 py-2 rounded-xl border">Сброс</button>
              </div>
            </form>
            {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
          </div>

          <div className="bg-white p-4 rounded-2xl shadow-sm">
            <h2 className="text-lg font-medium mb-3">Список заявок</h2>

            <div className="flex items-center gap-2 mb-3">
              <label className="text-sm">Страницы:</label>
              <button onClick={()=>setPage(Math.max(0,page-1))} className="px-3 py-1 rounded-md border">◀</button>
              <span className="px-2">{page + 1}</span>
              <button onClick={()=>setPage(page+1)} className="px-3 py-1 rounded-md border">▶</button>
              <select value={limit} onChange={(e)=>{setLimit(Number(e.target.value)); setPage(0);}} className="ml-auto rounded-md border p-1">
                <option value={5}>5</option>
                <option value={10}>10</option>
                <option value={25}>25</option>
              </select>
            </div>

            {loading ? <div className="text-sm text-slate-500">Загрузка...</div> : (
              <ul className="space-y-3">
                {orders.length === 0 && <li className="text-sm text-slate-500">Нет заявок</li>}
                {orders.map(o => (
                  <li key={o.id} className="p-3 border rounded-lg">
                    <div className="flex justify-between items-start gap-4">
                      <div>
                        <div className="text-sm font-semibold">#{o.id} — {o.order_status || '—'}</div>
                        <div className="text-xs text-slate-600">Пользователь: {o.user_id} · Объект: {o.object_id} · Сумма: {o.total_price ?? '—'}</div>
                        <div className="mt-2 text-sm">{o.description}</div>
                      </div>
                      <div className="text-right text-xs text-slate-500">Приоритет: {o.priority ?? '—'}</div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>

        <footer className="mt-6 text-sm text-slate-500">Простой интерфейс — подключай API и расширяй по необходимости.</footer>
      </div>
    </div>
  );
}
