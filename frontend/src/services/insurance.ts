import axios from 'axios';
import { API_URL } from '../config';

export interface InsurancePlan {
  id: number;
  name: string;
  coverage: string;
  price: number;
  price_per_month: number;
  conditions: string;
}

export const comparePlans = async (planIds: number[]): Promise<InsurancePlan[]> => {
  try {
    const response = await axios.post(`${API_URL}/api/plans/compare/`, { plan_ids: planIds });
    return response.data;
  } catch (error) {
    throw new Error('Failed to compare plans');
  }
};
