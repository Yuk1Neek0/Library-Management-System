import { useState, useEffect } from 'react';
import { loansAPI } from '../services/api';
import './MyLoans.css';

function MyLoans({ user }) {
  const [loans, setLoans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchLoans();
  }, []);

  const fetchLoans = async () => {
    try {
      const response = await loansAPI.getAll();
      setLoans(response.data);
    } catch (error) {
      console.error('Error fetching loans:', error);
      setMessage({ type: 'error', text: 'Failed to load loans' });
    } finally {
      setLoading(false);
    }
  };

  const handleReturn = async (loanId) => {
    try {
      await loansAPI.return(loanId);
      setMessage({ type: 'success', text: 'Book returned successfully!' });
      fetchLoans();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to return book'
      });
    }
  };

  const isOverdue = (dueDate) => {
    return new Date(dueDate) < new Date();
  };

  if (loading) {
    return <div className="container"><div className="loading">Loading loans...</div></div>;
  }

  const activeLoans = loans.filter(loan => loan.status === 'active');
  const returnedLoans = loans.filter(loan => loan.status === 'returned');

  return (
    <div className="container">
      <div className="my-loans-page">
        <h1>My Loans</h1>

        {message.text && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
            <button onClick={() => setMessage({ type: '', text: '' })} className="alert-close">×</button>
          </div>
        )}

        {/* Active Loans */}
        <div className="loans-section card">
          <h2>Active Loans ({activeLoans.length})</h2>

          {activeLoans.length === 0 ? (
            <p className="no-loans">You don't have any active loans.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Book</th>
                  <th>Author</th>
                  <th>Borrowed Date</th>
                  <th>Due Date</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {activeLoans.map((loan) => (
                  <tr key={loan.id} className={isOverdue(loan.due_date) ? 'overdue-row' : ''}>
                    <td>{loan.title}</td>
                    <td>{loan.author}</td>
                    <td>{new Date(loan.borrow_date).toLocaleDateString()}</td>
                    <td>
                      {new Date(loan.due_date).toLocaleDateString()}
                      {isOverdue(loan.due_date) && (
                        <span className="badge badge-danger ml-2">Overdue</span>
                      )}
                    </td>
                    <td>
                      <span className="badge badge-warning">Active</span>
                    </td>
                    <td>
                      <button
                        onClick={() => handleReturn(loan.id)}
                        className="btn btn-primary btn-small"
                      >
                        Return
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Loan History */}
        <div className="loans-section card">
          <h2>Loan History ({returnedLoans.length})</h2>

          {returnedLoans.length === 0 ? (
            <p className="no-loans">No loan history yet.</p>
          ) : (
            <table className="table">
              <thead>
                <tr>
                  <th>Book</th>
                  <th>Author</th>
                  <th>Borrowed Date</th>
                  <th>Due Date</th>
                  <th>Returned Date</th>
                </tr>
              </thead>
              <tbody>
                {returnedLoans.map((loan) => (
                  <tr key={loan.id}>
                    <td>{loan.title}</td>
                    <td>{loan.author}</td>
                    <td>{new Date(loan.borrow_date).toLocaleDateString()}</td>
                    <td>{new Date(loan.due_date).toLocaleDateString()}</td>
                    <td>
                      {loan.return_date ? new Date(loan.return_date).toLocaleDateString() : 'N/A'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}

export default MyLoans;
