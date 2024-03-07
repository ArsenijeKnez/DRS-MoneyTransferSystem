// ViewProfile.js
import React, { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "./Styles/admin.css";

const ViewProfile = () => {
  const [adminData, setAdminData] = useState({
    firstName: "",
    lastName: "",
    address: "",
    city: "",
    country: "",
    phoneNum: "",
    email: "",
    password: "",
  });

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const response = await fetch(
          "http://localhost:5000/getLogedInUserData",
          {
            method: "GET",
            credentials: "include",
          }
        );

        if (response.ok) {
          const data = await response.json();
          if (data.length > 0) {
            setAdminData(data[0]);
            console.log(data[0]);
          }
        } else {
          const errorData = await response.json();
          console.error("Failed to fetch admin profile!");
          toast.error(errorData.error || "Failed to fetch admin profile!");
        }
      } catch (error) {
        console.error("Error:", error);
        toast.error("Network or server error!");
      }
    };

    fetchAdminData();
  }, []);

  const handleBack = () => {
    window.location.href = "/admin-options";
  };

  return (
    <div>
  <form>
    <table>
      <caption>Admin Profile</caption>
      <tr>
        <td><label>First Name:</label></td>
        <td><input type="text" value={adminData.firstName} readOnly /></td>
      </tr>
      <tr>
        <td><label>Last Name:</label></td>
        <td><input type="text" value={adminData.lastName} readOnly /></td>
      </tr>
      <tr>
        <td><label>Address:</label></td>
        <td><input type="text" value={adminData.address} readOnly /></td>
      </tr>
      <tr>
        <td><label>City:</label></td>
        <td><input type="text" value={adminData.city} readOnly /></td>
      </tr>
      <tr>
        <td><label>Country:</label></td>
        <td><input type="text" value={adminData.country} readOnly /></td>
      </tr>
      <tr>
        <td><label>Phone Number:</label></td>
        <td><input type="text" value={adminData.phoneNum} readOnly /></td>
      </tr>
      <tr>
        <td><label>Email:</label></td>
        <td><input type="text" value={adminData.email} readOnly /></td>
      </tr>
      <tr>
        <td><label>Password:</label></td>
        <td><input type="password" value={adminData.password} readOnly /></td>
      </tr>
    </table>
  </form>
  <button onClick={handleBack}>Back</button>
  <ToastContainer />
</div>


  );
};

export default ViewProfile;
