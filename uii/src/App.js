import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import "./Styles/ALL.css";
import Login from "./Login";
import SignUpNewUser from "./SignUpNewUser";
import AdminOptions from "./AdminOptions";
import ViewAdminProfile from "./ViewAdminProfile";
import Verification from "./Verification";
import LiveMonitoring from "./LiveMonitoring";
import UserProfile from "./UpdateUserProfile";
import AddCard from "./AddCard";

function App() {
  const navigate = useNavigate();

  const handleSignUpClick = () => {
    // Navigate to the SignUpNewUser page
    navigate("/signup");
  };

  return (
    <div className="App">
      <header className="App-header">
        <Routes>
          <Route path="/signup" element={<SignUpNewUser />} />
          <Route path="/admin-options" element={<AdminOptions />} />
          <Route path="/" element={<Login />} />
          <Route path="/view-profile" element={<ViewAdminProfile />} />
          <Route path="/accept-verification" element={<Verification />} />
          <Route path="/live-monitoring" element={<LiveMonitoring />} />
          <Route path="/update-profile" element={<UserProfile />} />
          <Route path="/add-card" element={<AddCard />} />
        </Routes>
      </header>
    </div>
  );
}

export default App;
