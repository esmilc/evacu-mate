import { useAuth0 } from "@auth0/auth0-react";

function AuthPage() {
  const { loginWithRedirect, logout, isAuthenticated, user } = useAuth0();

  return (
    <div>
      {!isAuthenticated ? (
        <>
          <h1> Welcome to Evacumate </h1>
          
          <button onClick={() => loginWithRedirect()}>Log In / Sign Up</button>
        </>
      ) : (
        <>
          <h2>Welcome, {user.name}</h2>
          <button onClick={() => logout({ returnTo: window.location.origin })}>
            Log Out
          </button>
        </>
      )}
    </div>
  );
}

export default AuthPage;