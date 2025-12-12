
import { useState, type FormEvent } from "react";
// import { useLoginMutation } from "./authApiSlice";
import './Setup.css';
import catMascot from '../assets/mascot.png';
import setupSlice, { setUsername, setPassword, setNetworkName, setNetworkPassword } from "./setupSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";

export const Setup = () => {
  //   const [login, { isLoading, isError }] = useLoginMutation()
  const dispatch = useAppDispatch();

  const {
    username,
    password,
    networkName,
    networkPassword,
  } = useAppSelector(state => state.setup)

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    // login({ username, password })
  }

  return (
    <div className="setup-page">
      <form className="setup-card" onSubmit={onSubmit}>

        <img src={catMascot} alt="cat mascot" className="mascot" />

        <h2 className="title">Ostara Cam</h2>

        <input
          className="input"
          placeholder="network name"
          value={networkName}
          onChange={e => dispatch(setNetworkName(e.target.value))}
        />

        <input
          className="input"
          placeholder="network password"
          value={networkPassword}
          onChange={e => dispatch(setNetworkPassword(e.target.value))}
        />

        <input
          className="input"
          placeholder="username"
          value={username}
          onChange={e => dispatch(setUsername(e.target.value))}
        />

        <input
          className="input"
          type="password"
          placeholder="password"
          value={password}
          onChange={e => dispatch(setPassword(e.target.value))}
        />

        <button className="setup-button" type="submit" disabled={false}>
          Submit
        </button>

        {/* {isError && <div className="error">Login failed</div>} */}
      </form>
    </div>
  )
}
