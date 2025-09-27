// import { useState } from 'react'
import AuthPage from './pages/auth/authPage';
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import './App.css';
import {useAuth0} from "@auth0/auth0-react";
import DashboardPage from './pages/dashboard/DashboardPage';

function App() {
  const { isAuthenticated } = useAuth0();

  return(
    <Router>
      <Routes>
        <Route
        path = "/"
        element={isAuthenticated ? <DashboardPage /> : <AuthPage />}
        />
        <Route
        path = "/dashboard"
        element = {isAuthenticated ? <DashboardPage /> : <AuthPage />}
        />
      </Routes>
    </Router>
  );
}

export default App
