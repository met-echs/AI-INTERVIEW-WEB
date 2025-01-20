import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Use useNavigate for modern react-router-dom

const Apply = () => {
  const navigate = useNavigate(); // Use useNavigate instead of useHistory
  const [fileError, setFileError] = useState("");
  const [file, setFile] = useState(null);
  const maxFileSize = 2 * 1024 * 1024; // 2 MB in bytes

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.size > maxFileSize) {
        setFileError("File size must not exceed 2 MB");
        setFile(null); // Clear the file if it exceeds size
      } else {
        setFileError(""); // Clear any previous errors
        setFile(selectedFile);
      }
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!file) {
      alert("Please upload a valid file.");
      return;
    }

    alert("Details submitted!");
    navigate("/thank-you"); // Use navigate instead of history.push
  };

  return (
    <div
      style={{
        padding: "30px",
        maxWidth: "560px",
        margin: "60px auto",
        textAlign: "center",
        backgroundColor: "#fff",
        borderRadius: "10px",
        boxShadow: "0 0 20px rgba(0,0,0,0.1)", // Shadow copied from login page
      }}
    >
      <h2 style={{ marginBottom: "20px" }}>
        <strong>Fill the details</strong>
      </h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          required
          style={styles.input}
        />
        <input
          type="email"
          placeholder="Email address"
          required
          style={styles.input}
        />
        <input
          type="tel"
          placeholder="Phone no."
          required
          style={styles.input}
        />
        <input
          type="file"
          accept=".pdf"
          required
          onChange={handleFileChange}
          style={{
            ...styles.input,
            marginBottom: "10px", // Additional spacing for the file input
          }}
        />
        {fileError && <p style={{ color: "red", marginBottom: "10px" }}>{fileError}</p>}
        <p style={{ marginBottom: "20px" }}>File format must be pdf.</p>
        <button
          type="submit"
          style={styles.button}
        >
          Apply now
        </button>
      </form>
    </div>
  );
};

const styles = {
  input: {
    display: "block",
    width: "96%",
    marginBottom: "15px",
    padding: "10px",
    border: "1px solid #ccc",
    borderRadius: "5px",
    boxSizing: "border-box",
  },
  button: {
    backgroundColor: "#3498db",
    color: "#fff",
    padding: "10px 20px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
    boxShadow: "0 4px 8px rgba(0,0,0,0.2)", // Adding subtle shadow to the button
  },
};

export default Apply;
