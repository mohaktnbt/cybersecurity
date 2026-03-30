export default function DashboardPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6 border">
          <h3 className="text-sm font-medium text-gray-500">Active Scans</h3>
          <p className="text-3xl font-bold mt-2">0</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 border">
          <h3 className="text-sm font-medium text-gray-500">Total Findings</h3>
          <p className="text-3xl font-bold mt-2">0</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 border">
          <h3 className="text-sm font-medium text-gray-500">Risk Score</h3>
          <p className="text-3xl font-bold mt-2 text-green-600">A+</p>
        </div>
      </div>
      <p className="mt-8 text-gray-500">
        Dashboard implementation coming in Phase 3.
      </p>
    </div>
  );
}
