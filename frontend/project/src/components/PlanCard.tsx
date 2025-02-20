import React from 'react';
import { InsurancePlan } from '../types';
import { Check, Star } from 'lucide-react';

interface PlanCardProps {
  plan: InsurancePlan;
  onSelect: (plan: InsurancePlan) => void;
  isSelected?: boolean;
}

export function PlanCard({ plan, onSelect, isSelected }: PlanCardProps) {
  return (
    <div
      className={`${
        isSelected ? 'ring-2 ring-indigo-500' : ''
      } bg-white rounded-lg shadow-md overflow-hidden transition-all hover:shadow-lg`}
    >
      <div className="p-6">
        <div className="flex justify-between items-start">
          <h3 className="text-xl font-semibold text-gray-900">{plan.name}</h3>
          <div className="flex items-center">
            <Star className="w-5 h-5 text-yellow-400 fill-current" />
            <span className="ml-1 text-sm text-gray-600">{plan.rating}</span>
          </div>
        </div>
        
        <p className="mt-2 text-2xl font-bold text-gray-900">${plan.price}/mo</p>
        
        <div className="mt-4">
          <h4 className="text-sm font-medium text-gray-900">Coverage Includes:</h4>
          <ul className="mt-2 space-y-2">
            {plan.coverage.map((item, index) => (
              <li key={index} className="flex items-center text-sm text-gray-600">
                <Check className="w-4 h-4 mr-2 text-green-500" />
                {item}
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-6">
          <button
            onClick={() => onSelect(plan)}
            className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 transition-colors"
          >
            {isSelected ? 'Selected for Comparison' : 'Select for Comparison'}
          </button>
        </div>
      </div>
    </div>
  );
}