import React, { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "./Styles/UserCards.css"


const UserProfile = () => {
  const [userInfo, setUserInfo] = useState([]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserInfo({
      ...userInfo,
      [name]: value,
    });
  };

  const handleBack = () => {
    window.location.href = "/";
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", userInfo.email);
    formData.append("password", userInfo.lozinka);
    formData.append("firstName", userInfo.ime);
    formData.append("lastName", userInfo.prezime);

    try {
      const response = await fetch("http://localhost:5000/user/updateProfile", {
        method: "PUT",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        console.log("Successfully updated profile!");
        toast.success(data.ok || "Successfully updated profile!");
      } else {
        const errorData = await response.json();
        console.error("Update profile failed!");
        toast.error(errorData.error || "Update profile failed!");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Error:", error);
    }
  };

  return (
    <div >
      <form onSubmit={handleProfileUpdate}  >    
           
        <h2 className="h2Us">Update User Profile</h2>
        <br />

        <label>
          First Name:
          <input className="inputUser"
            type="text"
            name="ime"
            value={userInfo.ime}
            onChange={handleInputChange}
            required
          />
        </label>
        <label>
          Last Name:
          <input className="inputUser"
            type="text"
            name="prezime"
            value={userInfo.prezime}
            onChange={handleInputChange}
            required
          />
        </label>
      
        <label>
          Email:
          <input className="inputUser"
            type="email"
            name="email"
            value={userInfo.email}
            onChange={handleInputChange}
            required
          />
        </label>
        
        <label>
          Password:
          <input className="inputUser"
            type="password"
            name="lozinka"
            value={userInfo.lozinka}
            onChange={handleInputChange}
            required
          />
        </label>
        <button type="submit">Update Profile</button>
        <button onClick={handleBack}>Back</button>
      </form>
      <ToastContainer />
    </div>
  );
};

export default UserProfile;
