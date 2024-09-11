import { BrowserRouter } from "react-router-dom";
import { Provider } from "react-redux";
import { store } from "./ducks/store";
import AuthRouter from "./AuthRouter";
import "./App.scss";

function App() {
  return (
    <BrowserRouter>
      <Provider store={store}>
        <AuthRouter />
      </Provider>
    </BrowserRouter>
  );
}

export default App;
