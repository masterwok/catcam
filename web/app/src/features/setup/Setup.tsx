
import { type FormEvent } from "react";
import { useSetupMutation } from "./setupApiSlice";
import './Setup.css';
import catMascot from '../assets/mascot.png';
import { setUsername, setPassword, setNetworkName, setNetworkPassword } from "./setupSlice";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { APP_CONFIG } from "../../app/appConfig"

export const Setup = () => {
  const [setup, { isLoading }] = useSetupMutation();
  const dispatch = useAppDispatch();
  const state = useAppSelector(state => state.setup)

  const waitFor = async (url: string, timeoutMs = 60_000) => {
    const start = Date.now()
    while (Date.now() - start < timeoutMs) {
      try {
        await fetch(url, { mode: "no-cors", cache: "no-store" })
        return true
      } catch { }
      await new Promise(r => setTimeout(r, 1500))
    }
    return false
  }

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault()

    // Fire and forget because network will drop out on successful SSID connection
    setup(state)

    await waitFor(APP_CONFIG.prodUrl)
    window.location.assign(APP_CONFIG.prodUrl)
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

        {/* {isError && <div className="error">Setup failed</div>} */}
      </form>
    </div>
  )
}
