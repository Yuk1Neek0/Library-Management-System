import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Navbar from '../components/Navbar';

describe('Navbar Component', () => {
  const mockLogout = jest.fn();

  test('renders navbar with user info when logged in', () => {
    const user = {
      email: 'test@example.com',
      role: 'student'
    };

    render(
      <BrowserRouter>
        <Navbar user={user} onLogout={mockLogout} />
      </BrowserRouter>
    );

    expect(screen.getByText(/Library Management System/i)).toBeInTheDocument();
    expect(screen.getByText(/test@example.com/i)).toBeInTheDocument();
  });

  test('renders navbar without user info when not logged in', () => {
    render(
      <BrowserRouter>
        <Navbar user={null} onLogout={mockLogout} />
      </BrowserRouter>
    );

    expect(screen.getByText(/Library Management System/i)).toBeInTheDocument();
    expect(screen.queryByText(/test@example.com/i)).not.toBeInTheDocument();
  });

  test('shows admin links for admin users', () => {
    const adminUser = {
      email: 'admin@library.com',
      role: 'admin'
    };

    render(
      <BrowserRouter>
        <Navbar user={adminUser} onLogout={mockLogout} />
      </BrowserRouter>
    );

    expect(screen.getByText(/Admin Dashboard/i)).toBeInTheDocument();
  });

  test('does not show admin links for regular users', () => {
    const regularUser = {
      email: 'user@example.com',
      role: 'student'
    };

    render(
      <BrowserRouter>
        <Navbar user={regularUser} onLogout={mockLogout} />
      </BrowserRouter>
    );

    expect(screen.queryByText(/Admin Dashboard/i)).not.toBeInTheDocument();
  });
});
