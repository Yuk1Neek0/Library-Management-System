import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { statsAPI, loansAPI } from '../services/api';
import './Dashboard.css';

function Dashboard({ user }) {
  const [stats, setStats] = useState(null);
  const [recentLoans, setRecentLoans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const loansResponse = await loansAPI.getAll();
      setRecentLoans(loansResponse.data.slice(0, 5));

      if (user.role === 'admin') {
        const statsResponse = await statsAPI.get();
        setStats(statsResponse.data);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="container"><div className="loading">Loading...</div></div>;
  }

  return (
    <div className="container">
      <div className="dashboard">
        <h1>Welcome, {user.full_name}!</h1>

        {user.role === 'admin' && stats && (
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Books</h3>
              <p className="stat-number">{stats.total_books}</p>
            </div>
            <div className="stat-card">
              <h3>Available Books</h3>
              <p className="stat-number">{stats.available_books}</p>
            </div>
            <div className="stat-card">
              <h3>Total Users</h3>
              <p className="stat-number">{stats.total_users}</p>
            </div>
            <div className="stat-card">
              <h3>Active Loans</h3>
              <p className="stat-number">{stats.active_loans}</p>
            </div>
          </div>
        )}

        <div className="quick-actions card">
          <h2>Quick Actions</h2>
          <div className="actions-grid">
            <Link to="/books" className="action-btn">
              <span className="action-icon">📚</span>
              <span>Browse Books</span>
            </Link>
            <Link to="/my-loans" className="action-btn">
              <span className="action-icon">📖</span>
              <span>My Loans</span>
            </Link>
            {user.role === 'admin' && (
              <>
                <Link to="/admin/books" className="action-btn">
                  <span className="action-icon">➕</span>
                  <span>Manage Books</span>
                </Link>
                <Link to="/admin/users" className="action-btn">
                  <span className="action-icon">👥</span>
                  <span>Manage Users</span>
                </Link>
              </>
            )}
          </div>
        </div>

        {recentLoans.length > 0 && (
          <div className="recent-loans card">
            <h2>Recent Activity</h2>
            <table className="table">
              <thead>
                <tr>
                  <th>Book</th>
                  <th>Borrowed Date</th>
                  <th>Due Date</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {recentLoans.map((loan) => (
                  <tr key={loan.id}>
                    <td>{loan.title}</td>
                    <td>{new Date(loan.borrow_date).toLocaleDateString()}</td>
                    <td>{new Date(loan.due_date).toLocaleDateString()}</td>
                    <td>
                      <span className={`badge badge-${loan.status === 'active' ? 'warning' : 'success'}`}>
                        {loan.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
