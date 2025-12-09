import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react"
import { APP_CONFIG } from "../../app/configSlice"

// type MoveRequest = {
//     direction: Direction
// }

export enum CameraDirection {
    UP = "up",
    DOWN = "down",
    LEFT = "left",
    RIGHT = "right"
}

export const cameraApiSlice = createApi({
    reducerPath: "cameraApi",
    baseQuery: fetchBaseQuery({
        baseUrl: APP_CONFIG.baseUrl,
    }),
    tagTypes: ["Camera"],
    endpoints: build => ({
        move: build.mutation<unknown, CameraDirection>({
            query: (direction) => ({
                url: APP_CONFIG.movePath,
                method: "POST",
                body: JSON.stringify(direction),
            }),
        }),
    }),
})

// Auto-generated hook
export const { useMoveMutation } = cameraApiSlice