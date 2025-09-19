"use client";

import { useState } from "react";

interface ParsedTicket {
  from?: string;
  to?: string;
  train?: string;
  wagon?: string;
  seat?: string;
  name?: string;
  type?: string;
  discount?: string;
  distance_km?: string;
}

export default function UploadPage() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ParsedTicket | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const form = new FormData();
      form.append("file", file);

      const resp = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/decode`, {
        method: "POST",
        body: form,
      });

      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();

      setResult(data.info?.parsed || null);
    } catch (err: any) {
      setError(err.message || "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-2xl mx-auto py-12 px-4 space-y-6">
      <h1 className="text-3xl font-bold">Upload Ticket</h1>
      <p className="text-neutral-500">Upload a ticket image and parse details</p>

      <input
        type="file"
        accept="image/*"
        onChange={handleUpload}
        className="block w-full text-sm file:mr-4 file:rounded-md file:border-0 file:bg-blue-600 file:px-4 file:py-2 file:text-white hover:file:bg-blue-700"
      />

      {loading && <p className="text-blue-500">Processing...</p>}

      {error && (
        <div className="rounded-md bg-red-900/30 border border-red-700 p-4 text-red-300">
          {error}
        </div>
      )}

      {result && (
        <div className="rounded-md bg-neutral-900 border border-neutral-800 p-4 space-y-2">
          <h2 className="text-xl font-semibold">Parsed Ticket</h2>
          <ul className="space-y-1 text-sm">
            {Object.entries(result).map(([k, v]) =>
              v ? (
                <li key={k}>
                  <span className="font-semibold capitalize">{k}:</span> {v}
                </li>
              ) : null
            )}
          </ul>
        </div>
      )}
    </main>
  );
}
