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
    <div className="dashboard-container" style={{ padding: "2rem" }}>
      <main className="main-panel">
        <div className="header">
          <div>
            <div className="title">Evacu‑Mate Dashboard</div>
            <div className="subtitle">Real-time evacuation orchestration & monitoring</div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
            <div style={{ textAlign: 'right' }}>
              {user && <div style={{ fontSize: '0.9rem', color: '#083344' }}>{user.name}</div>}
              {user && <div style={{ fontSize: '0.75rem', color: '#1e3a8a' }}>{user.email}</div>}
            </div>
            <div className="pulse" title="Live activity"></div>
          </div>
        </div>

        <section className="cards-grid">
          <div className="card stat">
            <div className="value">2</div>
            <div className="label">Active Alerts</div>
          </div>
          <div className="card stat">
            <div className="value">12</div>
            <div className="label">Available Vehicles</div>
          </div>
          <div className="card stat">
            <div className="value">5</div>
            <div className="label">Pending Requests</div>
          </div>
          <div className="card stat">
            <div className="value">243</div>
            <div className="label">Shelter Capacity</div>
          </div>
        </section>

        <section style={{ marginTop: '1rem' }}>
          <div className="card">
            <h3 style={{ marginTop: 0 }}>Available Shelters</h3>
            {shelters.map((shelter) => (
              <div key={shelter.id} style={{ marginTop: '0.75rem', padding: '0.75rem', borderRadius: 8, background: 'rgba(255,255,255,0.9)' }}>
                <h4 style={{ margin: 0 }}>{shelter.name}</h4>
                <p style={{ margin: '0.25rem 0' }}>{shelter.address}</p>
                <p style={{ margin: 0 }}>Capacity: {shelter.capacity}</p>
                <div style={{ marginTop: '0.5rem' }}>
                  <button
                    style={{
                      marginTop: '0.5rem',
                      background: '#007bff',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      padding: '0.45rem 0.85rem',
                      cursor: 'pointer',
                    }}
                    onClick={() => handleRequestWaymo(shelter.name)}
                  >
                    Request Waymo
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>

        {message && (
          <div className="card" style={{ marginTop: '1rem', background: '#e6ffe6', border: '1px solid #00cc00', color: '#006600' }}>
            {message}
          </div>
        )}
      </main>

      <aside className="side-panel">
        <div className="card">
          <h4 style={{ marginTop: 0 }}>Quick Actions</h4>
          <button style={{ width: '100%', padding: '0.6rem', borderRadius: 8, border: 'none', background: '#38bdf8', color: '#012a4a', cursor: 'pointer' }}>
            Trigger Evacuation Drill
          </button>
          <div style={{ height: '0.75rem' }} />
          <button style={{ width: '100%', padding: '0.6rem', borderRadius: 8, border: '1px solid rgba(2,46,76,0.06)', background: '#fff', color: '#023e8a', cursor: 'pointer' }}>
            Sync Fleet Status
          </button>
        </div>

        <div style={{ height: '1rem' }} />

        <div className="card">
          <h4 style={{ marginTop: 0 }}>User</h4>
          {user ? (
            <>
              <p style={{ margin: 0 }}>{user.name}</p>
              <p style={{ marginTop: '0.5rem' }}><button onClick={() => logout({ returnTo: window.location.origin })}>Log Out</button></p>
            </>
          ) : (
            <p style={{ margin: 0 }}>Not signed in</p>
          )}
        </div>
      </aside>
    </div>
  );
}

export default DashboardPage;