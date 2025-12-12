
import { type FormEvent } from "react";
import { useSetupMutation } from "./setupApiSlice";
import './Setup.css';
import catMascot from '../assets/mascot.png';
import { setUsername, setPassword, setNetworkName, setNetworkPassword } from "./setupSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";

export const Setup = () => {
  const [setup, { isLoading, isError }] = useSetupMutation();
  const dispatch = useAppDispatch();
  const state = useAppSelector(state => state.setup)

  const onSubmit = (e: FormEvent) => {
    e.preventDefault()
    setup(state)

  }

  return (
    <div className="setup-page">
      <form className="setup-card" onSubmit={onSubmit}>

        <img src={catMascot} alt="cat mascot" className="mascot" />

        <h2 className="title">Ostara Cam</h2>

        <input
          className="input"
          placeholder="network name"
          value={state.networkName}
          onChange={e => dispatch(setNetworkName(e.target.value))}
        />

        <input
          className="input"
          placeholder="network password"
          value={state.networkPassword}
          onChange={e => dispatch(setNetworkPassword(e.target.value))}
        />

        <input
          className="input"
          placeholder="username"
          value={state.username}
          onChange={e => dispatch(setUsername(e.target.value))}
        />

        <input
          className="input"
          type="password"
          placeholder="password"
          value={state.password}
          onChange={e => dispatch(setPassword(e.target.value))}
        />

        <button className="setup-button" type="submit" disabled={isLoading}>
          Submit
        </button>

        {isError && <div className="error">Setup failed</div>}
      </form>
    </div>
  )
}
