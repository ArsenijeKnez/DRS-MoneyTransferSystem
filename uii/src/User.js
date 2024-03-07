// User.js

import React, { useState, useEffect } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "./Styles/UserCards.css"

const User = () => {
  const [userCards, setUserCards] = useState([]);
  const [selectedCardDeposit, setSelectedCardDeposit] = useState({
    number: null,
    index: null,
  });
  const [selectedCardConvert, setSelectedCardConvert] = useState({
    number: null,
    currencyFrom: null,
    index: null,
  });
  const [check, setCheck] = useState("");
  const [amountConvert, setAmountConvert] = useState("");
  const [currencyConvert, setCurrencyConvert] = useState("rsd");
  const [selectedCardPay, setSelectedCardPay] = useState({
    number: null,
    currency: null,
    index: null,
  });
  const [amountPay, setAmountPay] = useState("");
  const [recipientCardPay, setRecipientCardPay] = useState("");
  const [recipientEmailPay, setRecipientEmailPay] = useState("");
  const [recipientNamePay, setRecipientNamePay] = useState("");
  const [recipientSurnamePay, setRecipientSurnamePay] = useState("");

  const fetchUserCards = async () => {
    try {
      const response = await fetch(
        "http://localhost:5000/user/balanceOverview",
        {
          method: "GET",
          credentials: "include",
        }
      );

      if (response.ok) {
        const dataString = await response.text();
        const data = JSON.parse(dataString);
        console.log("Fetched user cards:", data);
        setUserCards(data);
      } else {
        console.error("Failed to retrieve user cards!");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  useEffect(() => {
    fetchUserCards();
  }, []);

  const navigateToProfileUpdate = () => {
    window.location.href = "/update-profile";
  };

  const navigateToAddCard = () => {
    window.location.href = "/add-card";
  };

  const handleDeposit = (card, index) => {
    setSelectedCardDeposit({ number: card.number, index: index });
  };

  const handleDepositFormCancel = () => {
    setSelectedCardDeposit({ number: null, index: null });
    setCheck("");
  };

  const handleConvert = (card, index) => {
    setSelectedCardConvert({
      number: card.number,
      index: index,
      currencyFrom: card.currency,
    });
  };

  const handleConvertFormCancel = () => {
    setSelectedCardConvert({ number: null, index: null, currencyFrom: null });
    setAmountConvert("");
  };

  const handlePay = (card, index) => {
    setSelectedCardPay({
      number: card.number,
      index: index,
      currencyFrom: card.currency,
    });
  };

  const handlePayFormCancel = () => {
    setSelectedCardPay({ number: null, index: null, currencyFrom: null });
    setAmountPay("");
    setRecipientCardPay("");
  };

  const handleBackToLogin = () => {
    sessionStorage.clear();
    window.location.href = "/";
  };

  const handleDepositFormApply = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("card", selectedCardDeposit.number);
    formData.append("check", check);

    try {
      const response = await fetch("http://localhost:5000/user/MakeDeposit", {
        method: "PUT",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        toast.success(data.ok || "Successfully deposited funds!");
        fetchUserCards();
      } else {
        const errorData = await response.json();
        console.error("Deposit failed:", errorData);
        toast.error(errorData.error || "Deposit failed");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Network or server error");
    } finally {
      setSelectedCardDeposit({ number: null, index: null });
      setCheck("");
    }
  };

  const handleConvertFormApply = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("card", selectedCardConvert.number);
    formData.append("amount", amountConvert);
    formData.append("currencyFrom", selectedCardConvert.currencyFrom);
    formData.append("currencyTo", currencyConvert);

    try {
      const response = await fetch("http://localhost:5000/user/Convert", {
        method: "PUT",
        body: formData,
        credentials: "include",
      });

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        toast.success(data.ok || "Successfully converted funds!");
        fetchUserCards();
      } else {
        const errorData = await response.json();
        console.error("Convert failed:", errorData);
        toast.error(errorData.error || "Convert failed");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Network or server error");
    } finally {
      setSelectedCardConvert({ number: null, index: null, currencyFrom: null });
      setAmountConvert("");
    }
  };

  const handlePayFormApply = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("senderCardNum", selectedCardPay.number);
    formData.append("amount", amountPay);
    formData.append("currency", selectedCardPay.currencyFrom);
    formData.append("receiverCardNum", recipientCardPay);
    formData.append("receiverFirstName", recipientNamePay);
    formData.append("receiverLastName", recipientSurnamePay);
    formData.append("receiverEmail", recipientEmailPay);

    try {
      const response = await fetch(
        "http://localhost:5000/user/MakeTransaction",
        {
          method: "POST",
          body: formData,
          credentials: "include",
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log(data);
        toast.success(data.ok || "Successfully created transaction!");
        fetchUserCards();
      } else {
        const errorData = await response.json();
        console.error("Payment failed:", errorData);
        toast.error(errorData.error || "Payment failed");
      }
    } catch (error) {
      console.error("Error:", error);
      toast.error("Network or server error");
    } finally {
      setSelectedCardPay({ number: null, index: null, currencyFrom: null });
      setAmountPay("");
      setRecipientCardPay("");
    }
  };

  return (
    <div className="user-container">
      
      <div >
      <div className="usernavigation">
        <h2>Wellcome User</h2>
        <button onClick={navigateToProfileUpdate}>Update Profile </button>
        <button onClick={navigateToAddCard}>Add Card</button>
        <button onClick={handleBackToLogin}>Back to Login</button>
      </div>
      <table border="1" className="userTable">
          <thead>
            <tr>
              <th colSpan="7">User Cards</th>
            </tr>
            <tr>
              
              <th>Card Number</th>
              <th>Currency</th>
              <th>Amount</th>
              <th colSpan="3">User Card Options</th>
            </tr>
          </thead>
          <tbody>
            {userCards.map((card, index) => (
              <tr key={index}>
                
                <td>{card.number}</td>
                <td>{card.currency}</td>
                <td>{card.amount}</td>
                <td>
                  <button onClick={() => handleDeposit(card, index)}>
                    Deposit
                  </button>
                </td>
                <td>
                  <button onClick={() => handleConvert(card, index)}>
                    Convert
                  </button>
                </td>
                <td>
                  <button onClick={() => handlePay(card, index)}>
                    Transaction
                    </button>
                </td>
                {selectedCardDeposit &&
                  selectedCardDeposit.number === card.number &&
                  selectedCardDeposit.index === index && (
                    <td colSpan="4">
                      <div>
                        <form onSubmit={handleDepositFormApply}>
                          <label>
                          Enter the Payment Check:
                            <input
                              type="text"
                              name="check"
                              value={check}
                              onChange={(e) => setCheck(e.target.value)}
                              required
                            />
                          </label>
                          <div className="button-container">
                            <button type="submit">Apply</button>
                            <button
                              type="button"
                              onClick={handleDepositFormCancel}
                            >
                              Cancel
                            </button>
                          </div>
                        </form>
                      </div>
                    </td>
                  )}
                {selectedCardConvert &&
                  selectedCardConvert.number === card.number &&
                  selectedCardConvert.index === index && (
                    <td colSpan="4">
                      <div>
                        <form onSubmit={handleConvertFormApply}>
                          
                          <label>
                            Amount to Convert:
                            <input
                              type="text"
                              name="amount"
                              value={amountConvert}
                              onChange={(e) => setAmountConvert(e.target.value)}
                              required
                            />
                          </label>
                          <label>
                            Currency:
                            <select
                              name="currency"
                              value={currencyConvert}
                              onChange={(e) =>
                                setCurrencyConvert(e.target.value)
                              }
                              required
                            >
                              <option value="rsd">RSD</option>
                              <option value="eur">EUR</option>
                              <option value="usd">USD</option>
                            </select>
                          </label>
                          <div className="button-container">
                            <button type="submit">Apply</button>
                            <button
                              type="button"
                              onClick={handleConvertFormCancel}
                            >
                              Cancel
                            </button>
                          </div>
                        </form>
                      </div>
                    </td>
                  )}
                {selectedCardPay &&
                  selectedCardPay.number === card.number &&
                  selectedCardPay.index === index && (
                    <td colSpan="4">
                      <div>
                        <form onSubmit={handlePayFormApply}>
                        <label>Insert Data for the Transaction</label>
                          <label>
                            Amount:
                            <input
                              type="number"
                              name="amount"
                              value={amountPay}
                              onChange={(e) => setAmountPay(e.target.value)}
                              required
                            />
                          </label>
                          <label>
                            Recipient card:
                            <input
                              type="number"
                              name="recipientCard"
                              value={recipientCardPay}
                              onChange={(e) =>
                                setRecipientCardPay(e.target.value)
                              }
                            />
                          </label>
                          <label>
                            Recipient email:
                            <input
                              type="text"
                              name="recipientEmail"
                              value={recipientEmailPay}
                              onChange={(e) =>
                                setRecipientEmailPay(e.target.value)
                              }
                            />
                          </label>
                          <label>
                            Recipient name:
                            <input
                              type="text"
                              name="recipientName"
                              value={recipientNamePay}
                              onChange={(e) =>
                                setRecipientNamePay(e.target.value)
                              }
                            />
                          </label>
                          <label>
                            Recipient surname:
                            <input
                              type="text"
                              name="recipientSurname"
                              value={recipientSurnamePay}
                              onChange={(e) =>
                                setRecipientSurnamePay(e.target.value)
                              }
                            />
                          </label>
                          <div className="button-container">
                            <button type="submit">Apply</button>
                            <button
                              type="button"
                              onClick={handlePayFormCancel}
                            >
                              Cancel
                            </button>
                          </div>
                        </form>
                      </div>
                    </td>
                  )}
              </tr>
            ))}
          </tbody>
          <tfoot>
            <tr>
              <td colSpan="6">
                <button onClick={fetchUserCards} colSpan="4">
                  Refresh
                </button>
              </td>
            </tr>
          </tfoot>
        </table>
      </div>
      <ToastContainer />
    </div>
  );
};

export default User;
