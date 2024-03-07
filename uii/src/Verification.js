import React, { useEffect, useState } from "react";
import { ToastContainer, toast } from "react-toastify";

const Verification = () => {
  const [unverifiedCards, setUnverifiedCards] = useState([]);

  const handleVerify = async (card, index) => {
    const verifyCard = async () => {
      const formData = new FormData();
      formData.append("card", card.number);

      try {
        const response = await fetch(
          "http://localhost:5000/admin/verifyAccount",
          {
            method: "PUT",
            body: formData,
            credentials: "include",
          }
        );

        if (response.ok) {
          const data = await response.json();
          console.log(data);
          toast.success(data.ok || "Successfully verified card!");
          fetchUnverifiedCards();
        } else {
          const errorData = await response.json();
          console.error("Verification failed: ", errorData);
          toast.error(errorData.error || "Verification failed!");
        }
      } catch (error) {
        console.error("Error", error);
      }
    };

    // Call the asynchronous function immediately
    verifyCard();

    console.log("Card Verified:", card);
  };

  const fetchUnverifiedCards = async () => {
    try {
      const response = await fetch(
        "http://localhost:5000/admin/getUnverifiedCardsWithOwner",
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (response.ok) {
        const dataString = await response.text();
        const data = JSON.parse(dataString);
        console.log("Fetched unverified cards:", data);
        setUnverifiedCards(data);
      } else {
        console.error("Failed to retrieve unverified cards!");
      }
    } catch (error) {
      console.error("Error: ", error);
    }
  };

  useEffect(() => {
    fetchUnverifiedCards();
  }, []);

  const handleBack = () => {
    window.location.href = "/";
  };

  return (
    <div className="verification">
      <table className="verification-table">
        <caption>Unverified Cards</caption><br/>
        <tbody>
          {unverifiedCards.length === 0 ? (
            <tr>
              <td>No unverified cards yet...<br/>(add a card to your account)</td>
            </tr>
          ) : (
            <tr>
              <td>
                <ul>
                  {unverifiedCards.map((card, index) => (
                    <li key={index}>
                      <strong>Card Number:</strong> <br/>{card.number}<br/>
                      <strong> Email:</strong><br/> {card.email}<br/>
                      <button onClick={() => handleVerify(card, index)}>
                        Verify
                      </button>
                    </li>
                  ))}
                </ul>
              </td>
            </tr>
          )}
          <tr>
            <td>
              <button onClick={fetchUnverifiedCards}>Refresh</button>
            </td>
          </tr>
          <tr>
            <td>
              <button onClick={handleBack}>Back</button>
            </td>
          </tr>
        </tbody>
      </table>
      <ToastContainer />
    </div>
  );
};

export default Verification;
