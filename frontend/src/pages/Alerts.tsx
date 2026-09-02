import React from 'react';

const mockAlerts = [
  { id: 'A-1001', user: 'U1234', severity: 'CRITICAL', category: 'USB Misuse', status: 'OPEN', time: '10 mins ago' },
  { id: 'A-1002', user: 'U992', severity: 'HIGH', category: 'Data Exfiltration', status: 'OPEN', time: '1 hr ago' },
  { id: 'A-1003', user: 'U444', severity: 'MEDIUM', category: 'Abnormal Login', status: 'RESOLVED', time: '2 hrs ago' },
];

const Alerts: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold text-white">Alert Management</h1>
        <button className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white text-sm font-semibold">
          Auto-Assign Unresolved
        </button>
      </div>

      <div className="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-700">
          <thead className="bg-gray-900">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Alert ID</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Severity</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">User</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Time</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-400 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-gray-800 divide-y divide-gray-700">
            {mockAlerts.map(alert => (
              <tr key={alert.id} className="hover:bg-gray-750">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{alert.id}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                    ${alert.severity === 'CRITICAL' ? 'bg-red-900 text-red-200' : 
                      alert.severity === 'HIGH' ? 'bg-orange-900 text-orange-200' : 'bg-yellow-900 text-yellow-200'}`}>
                    {alert.severity}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-400 font-medium">{alert.user}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{alert.category}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-300">{alert.status}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-400">{alert.time}</td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium space-x-2">
                  <button className="text-blue-400 hover:text-blue-300">Investigate</button>
                  {alert.status === 'OPEN' && (
                    <button className="text-green-400 hover:text-green-300">Resolve</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Alerts;
