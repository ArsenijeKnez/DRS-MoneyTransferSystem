import React, { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import AdminOptions from "./AdminOptions";
import User from "./User";


const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");
  const [loggedInUser, setLoggedInUser] = useState(false);
  const [loggedInAdmin, setLoggedInAdmin] = useState(false);

  useEffect(() => {
    const storedEmail = sessionStorage.getItem("email");
    const storedRole = sessionStorage.getItem("role");

    if (storedEmail && storedRole) {
      if (storedRole === "user") {
        setLoggedInUser(true);
      } else if (storedRole === "admin") {
        setLoggedInAdmin(true);
      }
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);
    formData.append("role", role);

    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        if (role == "user") {
          sessionStorage.setItem("email", email);
          sessionStorage.setItem("role", role);
          setLoggedInUser(true);
        } else {
          sessionStorage.setItem("email", email);
          sessionStorage.setItem("role", role);
          setLoggedInAdmin(true);
        }
      } else {
        const errorData = await response.json();
        console.error("Login failed!");
        toast.error(errorData.error || "Login failed");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Network or server error!");
    }
  };

  return (
    <div>
      {loggedInAdmin ? (
        <AdminOptions />
      ) : loggedInUser ? (
        <User />
      ) : (
        <div className="Login">
          <form onSubmit={handleSubmit}>
            <h2>Login</h2>
            <table>
              <tbody>
                <tr>
                  <td>Email:</td>
                  <td>
                    <input
                      type="text"
                      value={email}
                      placeholder="Enter email.."
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <td>Password:</td>
                  <td>
                    <input
                      type="password"
                      value={password}
                      placeholder="Enter password.."
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </td>
                </tr>

                <tr>
                  <td style={{ verticalAlign: "middle" }}>Role:</td>
                  <td>
                    <div style={{ display: "flex", alignItems: "center" }}>
                      <label
                        style={{
                          marginRight: "10px",
                          position: "relative",
                          top: "2px",
                        }}
                      >
                        Admin
                        <input
                          type="radio"
                          name="role"
                          value="admin"
                          checked={role === "admin"}
                          onChange={(e) => setRole(e.target.value)}
                          style={{ transform: "scale(1.5)" }}
                        />
                      </label>
                      <label style={{ position: "relative", top: "2px" }}>
                        User
                        <input
                          type="radio"
                          name="role"
                          value="user"
                          checked={role === "user"}
                          onChange={(e) => setRole(e.target.value)}
                          style={{ transform: "scale(1.5)" }}
                        />
                      </label>
                    </div>
                  </td>
                </tr>

                <tr>
                  <td colSpan={2}>
                    <button type="submit">Login</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </form>
        </div>
      )}
      <ToastContainer />
    </div>
  );
};

export default Login;
