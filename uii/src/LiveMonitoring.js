import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import "./Styles/signup.css";

const LiveMonitoring = () => {
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    var socket = io.connect("http://localhost:5000");

    socket.on("connect", () => {
      console.log("Connected to the server!");
    });

    // Listen for incoming transactions
    socket.on("freshly_executed_transactions", (newTransactions) => {
      console.log("Received transactions");

      if (newTransactions) {
        setTransactions((prevTransactions) => [
          ...prevTransactions,
          ...newTransactions,
        ]);
      }
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const handleBack = () => {
    window.location.href = "/";
  };

  return (
    <div className="liveMonitoring-container">
      <table className="monitoring-table">
        <caption>Live Monitoring</caption>
        <tbody>
          {transactions.length === 0 ? (
            <tr>
              <td>No incoming transactions yet</td>
            </tr>
          ) : (
            <tr>
              <td>
                <ul>
                  {transactions.map((transactionObject) => (
                    <li key={transactionObject.transaction.transactionId}>
                      <p>
                        Transaction ID:{" "}
                        {transactionObject.transaction.transactionId}
                      </p>
                      <p>Sender: {transactionObject.sender.email}</p>
                      <p>Receiver: {transactionObject.receiver.email}</p>
                      <p>Currency: {transactionObject.transaction.currency}</p>
                      <p>
                        Sent Amount: {transactionObject.transaction.sentAmount}
                      </p>
                      <p>
                        Date and Time:{" "}
                        {transactionObject.transaction.dateAndTime}
                      </p>
                    </li>
                  ))}
                </ul>
              </td>
            </tr>
          )}
          <tr>
            <td>
              <button onClick={handleBack}>Back</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default LiveMonitoring;
