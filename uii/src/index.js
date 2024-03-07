// index.js ili App.js (ulazna tačka vaše aplikacije)

import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter } from "react-router-dom";
import App from "./App"; // Zamenite putanjom do vaše glavne App komponente

ReactDOM.render(
  <BrowserRouter>
    <App />
  </BrowserRouter>,
  document.getElementById("root")
);
