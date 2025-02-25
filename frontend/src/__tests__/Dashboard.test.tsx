import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter, useNavigate } from 'react-router-dom';
import { vi } from 'vitest';
import Dashboard from '../pages/Dashboard';
import * as dashboardService from '../services/dashboard';

// Mock react-router-dom
const mockNavigate = vi.fn();
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom');
  return {
    ...actual,
    BrowserRouter: ({ children }: { children: React.ReactNode }) => <>{children}</>,
    useNavigate: () => mockNavigate,
    useLocation: () => ({ pathname: '/' })
  };
});

beforeEach(() => {
  mockNavigate.mockClear();
});

// Mock the dashboard service
vi.mock('../services/dashboard', () => ({
  getDashboardData: vi.fn(),
  submitFeedback: vi.fn(),
}));

const mockDashboardData = {
  user: {
    name: 'Test User',
    age: 30,
    budget: 5000,
    family_size: 2,
    medical_history: 'No major issues'
  },
  plans: [
    {
      id: 1,
      name: 'Basic Plan',
      coverage: 'Basic Coverage',
      price: 2000,
      price_per_month: 166.67,
      conditions: 'Standard conditions'
    }
  ],
  recommendations: [
    {
      id: 1,
      name: 'Family Plan',
      coverage: 'Family Coverage',
      price: 4000,
      price_per_month: 333.33,
      conditions: 'Family conditions',
      suitability_score: 0.85
    }
  ],
  feedback: [
    {
      id: 1,
      rating: 5,
      comments: 'Great service!',
      created_at: '2025-02-25T00:00:00Z'
    }
  ]
};

describe('Dashboard Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    (dashboardService.getDashboardData as ReturnType<typeof vi.fn>).mockResolvedValue(mockDashboardData);
  });

  test('renders dashboard with user profile', async () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(/Welcome, Test User/i)).toBeInTheDocument();
      expect(screen.getByText(/Age: 30/i)).toBeInTheDocument();
      expect(screen.getByText(/Budget: \$5000/i)).toBeInTheDocument();
      expect(screen.getByText(/Family Size: 2/i)).toBeInTheDocument();
      expect(screen.getByText(/Medical History: No major issues/i)).toBeInTheDocument();
    });
  });

  test('displays recommended plans', async () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText('Family Plan')).toBeInTheDocument();
      expect(screen.getByText('85% Match')).toBeInTheDocument();
      expect(screen.getByText('$333.33/month')).toBeInTheDocument();
      expect(screen.getByText('Family Coverage')).toBeInTheDocument();
    });
  });

  test('handles feedback submission', async () => {
    (dashboardService.submitFeedback as ReturnType<typeof vi.fn>).mockResolvedValue(undefined);

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    const ratingSelect = screen.getByRole('combobox');
    const commentsTextarea = screen.getByPlaceholderText(/share your experience/i);
    const submitButton = screen.getByRole('button', { name: /submit feedback/i });

    fireEvent.change(ratingSelect, { target: { value: '4' } });
    fireEvent.change(commentsTextarea, { target: { value: 'Great service!' } });
    fireEvent.click(submitButton);

    expect(dashboardService.submitFeedback).toHaveBeenCalledWith(4, 'Great service!');
  });

  test('handles feedback submission error', async () => {
    const errorMessage = 'Failed to submit feedback';
    (dashboardService.submitFeedback as ReturnType<typeof vi.fn>).mockRejectedValue(new Error(errorMessage));

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    const ratingSelect = screen.getByRole('combobox');
    const commentsTextarea = screen.getByPlaceholderText(/share your experience/i);
    const submitButton = screen.getByRole('button', { name: /submit feedback/i });

    fireEvent.change(ratingSelect, { target: { value: '3' } });
    fireEvent.change(commentsTextarea, { target: { value: 'Test feedback' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('displays loading state', () => {
    (dashboardService.getDashboardData as ReturnType<typeof vi.fn>).mockImplementation(
      () => new Promise(resolve => setTimeout(() => resolve(mockDashboardData), 100))
    );

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    const loadingSpinner = screen.getByTestId('loading-spinner');
    expect(loadingSpinner).toHaveClass('animate-spin');
  });

  test('handles error state', async () => {
    const errorMessage = 'Failed to load dashboard data';
    (dashboardService.getDashboardData as ReturnType<typeof vi.fn>).mockRejectedValue(new Error(errorMessage));

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('displays feedback submission loading state', async () => {
    (dashboardService.submitFeedback as ReturnType<typeof vi.fn>).mockImplementation(
      () => new Promise(resolve => setTimeout(resolve, 100))
    );

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(screen.queryByTestId('loading-spinner')).not.toBeInTheDocument();
    });

    const ratingSelect = screen.getByRole('combobox');
    const commentsTextarea = screen.getByPlaceholderText(/share your experience/i);
    const submitButton = screen.getByRole('button', { name: /submit feedback/i });

    fireEvent.change(ratingSelect, { target: { value: '5' } });
    fireEvent.change(commentsTextarea, { target: { value: 'Test comment' } });
    fireEvent.click(submitButton);

    expect(screen.getByText('Submitting...')).toBeInTheDocument();
  });

  test('displays recent feedback', async () => {
    (dashboardService.getDashboardData as ReturnType<typeof vi.fn>).mockResolvedValue({
      user: {
        name: 'John Doe',
        age: 30,
        budget: 1000,
        family_size: 2,
        medical_history: 'No major issues'
      },
      recommendations: [
        {
          name: 'Family Plan',
          coverage: 'Family Coverage',
          price: 4000,
          price_per_month: 333.33,
          suitability_score: 0.85
        }
      ],
      recent_feedback: [
        {
          rating: 5,
          comments: 'Great service!'
        }
      ]
    });

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    // Wait for feedback section to appear
    const feedbackHeader = await screen.findByText('Recent Feedback');
    expect(feedbackHeader).toBeInTheDocument();

    // Wait for feedback content
    const feedbackComment = await screen.findByText(/Great service!/i);
    expect(feedbackComment).toBeInTheDocument();

    // Check for star rating
    const stars = await screen.findAllByTestId('star');
    expect(stars).toHaveLength(5);
  });

  test('handles 401 unauthorized error', async () => {
    const errorMessage = '401 Unauthorized';
    (dashboardService.getDashboardData as ReturnType<typeof vi.fn>).mockRejectedValue(new Error(errorMessage));

    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );

    await waitFor(() => {
      expect(mockNavigate).toHaveBeenCalledWith('/login');
    });
  });
});
