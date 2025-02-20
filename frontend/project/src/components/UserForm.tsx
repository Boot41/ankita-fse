import React, { useState } from 'react';
import { UserFormData } from '../types';

const medicalConditions = [
  'None',
  'Diabetes',
  'Hypertension',
  'Heart Disease',
  'Asthma',
  'Cancer',
  'Other'
];

export function UserForm({ onSubmit }: { onSubmit: (data: UserFormData) => void }) {
  const [formData, setFormData] = useState<UserFormData>({
    age: 0,
    medicalHistory: [],
    budget: 500,
    familySize: 1
  });

  const [errors, setErrors] = useState<Partial<Record<keyof UserFormData, string>>>({});

  const validateForm = () => {
    const newErrors: Partial<Record<keyof UserFormData, string>> = {};
    
    if (formData.age < 18 || formData.age > 100) {
      newErrors.age = 'Age must be between 18 and 100';
    }
    if (formData.budget < 100) {
      newErrors.budget = 'Minimum budget is $100';
    }
    if (formData.familySize < 1) {
      newErrors.familySize = 'Family size must be at least 1';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 bg-white p-6 rounded-lg shadow-md">
      <div>
        <label className="block text-sm font-medium text-gray-700">Age</label>
        <input
          type="number"
          value={formData.age}
          onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
        {errors.age && <p className="mt-1 text-sm text-red-600">{errors.age}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Medical History</label>
        <select
          multiple
          value={formData.medicalHistory}
          onChange={(e) => setFormData({
            ...formData,
            medicalHistory: Array.from(e.target.selectedOptions, option => option.value)
          })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        >
          {medicalConditions.map(condition => (
            <option key={condition} value={condition}>{condition}</option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">
          Monthly Budget: ${formData.budget}
        </label>
        <input
          type="range"
          min="100"
          max="2000"
          step="50"
          value={formData.budget}
          onChange={(e) => setFormData({ ...formData, budget: parseInt(e.target.value) })}
          className="mt-1 block w-full"
        />
        {errors.budget && <p className="mt-1 text-sm text-red-600">{errors.budget}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700">Family Size</label>
        <input
          type="number"
          min="1"
          value={formData.familySize}
          onChange={(e) => setFormData({ ...formData, familySize: parseInt(e.target.value) })}
          className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
        />
        {errors.familySize && <p className="mt-1 text-sm text-red-600">{errors.familySize}</p>}
      </div>

      <button
        type="submit"
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
      >
        Get Recommendations
      </button>
    </form>
  );
}