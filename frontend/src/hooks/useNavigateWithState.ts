import { useNavigate, To, NavigateOptions, useLocation } from 'react-router-dom';

const useNavigateWithState = () => {
    const navigate = useNavigate();
    const location = useLocation();
    return (to: To, options?: NavigateOptions) => {
        return navigate(to, { ...options, state: { ...options?.state, from: location.pathname } })
    }
}

export default useNavigateWithState