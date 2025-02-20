import React from 'react';
import { FeedbackForm } from '../components/FeedbackForm';
import { FeedbackData } from '../types';

export function Feedback() {
  const handleFeedbackSubmit = (feedback: FeedbackData) => {
    // Here you would typically send the feedback to your backend
    console.log('Feedback submitted:', feedback);
  };

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">Share Your Feedback</h2>
      <p className="text-gray-600 mb-8">
        Help us improve our recommendations by sharing your experience with our service.
      </p>
      <FeedbackForm onSubmit={handleFeedbackSubmit} planId="1" />
    </div>
  );
}