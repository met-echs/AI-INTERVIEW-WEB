import React, { useState } from "react";
import axios from "axios";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false); // Toggle password visibility

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post("http://localhost:5000/login", {
        email,
        password,
      });
      if (response.status === 200) {
        setUser(response.data);
        setError("");
      }
    } catch (error) {
      setError("Invalid email or password. Please try again.");
    }
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
        boxShadow: "0 0 20px rgba(0,0,0,0.1)",
      }}
    >
      <h2><strong>Welcome back</strong></h2>
      <p>Please enter your details to sign in.</p>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Enter your email..."
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={styles.input}
        />
        <div style={{ position: "relative" }}>
          <input
            type={showPassword ? "text" : "password"}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            style={styles.input}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            style={styles.toggleButton}
          >
            {showPassword ? "Hide" : "Show"}
          </button>
        </div>
        <button type="submit" style={styles.button}>
          Login
        </button>
      </form>
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
      {user && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <h3>User Details</h3>
          <p>
            <strong>Full Name:</strong> {user.fullname}
          </p>
          <p>
            <strong>Phone Number:</strong> {user.phone}
          </p>
          <p>
            <strong>Email:</strong> {user.email}
          </p>
          <p>
            <strong>Message:</strong> {user.msg}
          </p>
        </div>
      )}
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
  },
  button: {
    backgroundColor: "#3498db",
    color: "white",
    border: "2px solid #3498db",
    padding: "10px 20px",
    cursor: "pointer",
    borderRadius: "5px",
  },
  toggleButton: {
    position: "absolute",
    right: "30px",
    top: "10px",
    backgroundColor: "transparent",
    border: "none",
    cursor: "pointer",
    color: "black",
  },
};

export default Login;
