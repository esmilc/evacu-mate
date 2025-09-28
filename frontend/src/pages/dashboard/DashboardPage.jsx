import { useAuth0 } from "@auth0/auth0-react";

function DashboardPage() {
  const { user, logout } = useAuth0();

  return (
    <div style={{ padding: "2rem" }}>
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
    </div>
  );
}

export default DashboardPage;