import React from 'react';
import { Activity, FileText, Bell, Settings } from 'lucide-react';

const Dashboard = () => {
  const recentClaims = [
    { id: 1, type: 'Medical', status: 'Pending', amount: '$500', date: '2024-03-15' },
    { id: 2, type: 'Property', status: 'Approved', amount: '$1,200', date: '2024-03-10' },
    { id: 3, type: 'Auto', status: 'Under Review', amount: '$800', date: '2024-03-05' },
  ];

  const notifications = [
    { id: 1, message: 'Your claim has been approved', date: '1 hour ago' },
    { id: 2, message: 'Premium payment due in 5 days', date: '3 hours ago' },
    { id: 3, message: 'New policy document available', date: '1 day ago' },
  ];

  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">My Dashboard</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Active Policy Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Active Policy</h2>
              <FileText className="h-6 w-6 text-blue-600" />
            </div>
            <div className="space-y-2">
              <p className="text-gray-600">Policy Number: #12345678</p>
              <p className="text-gray-600">Type: Family Plus</p>
              <p className="text-gray-600">Status: Active</p>
              <p className="text-gray-600">Next Payment: April 15, 2024</p>
            </div>
          </div>

          {/* Recent Claims */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Recent Claims</h2>
              <Activity className="h-6 w-6 text-blue-600" />
            </div>
            <div className="space-y-4">
              {recentClaims.map((claim) => (
                <div key={claim.id} className="border-b pb-2 last:border-0">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{claim.type}</span>
                    <span className="text-sm text-gray-500">{claim.date}</span>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-sm text-gray-600">{claim.status}</span>
                    <span className="text-sm font-medium">{claim.amount}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Notifications */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Notifications</h2>
              <Bell className="h-6 w-6 text-blue-600" />
            </div>
            <div className="space-y-4">
              {notifications.map((notification) => (
                <div key={notification.id} className="border-b pb-2 last:border-0">
                  <p className="text-gray-700">{notification.message}</p>
                  <p className="text-sm text-gray-500 mt-1">{notification.date}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold text-gray-900">Quick Actions</h2>
            <Settings className="h-6 w-6 text-blue-600" />
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button className="p-4 text-center border rounded-lg hover:bg-gray-50">
              File a Claim
            </button>
            <button className="p-4 text-center border rounded-lg hover:bg-gray-50">
              View Policy Details
            </button>
            <button className="p-4 text-center border rounded-lg hover:bg-gray-50">
              Make a Payment
            </button>
            <button className="p-4 text-center border rounded-lg hover:bg-gray-50">
              Contact Support
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;