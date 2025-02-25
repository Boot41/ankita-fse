import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { TestWrapper } from '../setupTests';
import Signup from '../pages/Signup';
import * as authService from '../services/auth';

// Mock the auth service
vi.mock('../services/auth', () => ({
  signup: vi.fn(),
}));

describe('Signup Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('renders signup form', () => {
    render(
      <TestWrapper>
        <Signup />
      </TestWrapper>
    );

    expect(screen.getByText(/Create an Account/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Password/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Age/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Budget/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Family Size/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Medical History/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sign Up/i })).toBeInTheDocument();
  });

  test('handles successful signup', async () => {
    const mockNavigate = vi.fn();
    vi.mock('react-router-dom', () => ({
      ...vi.importActual('react-router-dom'),
      useNavigate: () => mockNavigate,
    }));

    (authService.signup as ReturnType<typeof vi.fn>).mockResolvedValue({
      token: 'test-token',
      user: {
        id: 1,
        username: 'testuser',
      },
    });

    render(
      <TestWrapper>
        <Signup />
      </TestWrapper>
    );

    fireEvent.change(screen.getByLabelText(/Username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: 'password123' },
    });
    fireEvent.change(screen.getByLabelText(/Name/i), {
      target: { value: 'Test User' },
    });
    fireEvent.change(screen.getByLabelText(/Age/i), {
      target: { value: '30' },
    });
    fireEvent.change(screen.getByLabelText(/Budget/i), {
      target: { value: '5000' },
    });
    fireEvent.change(screen.getByLabelText(/Family Size/i), {
      target: { value: '2' },
    });
    fireEvent.change(screen.getByLabelText(/Medical History/i), {
      target: { value: 'No major issues' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Sign Up/i }));

    await waitFor(() => {
      expect(authService.signup).toHaveBeenCalledWith({
        username: 'testuser',
        email: 'test@example.com',
        password: 'password123',
        name: 'Test User',
        age: 30,
        budget: 5000,
        family_size: 2,
        medical_history: 'No major issues',
      });
      expect(mockNavigate).toHaveBeenCalledWith('/dashboard');
    });
  });

  test('handles signup error', async () => {
    const errorMessage = 'Username already exists';
    (authService.signup as ReturnType<typeof vi.fn>).mockRejectedValue(
      new Error(errorMessage)
    );

    render(
      <TestWrapper>
        <Signup />
      </TestWrapper>
    );

    fireEvent.change(screen.getByLabelText(/Username/i), {
      target: { value: 'testuser' },
    });
    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: 'test@example.com' },
    });
    fireEvent.change(screen.getByLabelText(/Password/i), {
      target: { value: 'password123' },
    });

    fireEvent.click(screen.getByRole('button', { name: /Sign Up/i }));

    await waitFor(() => {
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });
  });

  test('validates required fields', async () => {
    render(
      <TestWrapper>
        <Signup />
      </TestWrapper>
    );

    fireEvent.click(screen.getByRole('button', { name: /Sign Up/i }));

    await waitFor(() => {
      expect(screen.getByText(/Username is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Email is required/i)).toBeInTheDocument();
      expect(screen.getByText(/Password is required/i)).toBeInTheDocument();
    });
  });

  test('validates email format', async () => {
    render(
      <TestWrapper>
        <Signup />
      </TestWrapper>
    );

    fireEvent.change(screen.getByLabelText(/Email/i), {
      target: { value: 'invalid-email' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Sign Up/i }));

    await waitFor(() => {
      expect(screen.getByText(/Invalid email format/i)).toBeInTheDocument();
    });
  });
});
