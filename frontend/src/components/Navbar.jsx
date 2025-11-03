import { Link } from 'react-router-dom';
import './Navbar.css';

function Navbar({ user, onLogout }) {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-brand">
          Library System
        </Link>
        <div className="navbar-links">
          <Link to="/dashboard" className="nav-link">Dashboard</Link>
          <Link to="/books" className="nav-link">Books</Link>
          <Link to="/my-loans" className="nav-link">My Loans</Link>
          {user.role === 'admin' && (
            <Link to="/admin" className="nav-link">Admin</Link>
          )}
        </div>
        <div className="navbar-user">
          <span className="user-name">{user.full_name}</span>
          <span className="user-role">({user.role})</span>
          <button onClick={onLogout} className="btn btn-secondary btn-small">
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
