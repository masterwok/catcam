import { useState, type FormEvent } from "react";
import { useLoginMutation } from "./authApiSlice";

export const Login = () => {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [login, { isLoading, isError }] = useLoginMutation()

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    login({ username, password })   // token is stored automatically
  }

  return (
    <form onSubmit={onSubmit}>
      <h2>Login</h2>

      <input
        value={username}
        onChange={e => setUsername(e.target.value)}
      />

      <input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />

      <button type="submit" disabled={isLoading}>
        Login
      </button>

      {isError && <div>Login failed</div>}
    </form>
  )
}
