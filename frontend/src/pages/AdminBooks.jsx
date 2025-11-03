import { useState, useEffect } from 'react';
import { booksAPI } from '../services/api';
import './AdminBooks.css';

function AdminBooks() {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState({ type: '', text: '' });
  const [showModal, setShowModal] = useState(false);
  const [editingBook, setEditingBook] = useState(null);
  const [formData, setFormData] = useState({
    isbn: '',
    title: '',
    author: '',
    category: '',
    total_copies: 1,
    available_copies: 1,
    description: '',
  });

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async () => {
    try {
      const response = await booksAPI.getAll({});
      setBooks(response.data);
    } catch (error) {
      console.error('Error fetching books:', error);
      setMessage({ type: 'error', text: 'Failed to load books' });
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const value = e.target.type === 'number' ? parseInt(e.target.value) : e.target.value;
    setFormData({
      ...formData,
      [e.target.name]: value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (editingBook) {
        await booksAPI.update(editingBook.id, formData);
        setMessage({ type: 'success', text: 'Book updated successfully!' });
      } else {
        await booksAPI.create(formData);
        setMessage({ type: 'success', text: 'Book added successfully!' });
      }

      setShowModal(false);
      setEditingBook(null);
      resetForm();
      fetchBooks();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Operation failed'
      });
    }
  };

  const handleEdit = (book) => {
    setEditingBook(book);
    setFormData({
      isbn: book.isbn || '',
      title: book.title,
      author: book.author,
      category: book.category || '',
      total_copies: book.total_copies,
      available_copies: book.available_copies,
      description: book.description || '',
    });
    setShowModal(true);
  };

  const handleDelete = async (bookId) => {
    if (!window.confirm('Are you sure you want to delete this book?')) {
      return;
    }

    try {
      await booksAPI.delete(bookId);
      setMessage({ type: 'success', text: 'Book deleted successfully!' });
      fetchBooks();
    } catch (error) {
      setMessage({
        type: 'error',
        text: error.response?.data?.error || 'Failed to delete book'
      });
    }
  };

  const resetForm = () => {
    setFormData({
      isbn: '',
      title: '',
      author: '',
      category: '',
      total_copies: 1,
      available_copies: 1,
      description: '',
    });
  };

  const handleAddNew = () => {
    setEditingBook(null);
    resetForm();
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingBook(null);
    resetForm();
  };

  if (loading) {
    return <div className="container"><div className="loading">Loading...</div></div>;
  }

  return (
    <div className="container">
      <div className="admin-books-page">
        <div className="page-header">
          <h1>Manage Books</h1>
          <button onClick={handleAddNew} className="btn btn-primary">
            Add New Book
          </button>
        </div>

        {message.text && (
          <div className={`alert alert-${message.type}`}>
            {message.text}
            <button onClick={() => setMessage({ type: '', text: '' })} className="alert-close">×</button>
          </div>
        )}

        <div className="card">
          <table className="table">
            <thead>
              <tr>
                <th>ISBN</th>
                <th>Title</th>
                <th>Author</th>
                <th>Category</th>
                <th>Copies</th>
                <th>Available</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {books.map((book) => (
                <tr key={book.id}>
                  <td>{book.isbn || 'N/A'}</td>
                  <td>{book.title}</td>
                  <td>{book.author}</td>
                  <td>{book.category || 'N/A'}</td>
                  <td>{book.total_copies}</td>
                  <td>{book.available_copies}</td>
                  <td>
                    <div className="action-buttons">
                      <button
                        onClick={() => handleEdit(book)}
                        className="btn btn-warning btn-small"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(book.id)}
                        className="btn btn-danger btn-small"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Modal */}
        {showModal && (
          <div className="modal-overlay" onClick={handleCloseModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>{editingBook ? 'Edit Book' : 'Add New Book'}</h2>
                <button onClick={handleCloseModal} className="modal-close">×</button>
              </div>

              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label htmlFor="title">Title *</label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="author">Author *</label>
                  <input
                    type="text"
                    id="author"
                    name="author"
                    value={formData.author}
                    onChange={handleChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="isbn">ISBN</label>
                  <input
                    type="text"
                    id="isbn"
                    name="isbn"
                    value={formData.isbn}
                    onChange={handleChange}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="category">Category</label>
                  <input
                    type="text"
                    id="category"
                    name="category"
                    value={formData.category}
                    onChange={handleChange}
                  />
                </div>

                <div className="form-row">
                  <div className="form-group">
                    <label htmlFor="total_copies">Total Copies *</label>
                    <input
                      type="number"
                      id="total_copies"
                      name="total_copies"
                      value={formData.total_copies}
                      onChange={handleChange}
                      min="1"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label htmlFor="available_copies">Available Copies *</label>
                    <input
                      type="number"
                      id="available_copies"
                      name="available_copies"
                      value={formData.available_copies}
                      onChange={handleChange}
                      min="0"
                      required
                    />
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="description">Description</label>
                  <textarea
                    id="description"
                    name="description"
                    value={formData.description}
                    onChange={handleChange}
                    rows="4"
                  />
                </div>

                <div className="modal-actions">
                  <button type="button" onClick={handleCloseModal} className="btn btn-secondary">
                    Cancel
                  </button>
                  <button type="submit" className="btn btn-primary">
                    {editingBook ? 'Update' : 'Add'} Book
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminBooks;
