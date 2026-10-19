import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./styles.css";

const root = document.getElementById("root");
const page = root?.dataset.page || "home";

createRoot(root).render(
  <StrictMode>
    <App page={page} />
  </StrictMode>,
);
