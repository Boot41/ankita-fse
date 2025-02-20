import React, { useState } from 'react';
import { PlanCard } from '../components/PlanCard';
import { ComparisonTable } from '../components/ComparisonTable';
import { InsurancePlan } from '../types';

// Simulated available plans
const availablePlans: InsurancePlan[] = [
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
  },
  {
    id: '3',
    name: 'Premium Health Elite',
    price: 899,
    coverage: ['General Checkups', 'Emergency Care', 'Prescription Drugs', 'Dental', 'Vision', 'Mental Health', 'Alternative Medicine'],
    conditions: ['No waiting period', '100% coverage', 'Worldwide coverage'],
    description: 'Premium coverage with no compromises',
    rating: 4.9
  }
];

export function ComparePlans() {
  const [selectedPlans, setSelectedPlans] = useState<InsurancePlan[]>([]);

  const togglePlanSelection = (plan: InsurancePlan) => {
    if (selectedPlans.find(p => p.id === plan.id)) {
      setSelectedPlans(selectedPlans.filter(p => p.id !== plan.id));
    } else {
      setSelectedPlans([...selectedPlans, plan]);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Compare Insurance Plans</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {availablePlans.map((plan) => (
          <PlanCard
            key={plan.id}
            plan={plan}
            onSelect={togglePlanSelection}
            isSelected={selectedPlans.some(p => p.id === plan.id)}
          />
        ))}
      </div>

      {selectedPlans.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-bold text-gray-900 mb-4">Comparison</h3>
          <ComparisonTable plans={selectedPlans} />
        </div>
      )}
    </div>
  );
}