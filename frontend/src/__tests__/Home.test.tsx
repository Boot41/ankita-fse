import { render, screen, fireEvent } from '@testing-library/react';
import { vi } from 'vitest';
import { TestWrapper } from '../setupTests';
import Home from '../pages/Home';

beforeEach(() => {
  vi.clearAllMocks();
});

describe('Home Component', () => {
  test('renders hero section', () => {
    render(
      <TestWrapper>
        <Home />
      </TestWrapper>
    );

    expect(screen.getByText(/Find the Perfect Health Insurance Plan/i)).toBeInTheDocument();
    expect(screen.getByText(/Get personalized recommendations based on your needs/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Get Started/i })).toBeInTheDocument();
  });

  test('renders features section', () => {
    render(
      <TestWrapper>
        <Home />
      </TestWrapper>
    );

    expect(screen.getByText(/Smart Recommendations/i)).toBeInTheDocument();
    expect(screen.getByText(/Plan Comparison/i)).toBeInTheDocument();
    expect(screen.getByText(/User Reviews/i)).toBeInTheDocument();
  });

  test('navigates to signup page when Get Started is clicked', () => {
    render(
      <TestWrapper>
        <Home />
      </TestWrapper>
    );

    const getStartedButton = screen.getByRole('link', { name: /Get Started/i });
    expect(getStartedButton.getAttribute('href')).toBe('/signup');
  });

  test('renders testimonials section', () => {
    render(
      <TestWrapper>
        <Home />
      </TestWrapper>
    );

    expect(screen.getByText(/What Our Users Say/i)).toBeInTheDocument();
    const testimonials = screen.getAllByTestId('testimonial');
    expect(testimonials.length).toBeGreaterThan(0);
  });

  test('renders call-to-action section', () => {
    render(
      <TestWrapper>
        <Home />
      </TestWrapper>
    );

    expect(screen.getByText(/Ready to Find Your Perfect Plan?/i)).toBeInTheDocument();
    expect(screen.getByRole('link', { name: /Sign Up Now/i })).toBeInTheDocument();
  });

  test('renders footer with links', () => {
    render(
      <TestWrapper>
        <Home />
      </TestWrapper>
    );

    expect(screen.getByText(/About Us/i)).toBeInTheDocument();
    expect(screen.getByText(/Contact/i)).toBeInTheDocument();
    expect(screen.getByText(/Privacy Policy/i)).toBeInTheDocument();
    expect(screen.getByText(/Terms of Service/i)).toBeInTheDocument();
  });
});
