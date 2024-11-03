import { useEffect, useState } from "react";
import "./index.scss";
import { useRegisterMutation } from "../../ducks/user/api";
import { useNavigate } from "react-router-dom";

enum InputType {
  NAME = "name",
  EMAIL = "email",
  PASSWORD = "password",
}

type UserDetails = {
  [InputType.NAME]: string;
  [InputType.EMAIL]: string;
  [InputType.PASSWORD]: string;
};

const Register = ({ handleSession }: any) => {
  const navigate = useNavigate();
  const [userDetails, setUserDetails] = useState<UserDetails>({
    name: "",
    email: "",
    password: "",
  });
  const [register, { isLoading, isError, error }] = useRegisterMutation();
  const [errMsg, setErrMsg] = useState("");

  useEffect(() => {
    isError &&
      setErrMsg(
        ((error as any)?.data?.error || "Something Went Wrong") +
          ", Try again..."
      );
  }, [isError]);

  const handleInputChange = (value: string, inputType: InputType) => {
    isError && inputType === InputType.EMAIL && setErrMsg("");
    setUserDetails((prev) => ({ ...prev, [inputType]: value }));
  };

  const handleregister = async () => {
    try {
      const res = await register({ ...userDetails }).unwrap();
      if (res?.meta?.response?.status === 201) {
        handleSession(res?.data);
      } else {
        throw res?.data;
      }
    } catch (err) {
      console.log("register failed -", err);
    }
  };

  const handleKeyPress = (key: string, inputType: InputType) => {
    if (key === "Enter") {
      switch (inputType) {
        case InputType.NAME:
          document.getElementById("email-input")?.focus();
          break;
        case InputType.EMAIL:
          document.getElementById("password-input")?.focus();
          break;
        case InputType.PASSWORD:
          handleregister();
          break;
      }
    }
  };

  const handleLogin = () => {
    navigate("/login");
  };

  return (
    <div className="register-page-container center">
      <div className="register-widget-container">
        <div className="title">Register</div>
        <div className="error-container">{errMsg}</div>
        <div className="register-form">
          <input
            value={userDetails.name}
            className="register-form-input"
            placeholder="Enter Name..."
            type="text"
            onChange={(e) => handleInputChange(e.target.value, InputType.NAME)}
            onKeyPress={(e) => handleKeyPress(e.key, InputType.NAME)}
            disabled={isLoading}
          />
          <input
            id="email-input"
            value={userDetails.email}
            className="register-form-input"
            placeholder="Enter Email..."
            type="text"
            onChange={(e) => handleInputChange(e.target.value, InputType.EMAIL)}
            onKeyPress={(e) => handleKeyPress(e.key, InputType.EMAIL)}
            disabled={isLoading}
          />
          <input
            id="password-input"
            value={userDetails.password}
            className="register-form-input"
            placeholder="Enter Password..."
            type="password"
            onChange={(e) =>
              handleInputChange(e.target.value, InputType.PASSWORD)
            }
            onKeyPress={(e) => handleKeyPress(e.key, InputType.PASSWORD)}
            disabled={isLoading}
          />
          <button
            className={`register-submit ${isLoading && "loading"}`}
            onClick={handleregister}
            disabled={isLoading}
          >
            Register
          </button>
        </div>
        <div className="login-wrapper">
          Existing User?{" "}
          <button
            className="login-btn"
            onClick={handleLogin}
            disabled={isLoading}
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
};

export default Register;
