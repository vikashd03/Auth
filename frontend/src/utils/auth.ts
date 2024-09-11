// import { ACTIVITY_TRACKER_INTERVAL, DEFAULT_REDIRECT, TOKEN_REFRESH_INTERVAL, UNPROTECTED_ROUTES } from "./config";
// import { store } from "../ducks/store";
// import { userApi } from "../ducks/user/api";
// import { cacheKey } from "./constants";
// import { setAccessToken } from "../ducks/user/slice";

// // eslint-disable-next-line @typescript-eslint/no-unused-vars
// class Auth {
//     private accessToken: string | null;
//     private tokenRefreshTimeout: number | undefined = undefined
//     private activityTrackerTimeout: number | undefined = undefined
//     private authSuccessCb: (url: string) => Promise<void>
//     private logoutCb: () => void

//     constructor(authSuccessCb: (url: string) => Promise<void>, logoutCb: () => void) {
//         this.accessToken = null
//         this.tokenRefreshTimeout = undefined
//         this.activityTrackerTimeout = undefined
//         this.authSuccessCb = authSuccessCb
//         this.logoutCb = logoutCb
//     }

//     setAccessToken(accessToken: string | null) {
//         this.accessToken = accessToken
//         store.dispatch(setAccessToken(accessToken))
//     }

//     isAuthenticated() {
//         return !!this.accessToken
//     }

//     logout() {
//         store.dispatch(userApi.endpoints.logout.initiate(undefined, { fixedCacheKey: cacheKey.AUTH_LOGOUT })).unwrap().finally(() => {
//             clearTimeout(this.tokenRefreshTimeout)
//             clearTimeout(this.activityTrackerTimeout)
//             this.setAccessToken(null)
//             this.logoutCb()
//         })
//     }

//     handleSession(data: any, callBk: boolean) {
//         this.setAccessToken(data?.["access_token"])
//         if (callBk) {
//             const from = localStorage.getItem("from_url")
//             const url = from && !UNPROTECTED_ROUTES.includes(from) ? from : DEFAULT_REDIRECT
//             this.authSuccessCb(url)
//             this.startActivityTracker()
//         }
//         this.tokenRefreshTimeout = setTimeout(this.scheduledRefreshToken.bind(this), TOKEN_REFRESH_INTERVAL * 60_000)
//     }

//     refreshToken(callBk: boolean) {
//         store.dispatch(userApi.endpoints.refresh.initiate(undefined)).unwrap()
//             .then((res: any) => {
//                 this.handleSession(res?.data, callBk)
//             }).catch((err) => {
//                 console.log("token refresh failed -", err);
//             })
//     }

//     scheduledRefreshToken = () => this.refreshToken(false);

//     handleAuth() {
//         if (this.isAuthenticated()) return
//         this.refreshToken(true)
//     }

//     removeActivityTracker() {
//         window.removeEventListener('mousemove', () => this.activityHandler());
//         window.removeEventListener('scroll', () => this.activityHandler());
//         window.removeEventListener('keydown', () => this.activityHandler());
//     }

//     activityTracker() {
//         window.addEventListener('mousemove', () => this.activityHandler());
//         window.addEventListener('scroll', () => this.activityHandler());
//         window.addEventListener('keydown', () => this.activityHandler());
//     }

//     activityHandler() {
//         clearTimeout(this.activityTrackerTimeout)
//         this.activityTrackerTimeout = setTimeout(() => {
//             console.log('logging out due to inactivity -', new Date())
//             this.logout()
//         }, ACTIVITY_TRACKER_INTERVAL * 60_000)
//     }

//     startActivityTracker() {
//         console.log('started ActivityTracker -', new Date())
//         this.activityHandler()
//         this.activityTracker()
//     }
// }

// export default Auth