import { useState, type FormEvent } from "react";
import { useLoginMutation } from "./authApiSlice";
import './Login.css';
import catMascot from '../assets/mascot.png'; 

export const Login = () => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [login, { isLoading, isError }] = useLoginMutation()

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    login({ username, password })
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={onSubmit}>

        <img src={catMascot} alt="cat mascot" className="mascot" />

        <h2 className="title">Ostara Cam</h2>

        <input
          className="input"
          placeholder="username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />

        <input
          className="input"
          type="password"
          placeholder="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />

        <button className="login-button" type="submit" disabled={isLoading}>
          Login
        </button>

        {isError && <div className="error">Login failed</div>}
      </form>
    </div>
  )
}
