import { useAuth0 } from "@auth0/auth0-react";
import { useState, useEffect } from "react";

function DashboardPage() {
  const { user, logout } = useAuth0();
  const [message, setMessage] = useState("");
  const [shelters, setShelters] = useState([]);
  const [loading, setLoading] = useState(true);

  // Fetch shelters from backend on load
  useEffect(() => {
    const fetchShelters = async () => {
      try {
        const response = await fetch("http://localhost:8000/shelters");
        const data = await response.json();
        setShelters(data);
      } catch (err) {
        console.error("Error fetching shelters:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchShelters();
  }, []);

  // Handle Waymo request for a shelter
  const handleRequestWaymo = async (shelterId) => {
    try {
      const response = await fetch(`http://localhost:8000/request-waymo/${shelterId}`, {
        method: "POST",
      });
      const data = await response.json();
      setMessage(`🚗 Waymo dispatched! ETA: ${data.eta_minutes} min`);
    } catch (err) {
      console.error("Error requesting Waymo:", err);
      setMessage("❌ Failed to request Waymo");
    }
    setTimeout(() => setMessage(""), 5000);
  };

  return (
    <div className="dashboard-container" style={{ padding: "2rem" }}>
      <main className="main-panel">
        <div className="header">
          <div>
            <div className="title">Evacu-Mate Dashboard</div>
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
          <div className="card stat"><div className="value">2</div><div className="label">Active Alerts</div></div>
          <div className="card stat"><div className="value">12</div><div className="label">Available Vehicles</div></div>
          <div className="card stat"><div className="value">5</div><div className="label">Pending Requests</div></div>
          <div className="card stat"><div className="value">243</div><div className="label">Shelter Capacity</div></div>
        </section>

        <section style={{ marginTop: '1rem' }}>
          <div className="card">
            <h3 style={{ marginTop: 0 }}>Available Shelters</h3>
            {loading ? (
              <p>Loading shelters...</p>
            ) : shelters.length === 0 ? (
              <p>No shelters available</p>
            ) : (
              shelters.map((shelter) => (
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
                      onClick={() => handleRequestWaymo(shelter.id)}
                    >
                      Request Waymo
                    </button>
                  </div>
                </div>
              ))
            )}
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
