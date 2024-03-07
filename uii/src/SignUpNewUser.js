import React, { useState } from "react";
import { ToastContainer,toast } from "react-toastify";
import "./Styles/signup.css";


const UserRegistration = ({ history }) => {
  const [userData, setUserData] = useState({
    ime: "",
    prezime: "",
    adresa: "",
    grad: "",
    drzava: "",
    brojTelefona: "",
    email: "",
    lozinka: "",
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserData({
      ...userData,
      [name]: value,
    });
  };

  const handleRegistration = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", userData.email);
    formData.append("password", userData.lozinka);
    formData.append("firstName", userData.ime);
    formData.append("lastName", userData.prezime);

    try {
      const response = await fetch("http://localhost:5000/admin/create-user", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {       
        const data = await response.json();        
        console.log("Successfully added a new user:", data.message);
        toast.success(data.ok || "Successfully added a new user!");
      } else {
        const errorData = await response.json();
        console.error("Registration failed!");
        toast.error(errorData.error || "Registration failed!");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Network or server error!");
    }
  };

  const handleBack = () => {
    window.location.href = "/admin-options";
  };

  return (
    <div className="user-registration-container">
    <form className="form" onSubmit={handleRegistration}>
      <table>
        <caption>User Registration</caption><br/>
        <tr>
          <td><label>First Name:</label></td>
          <td><input type="text" name="ime" placeholder="Enter first name..."
          value={userData.ime} onChange={handleInputChange} required /></td>
        </tr>
        <tr>
          <td><label>Last Name:</label></td>
          <td><input type="text" name="prezime" placeholder="Enter last name..."
          value={userData.prezime} onChange={handleInputChange} required /></td>
        </tr>
        <tr>
          <td><label>Email:</label></td>
          <td><input type="email" name="email" placeholder="Enter email..."
          value={userData.email} onChange={handleInputChange} required /></td>
        </tr>
        <tr>
          <td><label>Password:</label></td>
          <td><input type="password" name="lozinka" placeholder="Enter password..."
           value={userData.lozinka} onChange={handleInputChange} required /></td>
        </tr>
        <tr>
          <td colSpan="2"><button type="submit">Register</button></td>
        </tr>
        <tr>
          <td colSpan="2"><button onClick={handleBack}>Back</button></td>
        </tr>
      </table>
    </form>
    <ToastContainer />
  </div>
  
  );
};

export default UserRegistration;
