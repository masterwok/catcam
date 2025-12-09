import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"
import { setToken } from "./authSlice"
import { APP_CONFIG } from "../../app/configSlice"

type LoginRequest = {
  username: string
  password: string
}

type LoginResponse = {
  access_token: string
  token_type: string
}

export const authApiSlice = createApi({
  reducerPath: "authApi",
  baseQuery: fetchBaseQuery({
    baseUrl: APP_CONFIG.baseUrl,
  }),
  endpoints: build => ({
    login: build.mutation<LoginResponse, LoginRequest>({
      query: body => ({
        url: "/login",
        method: "POST",
        body,
      }),

      // ⭐ THIS IS THE MAGIC:
      async onQueryStarted(arg, { dispatch, queryFulfilled }) {
        try {
          const { data } = await queryFulfilled
          dispatch(setToken(data.access_token))
        } catch (err) {
          // silently ignore — login failed
        }
      },
    }),
  }),
})

export const { useLoginMutation } = authApiSlice
