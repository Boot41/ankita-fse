import axios from 'axios';
import { isAuthenticated, refreshToken } from './auth';

const API_URL = 'http://127.0.0.1:8000/api/';

export interface DashboardData {
  user: {
    name: string;
    age: number;
    budget: number;
    family_size: number;
    medical_history: string;
  };
  plans: Array<{
    id: number;
    name: string;
    coverage: string;
    price: number;
    price_per_month: number;
    conditions: string;
  }>;
  recommendations: Array<{
    id: number;
    name: string;
    coverage: string;
    price: number;
    price_per_month: number;
    conditions: string;
    suitability_score: number;
  }>;
  feedback: Array<{
    id: number;
    rating: number;
    comments: string;
    created_at: string;
  }>;
}

const ensureAuth = async () => {
  if (!isAuthenticated()) {
    throw new Error('Please login to continue');
  }
  const tokens = JSON.parse(localStorage.getItem('tokens') || '{}');
  axios.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`;
};

export const getDashboardData = async (): Promise<DashboardData> => {
  try {
    await ensureAuth();

    // Get user data
    const userResponse = await axios.get(`${API_URL}users/me/`);
    const user = userResponse.data;

    // Get insurance plans
    const plansResponse = await axios.get(`${API_URL}plans/`);
    const plans = plansResponse.data;

    // Get recommendations
    const recommendationsResponse = await axios.get(`${API_URL}recommendations/`);
    const recommendations = recommendationsResponse.data.recommended_plans || [];

    // Get user feedback
    const feedbackResponse = await axios.get(`${API_URL}feedback/`);
    const feedback = Array.isArray(feedbackResponse.data) ? feedbackResponse.data : [];

    return {
      user,
      plans,
      recommendations,
      feedback
    };
  } catch (error: any) {
    if (error.response?.status === 401) {
      try {
        await refreshToken();
        return getDashboardData();
      } catch (refreshError) {
        throw new Error('Session expired. Please login again.');
      }
    }
    if (error.response?.data) {
      throw new Error(Object.values(error.response.data).flat().join(', '));
    }
    throw error;
  }
};

export const submitFeedback = async (rating: number, comments: string): Promise<void> => {
  try {
    await ensureAuth();
    await axios.post(`${API_URL}feedback/`, { rating, comments });
  } catch (error: any) {
    if (error.response?.status === 401) {
      try {
        await refreshToken();
        return submitFeedback(rating, comments);
      } catch (refreshError) {
        throw new Error('Session expired. Please login again.');
      }
    }
    if (error.response?.data) {
      throw new Error(Object.values(error.response.data).flat().join(', '));
    }
    throw error;
  }
};
