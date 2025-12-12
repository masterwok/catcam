import { createSlice, PayloadAction } from "@reduxjs/toolkit"

interface SetupState {
  username: string
  password: string
  networkName: string
  networkPassword: string
}

const initialState: SetupState = {
  username: "",
  password: "",
  networkName: "",
  networkPassword: "",
}

const setupSlice = createSlice({
  name: "setup",
  initialState,
  reducers: {
    setUsername(state, action: PayloadAction<string>) {
      state.username = action.payload
    },
    setPassword(state, action: PayloadAction<string>) {
      state.password = action.payload
    },
    setNetworkName(state, action: PayloadAction<string>) {
      state.networkName = action.payload
    },
    setNetworkPassword(state, action: PayloadAction<string>) {
      state.networkPassword = action.payload
    },
    resetSetup() {
      return initialState
    },
  },
})

export const {
  setUsername,
  setPassword,
  setNetworkName,
  setNetworkPassword,
  resetSetup,
} = setupSlice.actions

export default setupSlice
