
import { useAuth0 } from "@auth0/auth0-react";


function AuthPage() {
    
  const { loginWithRedirect } = useAuth0();  

  return (
    <div style={{ padding: "2rem" }}>
      <h1> Welcome to Evacu-Mate </h1>  
      {/* <h2>Login / Signup</h2> */}
      <button
        onClick={() =>
          loginWithRedirect({
            redirect_uri: "http://localhost:5173/dashboard"
          })
        }
      >
        Log In / Sign Up
      </button>
    </div>
  );
}

export default AuthPage;