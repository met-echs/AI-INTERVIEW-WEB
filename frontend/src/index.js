import React from "react";
import ReactDOM from "react-dom/client"; // Use ReactDOM from 'react-dom/client'
import App from "./App";
import "./index.css";

const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement); // Use createRoot instead of render

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
