import { useEffect, useRef } from "react";
import {
  useGetUserMutation,
  useLogoutMutation,
  useRefreshMutation,
} from "./ducks/user/api";
import { Navigate, Route, Routes, useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import Login from "./pages/login";
import Register from "./pages/register";
import Layout from "./Layout";
import {
  ACTIVITY_TRACKER_INTERVAL,
  DEFAULT_REDIRECT,
  TOKEN_REFRESH_INTERVAL,
  UNPROTECTED_ROUTES,
} from "./utils/config";
import { pubsub } from "./utils/PubSub";
import { cacheKey, pubsubTopic } from "./utils/constants";
import { useDispatch } from "react-redux";
import { setAccessToken } from "./ducks/user/slice";
import useAuth from "./hooks/useAuth";

const AuthRouter = () => {
  const [isAuthenticated] = useAuth();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const currPath = location.pathname;
  const activityTrackerTimeout = useRef<number>();
  const refreshTokenInterval = useRef<number>();
  const [logoutTr, { isLoading: logoutIsLoading }] = useLogoutMutation();
  const [getUser] = useGetUserMutation({
    fixedCacheKey: cacheKey.FETCH_USER_DATA,
  });
  const [refresh, { isLoading: tokenLoading, isError: tokenError }] =
    useRefreshMutation();

  const removeActivityTracker = () => {
    console.log("stopped ActivityTracker -", new Date());
    window.removeEventListener("mousemove", () => activityHandler());
    window.removeEventListener("scroll", () => activityHandler());
    window.removeEventListener("keydown", () => activityHandler());
  };

  const activityTracker = () => {
    window.addEventListener("mousemove", () => activityHandler());
    window.addEventListener("scroll", () => activityHandler());
    window.addEventListener("keydown", () => activityHandler());
  };

  const activityHandler = () => {
    clearTimeout(activityTrackerTimeout.current);
    activityTrackerTimeout.current = setTimeout(() => {
      console.log("logging out due to inactivity -", new Date());
      logout();
    }, ACTIVITY_TRACKER_INTERVAL * 60_000);
  };

  const startActivityTracker = () => {
    console.log("started ActivityTracker -", new Date());
    activityHandler();
    activityTracker();
  };

  const handleSession = (authRes: any) => {
    dispatch(setAccessToken(authRes["access_token"] ?? null));
    const from = localStorage.getItem("from_url");
    const url =
      from && !UNPROTECTED_ROUTES.includes(from) ? from : DEFAULT_REDIRECT;
    navigate(url);
    getUser(undefined);
    startActivityTracker();
    clearInterval(refreshTokenInterval.current);
    refreshTokenInterval.current = setInterval(() => {
      refreshToken();
    }, TOKEN_REFRESH_INTERVAL * 60_000);
  };

  const authSuccessCb = (authRes: any) => {
    handleSession(authRes);
  };

  const logoutCb = () => {
    clearInterval(refreshTokenInterval.current);
    clearTimeout(activityTrackerTimeout.current);
    removeActivityTracker();
    dispatch(setAccessToken(null));
    navigate("/login");
  };

  const logout = () => {
    logoutTr(undefined).finally(() => logoutCb());
  };

  const refreshToken = (silent: boolean = true) => {
    refresh(undefined)
      .unwrap()
      .then((res) => {
        if (silent) {
          dispatch(setAccessToken(res.data["access_token"]));
        } else {
          authSuccessCb(res.data);
        }
      })
      .catch((err) => {
        console.log("token refresh failed, logging out -", err);
        logout();
      });
  };

  const setPubSub = () => {
    pubsub.subscribe(pubsubTopic.AUTH_LOGOUT, {
      id: "auth-handler",
      handler: (message: string) => {
        console.log("message -", message);
        logout();
      },
    });
  };

  useEffect(() => {
    if (!isAuthenticated && !UNPROTECTED_ROUTES.includes(currPath)) {
      refreshToken(false);
    }
    setPubSub();
    return () => {
      pubsub.unsubscribe(pubsubTopic.AUTH_LOGOUT, "auth-handler");
    };
  }, []);

  return (
    <Routes>
      <Route
        path="/login"
        element={(() => {
          if (isAuthenticated) {
            return (
              <Navigate
                to="/"
                replace
                state={{ ...location.state, redirect: true }}
              />
            );
          } else {
            return <Login handleSession={handleSession} />;
          }
        })()}
      />
      <Route
        path="/register"
        element={(() => {
          if (isAuthenticated) {
            return (
              <Navigate
                to="/"
                replace
                state={{ ...location.state, redirect: true }}
              />
            );
          } else {
            return <Register handleSession={handleSession} />;
          }
        })()}
      />
      <Route
        path="/"
        element={(() => {
          const { from, redirect } = location?.state || {};
          if (from && !UNPROTECTED_ROUTES.includes(from)) {
            localStorage.setItem("from_url", from);
          }
          if (redirect) {
            const url =
              from && !UNPROTECTED_ROUTES.includes(from)
                ? from
                : DEFAULT_REDIRECT;
            return <Navigate to={url} replace />;
          } else {
            return null;
          }
        })()}
      />
      <Route
        path="/*"
        element={(() => {
          if (!logoutIsLoading && isAuthenticated) {
            return <Layout />;
          } else if (!isAuthenticated && tokenLoading) {
            return <div className="center">Auth Loading...</div>;
          } else if (tokenError) {
            return (
              <div className="center">
                {"<---"} Auth Error {"--->"}
              </div>
            );
          } else {
            return <Navigate to="/" replace state={{ from: currPath }} />;
          }
        })()}
      />
    </Routes>
  );
};

export default AuthRouter;
