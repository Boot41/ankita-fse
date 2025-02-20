import React from 'react';
import { InsurancePlan } from '../types';
import { Check, X } from 'lucide-react';

interface ComparisonTableProps {
  plans: InsurancePlan[];
}

export function ComparisonTable({ plans }: ComparisonTableProps) {
  if (plans.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">Select plans to compare</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Feature
            </th>
            {plans.map((plan) => (
              <th
                key={plan.id}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
              >
                {plan.name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              Monthly Premium
            </td>
            {plans.map((plan) => (
              <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                ${plan.price}
              </td>
            ))}
          </tr>
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              Coverage
            </td>
            {plans.map((plan) => (
              <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <ul className="list-none">
                  {plan.coverage.map((item, index) => (
                    <li key={index} className="flex items-center">
                      <Check className="w-4 h-4 mr-2 text-green-500" />
                      {item}
                    </li>
                  ))}
                </ul>
              </td>
            ))}
          </tr>
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              Conditions
            </td>
            {plans.map((plan) => (
              <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <ul className="list-none">
                  {plan.conditions.map((condition, index) => (
                    <li key={index}>{condition}</li>
                  ))}
                </ul>
              </td>
            ))}
          </tr>
          <tr>
            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
              Rating
            </td>
            {plans.map((plan) => (
              <td key={plan.id} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                <div className="flex items-center">
                  {plan.rating} / 5
                </div>
              </td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  );
}