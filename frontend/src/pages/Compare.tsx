import React, { useState } from 'react';
import { Check, X, ArrowRight } from 'lucide-react';

const Compare = () => {
  const plans = [
    {
      id: 1,
      name: 'Basic Coverage',
      price: '$99',
      features: {
        'Personal Liability': true,
        'Property Damage': true,
        'Medical Payments': true,
        '24/7 Support': true,
        'Family Protection': false,
        'Child Education': false,
        'Travel Insurance': false,
        'Worldwide Coverage': false,
        'Premium Healthcare': false,
        'Investment Protection': false,
        'Retirement Benefits': false
      }
    },
    {
      id: 2,
      name: 'Family Plus',
      price: '$199',
      features: {
        'Personal Liability': true,
        'Property Damage': true,
        'Medical Payments': true,
        '24/7 Support': true,
        'Family Protection': true,
        'Child Education': true,
        'Travel Insurance': true,
        'Worldwide Coverage': false,
        'Premium Healthcare': false,
        'Investment Protection': false,
        'Retirement Benefits': false
      }
    },
    {
      id: 3,
      name: 'Premium Protection',
      price: '$299',
      features: {
        'Personal Liability': true,
        'Property Damage': true,
        'Medical Payments': true,
        '24/7 Support': true,
        'Family Protection': true,
        'Child Education': true,
        'Travel Insurance': true,
        'Worldwide Coverage': true,
        'Premium Healthcare': true,
        'Investment Protection': true,
        'Retirement Benefits': true
      }
    }
  ];

  const [selectedPlans, setSelectedPlans] = useState([plans[0], plans[1]]);

  const addPlan = () => {
    if (selectedPlans.length < 3) {
      const remainingPlans = plans.filter(plan => !selectedPlans.includes(plan));
      if (remainingPlans.length > 0) {
        setSelectedPlans([...selectedPlans, remainingPlans[0]]);
      }
    }
  };

  const removePlan = (planId: number) => {
    if (selectedPlans.length > 2) {
      setSelectedPlans(selectedPlans.filter(plan => plan.id !== planId));
    }
  };

  const changePlan = (oldPlanId: number, newPlanId: number) => {
    const newPlan = plans.find(plan => plan.id === newPlanId);
    if (newPlan) {
      setSelectedPlans(selectedPlans.map(plan => 
        plan.id === oldPlanId ? newPlan : plan
      ));
    }
  };

  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold text-gray-900">Compare Insurance Plans</h1>
          <p className="mt-4 text-lg text-gray-600">
            Compare our insurance plans side by side to find the perfect coverage for you
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          {/* Plans Header */}
          <div className="grid grid-cols-[200px_1fr] border-b">
            <div className="p-6 bg-gray-50"></div>
            <div className="grid" style={{ gridTemplateColumns: `repeat(${selectedPlans.length}, 1fr)` }}>
              {selectedPlans.map((plan) => (
                <div key={plan.id} className="p-6 border-l">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{plan.name}</h3>
                      <p className="text-2xl font-bold text-blue-600 mt-2">{plan.price}</p>
                      <p className="text-sm text-gray-500">per month</p>
                    </div>
                    {selectedPlans.length > 2 && (
                      <button
                        onClick={() => removePlan(plan.id)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        <X className="h-5 w-5" />
                      </button>
                    )}
                  </div>
                  <select
                    value={plan.id}
                    onChange={(e) => changePlan(plan.id, Number(e.target.value))}
                    className="mt-4 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                  >
                    {plans.map((p) => (
                      <option key={p.id} value={p.id} disabled={selectedPlans.some(sp => sp.id === p.id && sp.id !== plan.id)}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                </div>
              ))}
            </div>
          </div>

          {/* Features Comparison */}
          <div className="grid grid-cols-[200px_1fr]">
            <div className="bg-gray-50">
              {Object.keys(plans[0].features).map((feature) => (
                <div key={feature} className="p-6 border-b">
                  <span className="font-medium text-gray-900">{feature}</span>
                </div>
              ))}
            </div>
            <div className="grid" style={{ gridTemplateColumns: `repeat(${selectedPlans.length}, 1fr)` }}>
              {selectedPlans.map((plan) => (
                <div key={plan.id} className="border-l">
                  {Object.entries(plan.features).map(([feature, included]) => (
                    <div key={feature} className="p-6 border-b flex justify-center">
                      {included ? (
                        <Check data-testid="feature-included" className="h-6 w-6 text-green-500" />
                      ) : (
                        <X data-testid="feature-not-included" className="h-6 w-6 text-red-500" />
                      )}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Add Plan Button */}
        {selectedPlans.length < 3 && (
          <div className="mt-8 text-center">
            <button
              onClick={addPlan}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Add Another Plan <ArrowRight className="ml-2 h-5 w-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Compare;