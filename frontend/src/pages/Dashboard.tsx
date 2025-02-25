import React, { useEffect, useState } from 'react';
import { Activity, FileText, Star } from 'lucide-react';
import { toast } from 'react-toastify';
import { getDashboardData, submitFeedback, type DashboardData } from '../services/dashboard';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getDashboardData();
        setDashboardData(data);
        setError(null);
      } catch (err: any) {
        setError(err.message);
        if (err.message.includes('401')) {
          navigate('/login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [navigate]);

  const handleFeedbackSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      await submitFeedback(rating, comment);
      setComment('');
      // Refresh dashboard data to show new feedback
      const data = await getDashboardData();
      setDashboardData(data);
      // Show success message
      toast.success('Feedback submitted successfully!');
    } catch (err: any) {
      toast.error(err.message || 'Failed to submit feedback');
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div data-testid="loading-spinner" className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
            <strong className="font-bold">Error! </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Welcome, {dashboardData?.user.name || 'User'}</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* User Profile Card */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">My Profile</h2>
              <FileText className="h-6 w-6 text-blue-600" />
            </div>
            <div className="space-y-2">
              <p className="text-gray-600">Age: {dashboardData?.user.age || 'Not set'}</p>
              <p className="text-gray-600">Budget: ${dashboardData?.user.budget || 'Not set'}</p>
              <p className="text-gray-600">Family Size: {dashboardData?.user.family_size || 'Not set'}</p>
              <p className="text-gray-600">Medical History: {dashboardData?.user.medical_history || 'None'}</p>
            </div>
          </div>

          {/* Recommended Plans */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Recommended Plans</h2>
              <Activity className="h-6 w-6 text-blue-600" />
            </div>
            <div className="space-y-4">
              {(dashboardData?.recommendations || []).map((plan) => (
                <div key={plan.id} className="border-b pb-2 last:border-0">
                  <div className="flex justify-between items-center">
                    <span className="font-medium">{plan.name}</span>
                    <span className="text-sm text-gray-500">${plan.price_per_month}/month</span>
                  </div>
                  <div className="flex justify-between items-center mt-1">
                    <span className="text-sm text-gray-500">{plan.coverage}</span>
                    <span className="text-sm font-medium text-green-600">
                      {Math.round(plan.suitability_score * 100)}% Match
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Feedback Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">Your Feedback</h2>
              <Star className="h-6 w-6 text-blue-600" />
            </div>
            <form onSubmit={handleFeedbackSubmit} className="space-y-4">
              <div>
                <label htmlFor="rating" className="block text-sm font-medium text-gray-700">Rating</label>
                <select
                  id="rating"
                  value={rating}
                  onChange={(e) => setRating(Number(e.target.value))}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                >
                  {[5, 4, 3, 2, 1].map((value) => (
                    <option key={value} value={value}>{value} Stars</option>
                  ))}
                </select>
              </div>
              <div>
                <label htmlFor="comments" className="block text-sm font-medium text-gray-700">Comments</label>
                <textarea
                  id="comments"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  rows={3}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  placeholder="Share your experience..."
                />
              </div>
              <button
                type="submit"
                disabled={submitting}
                className={`w-full py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${submitting ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
              >
                {submitting ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></div>
                    Submitting...
                  </div>
                ) : (
                  'Submit Feedback'
                )}
              </button>
            </form>
            <div className="mt-6 space-y-4">
              <h3 className="font-medium text-gray-900">Recent Feedback</h3>
              {(dashboardData?.feedback || []).map((item) => (
                <div key={item.id} className="border-b pb-2 last:border-0">
                  <div className="flex items-center space-x-1">
                    {Array.from({ length: item.rating }).map((_, i) => (
                      <Star key={i} className="h-4 w-4 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-sm text-gray-600 mt-1">{item.comments}</p>
                  <p className="text-xs text-gray-500 mt-1">{new Date(item.created_at).toLocaleDateString()}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;