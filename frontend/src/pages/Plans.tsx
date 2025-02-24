import React, { useState } from 'react';
import { Shield, Check } from 'lucide-react';

const Plans = () => {
  const [selectedPlan, setSelectedPlan] = useState(null);

  const plans = [
    {
      id: 1,
      name: 'Basic Coverage',
      price: '$99',
      features: [
        'Personal liability coverage',
        'Property damage protection',
        'Medical payments coverage',
        '24/7 customer support'
      ]
    },
    {
      id: 2,
      name: 'Family Plus',
      price: '$199',
      features: [
        'All Basic Coverage features',
        'Extended family protection',
        'Child education benefits',
        'Family medical coverage',
        'Travel insurance'
      ]
    },
    {
      id: 3,
      name: 'Premium Protection',
      price: '$299',
      features: [
        'All Family Plus features',
        'Worldwide coverage',
        'Premium healthcare access',
        'Investment protection',
        'Retirement benefits',
        'Exclusive member perks'
      ]
    }
  ];

  return (
    <div className="py-12 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">
            Choose Your Perfect Plan
          </h2>
          <p className="mt-4 text-xl text-gray-600">
            Select the coverage that best fits your needs
          </p>
        </div>

        <div className="mt-16 grid gap-8 lg:grid-cols-3 lg:gap-x-8">
          {plans.map((plan) => (
            <div
              key={plan.id}
              className={`relative rounded-2xl shadow-xl overflow-hidden transition-all duration-300 ${
                selectedPlan === plan.id ? 'ring-2 ring-blue-600 transform scale-105' : ''
              }`}
            >
              <div className="bg-white px-6 py-8">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-gray-900">{plan.name}</h3>
                  <Shield className="h-6 w-6 text-blue-600" />
                </div>
                <p className="mt-4 text-3xl font-bold text-gray-900">{plan.price}</p>
                <p className="mt-1 text-sm text-gray-500">per month</p>

                <ul className="mt-6 space-y-4">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-start">
                      <Check className="h-5 w-5 text-green-500 mr-2" />
                      <span className="text-sm text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                <button
                  onClick={() => setSelectedPlan(plan.id)}
                  className={`mt-8 w-full px-4 py-2 rounded-md font-medium ${
                    selectedPlan === plan.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900 hover:bg-gray-200'
                  }`}
                >
                  {selectedPlan === plan.id ? 'Selected' : 'Select Plan'}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Plans;