import React, { useState } from 'react';
import { UserForm } from '../components/UserForm';
import { PlanCard } from '../components/PlanCard';
import { UserFormData, InsurancePlan } from '../types';
import { Loader2 } from 'lucide-react';

// Simulated API response
const mockRecommendations: InsurancePlan[] = [
  {
    id: '1',
    name: 'Basic Care Plus',
    price: 299,
    coverage: ['General Checkups', 'Emergency Care', 'Prescription Drugs'],
    conditions: ['No waiting period', '80% coverage'],
    description: 'Affordable basic coverage for individuals',
    rating: 4.2
  },
  {
    id: '2',
    name: 'Family Shield Pro',
    price: 599,
    coverage: ['General Checkups', 'Emergency Care', 'Prescription Drugs', 'Dental', 'Vision'],
    conditions: ['30-day waiting period', '90% coverage'],
    description: 'Comprehensive coverage for families',
    rating: 4.8
  }
];

export function Home() {
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState<InsurancePlan[]>([]);

  const handleSubmit = async (data: UserFormData) => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setRecommendations(mockRecommendations);
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Find Your Perfect Health Insurance Plan
          </h2>
          <UserForm onSubmit={handleSubmit} />
        </div>

        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">
            Recommended Plans
          </h2>
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
            </div>
          ) : recommendations.length > 0 ? (
            <div className="space-y-6">
              {recommendations.map((plan) => (
                <PlanCard
                  key={plan.id}
                  plan={plan}
                  onSelect={() => {}}
                />
              ))}
            </div>
          ) : (
            <div className="bg-gray-50 rounded-lg p-6 text-center">
              <p className="text-gray-500">
                Fill out the form to get personalized recommendations
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}