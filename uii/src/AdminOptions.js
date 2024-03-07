import React from "react";
//import './Styles/admin.css';

const AdminOptions = () => {
  const navigateToSignUp = () => {
    window.location.href = "/signup";
  };

  const navigateToLiveMonitoring = () => {
    window.location.href = "/live-monitoring";
  };

  const navigateToAcceptVerification = () => {
    window.location.href = "/accept-verification";
  };

  const navigateBackToLogin = () => {
    sessionStorage.clear();
    window.location.href = "/"; // Adjust the path as needed
    
  };
  const navigateToViewProfile = () => {
    window.location.href = "/view-profile"; // Dodajte ovu liniju
  };

  return (
    <div >
      <h1>Welcome admin!</h1>

      <div className="adminOptions">
        <button onClick={navigateToViewProfile}>View Profile</button>
        <br />
        <button onClick={navigateToSignUp}>Sign up new user</button>
        <br />

        <button onClick={navigateToLiveMonitoring}>Live Transactions</button>
        <br />

        <button onClick={navigateToAcceptVerification}>
          Accept Verification
        </button>
        <br />

        <button onClick={navigateBackToLogin}>Back to Login</button>
      </div>
    </div>
  );
};

export default AdminOptions;
