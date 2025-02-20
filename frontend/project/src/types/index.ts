export interface InsurancePlan {
  id: string;
  name: string;
  price: number;
  coverage: string[];
  conditions: string[];
  description: string;
  rating: number;
}

export interface UserFormData {
  age: number;
  medicalHistory: string[];
  budget: number;
  familySize: number;
}

export interface FeedbackData {
  rating: number;
  comment: string;
  planId: string;
}

export interface AuthUser {
  email: string;
  name: string;
}

export interface LoginFormData {
  email: string;
  password: string;
}