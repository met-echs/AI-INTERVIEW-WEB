import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

// Configure Axios defaults
axios.defaults.withCredentials = true;

const ApplyForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    phone: "",
  });
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const maxFileSize = 2 * 1024 * 1024; // 2MB

  // Fetch CSRF token on component mount
  useEffect(() => {
    const fetchCsrfToken = async () => {
      try {
        await axios.get(`${process.env.REACT_APP_API_URL}/csrf-token/`);
      } catch (error) {
        console.error("Error fetching CSRF token:", error);
      }
    };
    fetchCsrfToken();
  }, []);

  // Form validation
  const validateForm = () => {
    const newErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const phoneRegex = /^[+]?[(]?[0-9]{1,4}[)]?[-\s./0-9]*$/;

    if (!formData.name.trim()) newErrors.name = "Name is required";
    if (!emailRegex.test(formData.email)) newErrors.email = "Invalid email address";
    if (!phoneRegex.test(formData.phone)) newErrors.phone = "Invalid phone number";
    
    if (!file) {
      newErrors.file = "PDF file is required";
    } else {
      if (file.type !== "application/pdf") newErrors.file = "Only PDF files are allowed";
      if (file.size > maxFileSize) newErrors.file = "File size must be less than 2MB";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Get CSRF token from cookies
  const getCsrfToken = () => {
    return document.cookie
      .split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    if (errors[name]) setErrors(prev => ({ ...prev, [name]: "" }));
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (errors.file) setErrors(prev => ({ ...prev, file: "" }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    
    const formPayload = new FormData();
    formPayload.append("name", formData.name);
    formPayload.append("email", formData.email);
    formPayload.append("phone", formData.phone);
    formPayload.append("resume", file);

    try {
      const response = await axios.post("http://127.0.0.1:8000/apply/", formPayload, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        }
      );

      if (response.status === 201) {
        navigate("/thank-you");
      }
    } catch (error) {
      console.error("Submission error:", error);
      
      let errorMessage = "Failed to submit application. Please try again.";
      if (error.response) {
        // Handle Django validation errors
        if (error.response.data) {
          errorMessage = Object.entries(error.response.data)
            .flatMap(([key, values]) => values)
            .join(" ") || errorMessage;
        }
      }
      
      setErrors(prev => ({ ...prev, submit: errorMessage }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="form-container">
      <h2>Job Application Form</h2>
      
      {errors.submit && <div className="error-alert">{errors.submit}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Full Name</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            className={errors.name ? "input-error" : ""}
          />
          {errors.name && <span className="error-text">{errors.name}</span>}
        </div>

        <div className="form-group">
          <label>Email Address</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            className={errors.email ? "input-error" : ""}
          />
          {errors.email && <span className="error-text">{errors.email}</span>}
        </div>

        <div className="form-group">
          <label>Phone Number</label>
          <input
            type="tel"
            name="phone"
            value={formData.phone}
            onChange={handleInputChange}
            className={errors.phone ? "input-error" : ""}
          />
          {errors.phone && <span className="error-text">{errors.phone}</span>}
        </div>

        <div className="form-group">
          <label>Upload Resume (PDF only, max 2MB)</label>
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileChange}
            className={errors.file ? "input-error" : ""}
          />
          {errors.file && <span className="error-text">{errors.file}</span>}
        </div>

        <button
          type="submit"
          className="submit-btn"
          disabled={loading}
        >
          {loading ? "Submitting..." : "Submit Application"}
        </button>
      </form>
    </div>
  );
};

// Add CSS (create a separate CSS file or use styled-components)
const styles = `
  .form-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  }

  .form-group {
    margin-bottom: 1.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
  }

  input {
    width: 100%;
    padding: 0.8rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
  }

  .input-error {
    border-color: #e53e3e;
  }

  .error-text {
    color: #e53e3e;
    font-size: 0.875rem;
    margin-top: 0.25rem;
    display: block;
  }

  .error-alert {
    background: #fed7d7;
    color: #c53030;
    padding: 1rem;
    border-radius: 4px;
    margin-bottom: 1.5rem;
  }

  .submit-btn {
    background: #3182ce;
    color: white;
    padding: 0.8rem 1.5rem;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    cursor: pointer;
    transition: background 0.2s;
  }

  .submit-btn:disabled {
    background: #a0aec0;
    cursor: not-allowed;
  }
`;

// Inject styles
document.head.insertAdjacentHTML('beforeend', `<style>${styles}</style>`);

export default ApplyForm;