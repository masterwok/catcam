import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"
import { APP_CONFIG } from "../../app/configSlice"

type SetupRequest = {
  username: string
  password: string
  networkName: string
  networkPassword: string
}

type SetupResponse = {
  access_token: string
  token_type: string
}

type SetupStatusResponse = {
  setupComplete: boolean
}

export const setupApiSlice = createApi({
  reducerPath: "setupApi",
  baseQuery: fetchBaseQuery({
    baseUrl: APP_CONFIG.baseUrl
  }),
  endpoints: build => ({
    setup: build.mutation<SetupResponse, SetupRequest>({
      query: (request) => ({
        url: "/setup",
        method: "POST",
        body: request
      })
    }),
    getSetupStatus: build.query<SetupStatusResponse, void>({
      query: () => ({
        url: "/status",
        method: "GET",
      }),
    }),
  }),
})

export const { 
  useSetupMutation,
  useGetSetupStatusQuery
} = setupApiSlice
