import "./App.css"
import { useAppSelector } from "./app/hooks"
import { selectIsAuthenticated } from "./features/auth/authSlice"
import { Login } from "./features/auth/Login"
import { Camera } from "./features/camera/Camera"
import { Setup } from "./features/setup/Setup"
import { useGetSetupStatusQuery } from "./features/setup/setupApiSlice"

export const App = () => {
  const { data, isLoading } = useGetSetupStatusQuery()
  const isAuthenticated = useAppSelector(selectIsAuthenticated)

  if (isLoading) return null

  const content = data?.setupComplete
    ? (isAuthenticated ? <Camera /> : <Login />)
    : <Setup />

  return (
    <div className="App">
      {content}
    </div>
  )
}
