import { fetchBaseQuery } from "@reduxjs/toolkit/query/react"
import { APP_CONFIG } from "../../app/appConfig"
import { selectToken } from "./authSlice"
import { RootState } from "../../app/store"

export const baseQueryWithAuth = fetchBaseQuery({
    baseUrl: APP_CONFIG.baseUrl,
    prepareHeaders: (headers, { getState }) => {
        const state = getState() as RootState
        const token = selectToken(state)

        if (token) {
            headers.set("authorization", `Bearer ${token}`)
        }

        return headers
    },
})
