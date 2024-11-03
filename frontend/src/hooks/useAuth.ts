import { useSelector } from "react-redux";
import { RootState } from "../ducks/store";
import { useEffect, useRef } from "react";

const useAuth = (): [boolean, string | null] => {
  const isAuthenticated = useRef<boolean>(false);
  const user = useSelector((state: RootState) => state.user);
  const accessToken = user.access_token;

  useEffect(() => {
    isAuthenticated.current = !!accessToken;
  }, [accessToken]);

  return [isAuthenticated.current, accessToken];
};

export default useAuth;
