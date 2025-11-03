import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { statsAPI } from '../services/api';
import './AdminDashboard.css';

function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await statsAPI.get();
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container"><div className="loading">Loading...</div></div>;
  }

  return (
    <div className="container">
      <div className="admin-dashboard">
        <h1>Admin Dashboard</h1>

        {stats && (
          <div className="admin-stats-grid">
            <div className="admin-stat-card">
              <div className="stat-icon">📚</div>
              <div className="stat-content">
                <h3>Total Books</h3>
                <p className="stat-value">{stats.total_books}</p>
              </div>
            </div>

            <div className="admin-stat-card">
              <div className="stat-icon">✅</div>
              <div className="stat-content">
                <h3>Available Books</h3>
                <p className="stat-value">{stats.available_books}</p>
              </div>
            </div>

            <div className="admin-stat-card">
              <div className="stat-icon">👥</div>
              <div className="stat-content">
                <h3>Total Users</h3>
                <p className="stat-value">{stats.total_users}</p>
              </div>
            </div>

            <div className="admin-stat-card">
              <div className="stat-icon">📖</div>
              <div className="stat-content">
                <h3>Active Loans</h3>
                <p className="stat-value">{stats.active_loans}</p>
              </div>
            </div>
          </div>
        )}

        <div className="admin-actions card">
          <h2>Management</h2>
          <div className="admin-actions-grid">
            <Link to="/admin/books" className="admin-action-card">
              <span className="action-icon">📚</span>
              <h3>Manage Books</h3>
              <p>Add, edit, or delete books from the library</p>
            </Link>

            <Link to="/admin/users" className="admin-action-card">
              <span className="action-icon">👥</span>
              <h3>Manage Users</h3>
              <p>View and manage user accounts</p>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
