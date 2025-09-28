import { useAuth0 } from "@auth0/auth0-react";
import { useState } from "react";

function DashboardPage() {
  const { user, logout } = useAuth0();
  const [message, setMessage] = useState("");

  const shelters = [
    { id: "s1", name: "Miami High School Shelter", address: "202 Palm Blvd, Miami, FL", capacity: 100 },
    { id: "s2", name: "Downtown Community Center", address: "99 City Ave, Miami, FL", capacity: 50 },
    { id: "s3", name: "Westside Recreation Center", address: "45 Sunset Dr, Miami, FL", capacity: 75 },
  ];

  const handleRequestWaymo = (shelterName) => {
    setMessage(`🚗 Waymo dispatched to ${shelterName}! ETA: 10 min`);
    setTimeout(() => setMessage(""), 5000);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "0 auto" }}>
      <h1>Dashboard</h1>

      {user && (
        <>
          <p>Welcome, {user.name}!</p>
          <p>Email: {user.email}</p>
          <button onClick={() => logout({ returnTo: window.location.origin })}>
            Log Out
          </button>
        </>
      )}

      <h2 style={{ marginTop: "2rem" }}>Available Shelters</h2>
      {shelters.map((shelter) => (
        <div
          key={shelter.id}
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "1rem",
            marginTop: "1rem",
            background: "white",
          }}
        >
          <h3>{shelter.name}</h3>
          <p>{shelter.address}</p>
          <p>Capacity: {shelter.capacity}</p>
          <button
            style={{
              marginTop: "0.5rem",
              background: "#007bff",
              color: "white",
              border: "none",
              borderRadius: "5px",
              padding: "0.5rem 1rem",
              cursor: "pointer",
            }}
            onClick={() => handleRequestWaymo(shelter.name)}
          >
            Request Waymo
          </button>
        </div>
      ))}

      {message && (
        <div
          style={{
            marginTop: "1rem",
            padding: "0.5rem",
            background: "#e6ffe6",
            border: "1px solid #00cc00",
            borderRadius: "5px",
            color: "#006600",
          }}
        >
          {message}
        </div>
      )}
    </div>
  );
}

export default DashboardPage;