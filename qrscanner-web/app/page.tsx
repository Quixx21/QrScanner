"use client";

import { useState, useRef } from "react";
import Webcam from "react-webcam";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [useCamera, setUseCamera] = useState(false);
  const webcamRef = useRef<Webcam>(null);

  const handleUpload = async (file: File) => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE}/decode`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setResult(data);
  };

  const handleCapture = async () => {
    if (!webcamRef.current) return;
    const imageSrc = webcamRef.current.getScreenshot();
    if (!imageSrc) return;

    const blob = await (await fetch(imageSrc)).blob();
    const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
    await handleUpload(file);
  };

  return (
    <main className="relative min-h-screen flex flex-col items-center justify-center text-white overflow-hidden">
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="sphere sphere-1" />
        <div className="sphere sphere-2" />
        <div className="sphere sphere-3" />
      </div>

      <motion.h1
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="text-5xl font-extrabold mb-12 tracking-wide"
      >
        QR Ticket Scanner
      </motion.h1>

      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="bg-gray-900/60 backdrop-blur-xl shadow-2xl rounded-2xl p-8 w-full max-w-lg text-center border border-gray-700"
      >
        {!useCamera ? (
          <>
            <input
              type="file"
              accept="image/*"
              className="hidden"
              id="file-input"
              onChange={(e) => {
                if (e.target.files?.[0]) handleUpload(e.target.files[0]);
              }}
            />
            <label
              htmlFor="file-input"
              className="block cursor-pointer bg-blue-600 px-6 py-3 rounded-lg hover:shadow-[0_0_20px_#3b82f6] transition mb-4"
            >
              Upload Ticket
            </label>

            <button
              onClick={() => setUseCamera(true)}
              className="w-full bg-green-600 px-6 py-3 rounded-lg hover:shadow-[0_0_20px_#22c55e] transition"
            >
              Open Camera
            </button>
          </>
        ) : (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center"
          >
            <Webcam
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="rounded-lg border-4 border-green-500 mb-4"
              videoConstraints={{ facingMode: "environment" }}
            />

            <div className="flex gap-4">
              <button
                onClick={handleCapture}
                className="bg-green-600 px-6 py-2 rounded-lg hover:shadow-[0_0_20px_#22c55e] transition"
              >
                Capture & Scan
              </button>
              <button
                onClick={() => setUseCamera(false)}
                className="bg-gray-600 px-6 py-2 rounded-lg hover:shadow-[0_0_20px_#9ca3af] transition"
              >
                Close Camera
              </button>
            </div>
          </motion.div>
        )}
      </motion.div>

      <AnimatePresence>
        {result?.info?.parsed && (
          <motion.div
            initial={{ y: 60, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 60, opacity: 0 }}
            transition={{ duration: 0.6 }}
            className="mt-12 bg-gray-900/70 backdrop-blur-xl shadow-2xl rounded-2xl p-8 w-full max-w-3xl border border-gray-700"
          >
            <h2 className="text-2xl font-semibold mb-6">Parsed Ticket</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
              {Object.entries(result.info.parsed).map(([key, value], idx) => (
                <motion.div
                  key={key}
                  initial={{ y: 30, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: idx * 0.1 }}
                  className="bg-gray-800/60 rounded-lg p-4 shadow-lg hover:shadow-[0_0_20px_rgba(255,255,255,0.2)] transition"
                >
                  <p className="text-sm uppercase text-gray-400">{key}</p>
                  <p className="text-lg font-bold">{String(value)}</p>
                </motion.div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </main>
  );
}
