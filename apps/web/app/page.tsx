'use client';

import { FormEvent, useState } from 'react';

export default function HomePage() {
  const [prompt, setPrompt] = useState('Explain time dilation and then calculate how much proper time passes for a spacecraft traveling at 0.99c while one year passes for an Earth observer.');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setLoading(true);
    setResponse('');

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: prompt }),
    });

    const data = await res.json();
    setResponse(data.response || 'No response');
    setLoading(false);
  };

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-6xl p-8">
        <header className="mb-8 border-b border-slate-800 pb-6">
          <h1 className="text-4xl font-bold">OMNIA</h1>
          <p className="mt-2 text-slate-400">Universal Research Intelligence</p>
        </header>

        <div className="grid gap-6 lg:grid-cols-[1.4fr_0.6fr]">
          <section className="rounded-xl border border-slate-800 bg-slate-900 p-6">
            <form onSubmit={handleSubmit} className="space-y-4">
              <textarea
                className="min-h-[150px] w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm text-slate-100 outline-none ring-0"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
              />
              <button
                type="submit"
                disabled={loading}
                className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? 'Thinking...' : 'Send'}
              </button>
            </form>

            <div className="mt-8 rounded-lg border border-slate-800 bg-slate-950 p-4">
              <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-slate-400">Response</h2>
              <p className="whitespace-pre-wrap text-sm leading-7 text-slate-200">{response || 'Awaiting a message...'}</p>
            </div>
          </section>

          <aside className="space-y-4">
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
              <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">Activity</h3>
              <ul className="mt-3 space-y-2 text-sm text-slate-300">
                <li>Task created</li>
                <li>Model selected</li>
                <li>Tool execution logged</li>
              </ul>
            </div>
            <div className="rounded-xl border border-slate-800 bg-slate-900 p-4">
              <h3 className="text-sm font-semibold uppercase tracking-wide text-slate-400">Status</h3>
              <p className="mt-3 text-sm text-slate-300">Foundation online</p>
            </div>
          </aside>
        </div>
      </div>
    </main>
  );
}
