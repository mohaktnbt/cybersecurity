export default function TargetsPage() {
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">Targets</h1>
        <button className="bg-hexstrike-600 text-white px-4 py-2 rounded-lg hover:bg-hexstrike-700">
          Add Target
        </button>
      </div>
      <div className="bg-white rounded-lg shadow border p-12 text-center text-gray-500">
        No targets configured yet. Add your first target to start scanning.
      </div>
    </div>
  );
}
