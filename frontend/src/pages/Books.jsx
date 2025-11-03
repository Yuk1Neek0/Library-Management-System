import { useState, useEffect } from 'react';
import { booksAPI, loansAPI } from '../services/api';
import './Books.css';

function Books({ user }) {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [category, setCategory] = useState('');
  const [availableOnly, setAvailableOnly] = useState(false);
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchBooks();
  }, [searchTerm, category, availableOnly]);

  const fetchBooks = async () => {
    try {
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (category) params.category = category;
      if (availableOnly) params.available_only = 'true';

      const response = await booksAPI.getAll(params);
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
      setMessage({ type: 'error', text: 'Failed to load books' });
    } finally {
      setLoading(false);
    }
  };

  const handleBorrow = async (bookId) => {
    try {
      await loansAPI.borrow(bookId);
      setMessage({ type: 'success', text: 'Book borrowed successfully!' });
      fetchBooks();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to borrow book'
      });
    }
  };

  const categories = [...new Set(books.map(book => book.category).filter(Boolean))];

  if (loading) {
    return <div className="container"><div className="loading">Loading books...</div></div>;
  }

  return (
    <div className="container">
      <div className="books-page">
        <h1>Browse Books</h1>

        {message.text && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
            <button onClick={() => setMessage({ type: '', text: '' })} className="alert-close">×</button>
          </div>
        )}

        <div className="filters card">
          <div className="filter-row">
            <div className="form-group">
              <input
                type="text"
                placeholder="Search by title, author, or ISBN..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>

            <div className="form-group">
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="filter-select"
              >
                <option value="">All Categories</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            <div className="form-group checkbox-group">
              <label>
                <input
                  type="checkbox"
                  checked={availableOnly}
                  onChange={(e) => setAvailableOnly(e.target.checked)}
                />
                <span>Available only</span>
              </label>
            </div>
          </div>
        </div>

        {books.length === 0 ? (
          <div className="no-books card">
            <p>No books found matching your criteria.</p>
          </div>
        ) : (
          <div className="books-grid">
            {books.map((book) => (
              <div key={book.id} className="book-card">
                <div className="book-header">
                  <h3>{book.title}</h3>
                  <span className={`badge badge-${book.available_copies > 0 ? 'success' : 'danger'}`}>
                    {book.available_copies > 0 ? 'Available' : 'Unavailable'}
                  </span>
                </div>

                <p className="book-author">By {book.author}</p>

                {book.category && (
                  <p className="book-category">
                    <span className="badge badge-info">{book.category}</span>
                  </p>
                )}

                {book.description && (
                  <p className="book-description">{book.description}</p>
                )}

                {book.isbn && (
                  <p className="book-isbn">ISBN: {book.isbn}</p>
                )}

                <div className="book-availability">
                  <span>Available: {book.available_copies} / {book.total_copies}</span>
                </div>

                {book.available_copies > 0 && (
                  <button
                    onClick={() => handleBorrow(book.id)}
                    className="btn btn-primary btn-full"
                  >
                    Borrow Book
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Books;
