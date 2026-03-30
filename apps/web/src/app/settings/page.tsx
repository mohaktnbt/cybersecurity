export default function SettingsPage() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Settings</h1>
      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">Organization</h2>
          <p className="text-gray-500">Organization settings coming in Phase 3.</p>
        </div>
        <div className="bg-white rounded-lg shadow border p-6">
          <h2 className="text-xl font-semibold mb-4">API Keys</h2>
          <p className="text-gray-500">API key management coming in Phase 3.</p>
        </div>
      </div>
    </div>
  );
}
