import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import App from './pages/App';
import Login from './pages/login/LoginView';
import AdminView from './pages/admin/AdminView';
import About from './pages/About';
import ResetPassword from './pages/ResetPassword';
import NotFound from './pages/NotFound';
import ForgotPass from './pages/ForgotPass';

import './components/popup.css'
import Profile from './pages/profile/Profile';
import SignUp from './pages/Signup';


const router = createBrowserRouter([
  {
    path: "/",
    element: <App />
  },
  {
    path: "/login",
    element: <Login />
  },
  {
    path: "/signup",
    element: <SignUp />
  },
  {
    path: "/admin",
    element: <AdminView />
  },
  {
    path: "/about",
    element: <About />
  },
  {
    path: "/profile",
    element: <Profile />
  },
  {
    path: "/forgot-password",
    element: <ForgotPass />
  },
  {
    path: "/reset-password",
    element: <ResetPassword />
  },  
  {
    path: "*",
    element: <NotFound />
  }
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);