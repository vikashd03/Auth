export const BASE_URI = "https://localhost:8090/";

export const UNPROTECTED_ROUTES = ["/login", "/register", "/logout"];

export const UNPROTECTED_ENPOINTS = [
  "auth/signup/",
  "auth/signin/",
  "auth/refresh/token/",
  "auth/logout/",
];

export const DEFAULT_REDIRECT = "/home";

export const TOKEN_REFRESH_INTERVAL = 15; // in mins

export const ACTIVITY_TRACKER_INTERVAL = 30; // in mins

export const NAV_ITEMS = [
  {
    label: "Home",
    url: "/home",
  },
  {
    label: "Chat",
    url: "/chat",
  },
];

export const PROFILE_IMAGE_FILE_FORMATS = ["image/jpeg", "image/png"];
