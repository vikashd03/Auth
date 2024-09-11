import { useSelector } from "react-redux";
import { RootState } from "../../ducks/store";
import { useGetUserMutation } from "../../ducks/user/api";
import { cacheKey } from "../../utils/constants";

const Profile = () => {
  const user = useSelector((state: RootState) => state.user).user;
  const [, { isLoading: getUserIsLoading }] = useGetUserMutation({
    fixedCacheKey: cacheKey.FETCH_USER_DATA,
  });

  if (getUserIsLoading) {
    return <div>laoding...</div>;
  }

  if (!user) return;

  return (
    <div className="profile-wrapper">
      <div className="profile-title">Profile</div>
      <div>Name: {user.name}</div>
      <div>Email: {user.email}</div>
    </div>
  );
};

export default Profile;
