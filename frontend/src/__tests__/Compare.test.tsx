import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { vi } from 'vitest';
import Compare from '../pages/Compare';
import * as insuranceService from '../services/insurance';

// Mock the insurance service
vi.mock('../services/insurance', () => ({
  comparePlans: vi.fn(),
}));

const mockPlans = [
  {
    id: 1,
    name: 'Basic Coverage',
    price: '$99',
    features: {
      'Personal Liability': true,
      'Property Damage': true,
      'Medical Payments': true,
      '24/7 Support': true,
      'Family Protection': false,
      'Child Education': false,
      'Travel Insurance': false,
      'Worldwide Coverage': false,
      'Premium Healthcare': false,
      'Investment Protection': false,
      'Retirement Benefits': false
    }
  },
  {
    id: 2,
    name: 'Family Plus',
    price: '$199',
    features: {
      'Personal Liability': true,
      'Property Damage': true,
      'Medical Payments': true,
      '24/7 Support': true,
      'Family Protection': true,
      'Child Education': true,
      'Travel Insurance': true,
      'Worldwide Coverage': false,
      'Premium Healthcare': false,
      'Investment Protection': false,
      'Retirement Benefits': false
    }
  }
];

describe('Compare Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test('renders compare plans page', () => {
    render(
      <BrowserRouter>
        <Compare />
      </BrowserRouter>
    );
    expect(screen.getByText(/Compare Insurance Plans/i)).toBeInTheDocument();
  });

  test('displays selected plans for comparison', () => {
    render(
      <BrowserRouter>
        <Compare />
      </BrowserRouter>
    );

    const planHeaders = screen.getAllByRole('heading', { level: 3 });
    expect(planHeaders[0]).toHaveTextContent('Basic Coverage');
    expect(planHeaders[1]).toHaveTextContent('Family Plus');
    expect(screen.getAllByText('$99')).toHaveLength(1);
    expect(screen.getAllByText('$199')).toHaveLength(1);
  });

  test('can add a third plan', () => {
    render(
      <BrowserRouter>
        <Compare />
      </BrowserRouter>
    );

    const addButton = screen.getByRole('button', { name: /add another plan/i });
    fireEvent.click(addButton);

    const planHeaders = screen.getAllByRole('heading', { level: 3 });
    expect(planHeaders[2]).toHaveTextContent('Premium Protection');
    expect(screen.getAllByText('$299')).toHaveLength(1);
  });

  test('displays feature comparison correctly', () => {
    render(
      <BrowserRouter>
        <Compare />
      </BrowserRouter>
    );

    // Check for feature names
    expect(screen.getByText('Personal Liability')).toBeInTheDocument();
    expect(screen.getByText('Family Protection')).toBeInTheDocument();

    // Check for feature icons (included/not included)
    const checkIcons = screen.getAllByTestId('feature-included');
    const xIcons = screen.getAllByTestId('feature-not-included');
    expect(checkIcons.length).toBeGreaterThan(0);
    expect(xIcons.length).toBeGreaterThan(0);
  });
});
