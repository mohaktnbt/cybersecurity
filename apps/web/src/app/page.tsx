export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-6xl font-bold mb-4">
          <span className="text-hexstrike-500">Hex</span>Strike
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-Powered Autonomous Penetration Testing
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/dashboard"
            className="bg-hexstrike-600 text-white px-6 py-3 rounded-lg hover:bg-hexstrike-700 transition"
          >
            Go to Dashboard
          </a>
          <a
            href="/api/v1/health"
            className="border border-gray-300 px-6 py-3 rounded-lg hover:bg-gray-50 transition"
          >
            API Health
          </a>
        </div>
      </div>
    </main>
  );
}
