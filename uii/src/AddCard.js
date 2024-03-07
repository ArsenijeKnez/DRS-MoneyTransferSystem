import React, { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";

const AddCard = () => {
  const [addCard, setAddCard] = useState("");

  const handleBack = () => {
    window.location.href = "/";
  };

  const handleAddCard = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("card", addCard);

    try {
      const response = await fetch("http://localhost:5000/user/addCard", {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        console.log("Successfully added card!");
        toast.success(data.ok || "Successfully added card!");
      } else {
        const errorData = await response.json();
        console.error("Add card failed!");
        toast.error(errorData.error || "Add card failed");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Network or server error!");
    }
  };

  return (
    <div>
      <div>
        <form onSubmit={handleAddCard}>
          <h2>Add card: </h2>
          <label>
            Card number:
            <input
              type="number"
              name="addCard"
              value={addCard}
              onChange={(e) => setAddCard(e.target.value)}
            />
          </label>
          <button type="submit">Add</button>
          <button onClick={handleBack}>Back</button>
        </form>
      </div>
      <ToastContainer />
    </div>
  );
};

export default AddCard;
