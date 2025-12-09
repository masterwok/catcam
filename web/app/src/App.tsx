import "./App.css"
import { useAppSelector } from "./app/hooks"
import { selectIsAuthenticated } from "./features/auth/authSlice"
import { Login } from "./features/auth/Login"
import { Camera } from "./features/camera/Camera"

export const App = () => {
  const isAuthenticated = useAppSelector(selectIsAuthenticated);

  const content = isAuthenticated ? <Camera /> : <Login />

  return (
    <div className="App">
      {content}
    </div>
  );
}


