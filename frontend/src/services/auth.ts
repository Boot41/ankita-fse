import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/';
const AUTH_URL = 'http://127.0.0.1:8000/api/token/';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface SignupCredentials extends LoginCredentials {
  email: string;
  name?: string;
  age?: number;
  budget?: number;
  family_size?: number;
  medical_history?: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export const signup = async (credentials: SignupCredentials): Promise<void> => {
  try {
    await axios.post(`${API_URL}users/`, credentials);
  } catch (error: any) {
    if (error.response?.data) {
      throw new Error(Object.values(error.response.data).flat().join(', '));
    }
    throw new Error('Signup failed. Please try again.');
  }
};

export const login = async (credentials: LoginCredentials): Promise<AuthTokens> => {
  try {
    const response = await axios.post(AUTH_URL, credentials);
    if (response.data.access) {
      localStorage.setItem('tokens', JSON.stringify(response.data));
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
    }
    return response.data;
  } catch (error: any) {
    if (error.response?.data) {
      throw new Error(Object.values(error.response.data).flat().join(', '));
    }
    throw new Error('Login failed. Please check your credentials.');
  }
};

export const logout = (): void => {
  localStorage.removeItem('tokens');
  delete axios.defaults.headers.common['Authorization'];
};

export const refreshToken = async (): Promise<string> => {
  try {
    const tokens = JSON.parse(localStorage.getItem('tokens') || '{}');
    const response = await axios.post(`${AUTH_URL}refresh/`, {
      refresh: tokens.refresh
    });
    if (response.data.access) {
      const newTokens = { ...tokens, access: response.data.access };
      localStorage.setItem('tokens', JSON.stringify(newTokens));
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
      return response.data.access;
    }
    throw new Error('Failed to refresh token');
  } catch (error) {
    logout();
    throw new Error('Session expired. Please login again.');
  }
};

export const isAuthenticated = (): boolean => {
  const tokens = localStorage.getItem('tokens');
  return tokens !== null;
};

// Setup axios interceptor for token refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        await refreshToken();
        return axios(originalRequest);
      } catch (refreshError) {
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);
