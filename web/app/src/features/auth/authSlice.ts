import { createSlice, PayloadAction } from "@reduxjs/toolkit"

type AuthState = {
    token: string | null
}

const initialState: AuthState = {
    token: null,
}

export const authSlice = createSlice({
    name: "auth",
    initialState,
    reducers: {
        setToken(state, action: PayloadAction<string>) {
            state.token = action.payload
        },
        clearToken(state) {
            state.token = null
        },
    },
    selectors: {
        selectIsAuthenticated: auth => !!auth.token,
        selectToken: auth => auth.token,
    }
})

export const { setToken, clearToken } = authSlice.actions

export const { selectIsAuthenticated, selectToken } = authSlice.selectors;

export default authSlice
