import { useState } from "react";

import {
  createUserWithEmailAndPassword,
  signInWithPopup,
  signInWithRedirect,
  signOut,
} from "firebase/auth";
import { auth, googleProvider } from "../../config/firebase";

import "./Auth.scss";

const Auth = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const signIn = async () => {
    try {
      await createUserWithEmailAndPassword(auth, email, password);
      console.log("emailsignin");
    } catch (err) {
      console.error(err);
    }
  };

  const logout = async () => {
    try {
      await signOut(auth);
      console.log("logged out");
    } catch (err) {
      console.error(err);
    }
  };

  const signInWithGoogle = async () => {
    try {
      await signInWithPopup(auth, googleProvider);
      console.log("googlesignin");
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="login-container">
      <div>
        <input
          placeholder="Email..."
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          placeholder="Password..."
          type="password"
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={signIn}>Sign In</button>
        <button onClick={signInWithGoogle}>Sign in with Google</button>
        <button onClick={logout}>Log Out</button>
      </div>
      <div>
        <p>{auth?.currentUser?.email}</p>
        <img src={auth?.currentUser?.photoURL}></img>
      </div>
    </div>
  );
};

export default Auth;
