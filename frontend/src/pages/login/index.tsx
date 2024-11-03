import { useEffect, useState } from "react";
import "./index.scss";
import { useLoginMutation } from "../../ducks/user/api";
import { useNavigate } from "react-router-dom";

enum InputType {
  EMAIL = "email",
  PASSWORD = "password",
}

type UserDetails = {
  [InputType.EMAIL]: string;
  [InputType.PASSWORD]: string;
};

const Login = ({ handleSession }: any) => {
  const navigate = useNavigate();
  const [userDetails, setUserDetails] = useState<UserDetails>({
    email: "",
    password: "",
  });
  const [login, { isLoading, isError, error }] = useLoginMutation();
  const [errMsg, setErrMsg] = useState("");

  useEffect(() => {
    isError &&
      setErrMsg(
        ((error as any)?.data?.error || "Something Went Wrong") +
          ", Try again..."
      );
  }, [isError]);

  const handleInputChange = (value: string, inputType: InputType) => {
    setErrMsg("");
    setUserDetails((prev) => ({ ...prev, [inputType]: value }));
  };

  const handleLogin = async () => {
    if (!userDetails.email || !userDetails.password) {
      setErrMsg("Email or Password is InValid");
      return;
    }
    try {
      const res = await login({ ...userDetails }).unwrap();
      if (res?.meta?.response?.status === 200) {
        handleSession(res?.data);
      } else {
        throw res?.data;
      }
    } catch (err) {
      console.log("auth failed -", err);
    }
  };

  const handleKeyPress = (key: string, inputType: InputType) => {
    if (key === "Enter") {
      switch (inputType) {
        case InputType.EMAIL:
          document.getElementById("password-input")?.focus();
          break;
        case InputType.PASSWORD:
          handleLogin();
          break;
      }
    }
  };

  const handleRegister = () => {
    navigate("/register");
  };

  return (
    <div className="login-page-container center">
      <div className="login-widget-container">
        <div className="title">Login</div>
        <div className="error-container">{errMsg}</div>
        <div className="login-form">
          <input
            value={userDetails.email}
            className="login-form-input"
            placeholder="Enter Email..."
            type="text"
            onChange={(e) => handleInputChange(e.target.value, InputType.EMAIL)}
            onKeyPress={(e) => handleKeyPress(e.key, InputType.EMAIL)}
            disabled={isLoading}
          />
          <input
            id="password-input"
            value={userDetails.password}
            className="login-form-input"
            placeholder="Enter Password..."
            type="password"
            onChange={(e) =>
              handleInputChange(e.target.value, InputType.PASSWORD)
            }
            onKeyPress={(e) => handleKeyPress(e.key, InputType.PASSWORD)}
            disabled={isLoading}
          />
          <button
            className={`login-submit ${isLoading && "loading"}`}
            onClick={handleLogin}
            disabled={isLoading}
          >
            Login
          </button>
        </div>
        <div className="register-wrapper">
          New User?{" "}
          <button
            className="register-btn"
            onClick={handleRegister}
            disabled={isLoading}
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default Login;
