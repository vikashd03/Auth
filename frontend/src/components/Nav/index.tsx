import { useSelector } from "react-redux";
import useNavigateWithState from "../../hooks/useNavigateWithState";
import { NAV_ITEMS } from "../../utils/config";
import { cacheKey, pubsubTopic } from "../../utils/constants";
import { pubsub } from "../../utils/PubSub";
import "./index.scss";
import { RootState } from "../../ducks/store";
import { useGetUserMutation } from "../../ducks/user/api";
import Loader from "../Loader";
import { useEffect, useRef, useState } from "react";
import { FaPencil } from "react-icons/fa6";
import { IoMdSettings } from "react-icons/io";
import { MdLogout } from "react-icons/md";
import EditProfileModal from "../EditProfileModal";

const Nav = () => {
  const navigate = useNavigateWithState();
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);
  const [editProfileOpen, setEditProfileOpen] = useState(false);
  const { user } = useSelector((state: RootState) => state.user);
  const [, { isLoading: userLoading }] = useGetUserMutation({
    fixedCacheKey: cacheKey.FETCH_USER_DATA,
  });
  const profileDropdownRef = useRef<any>();

  useEffect(() => {
    const listener = (e: any) => {
      if (
        profileDropdownRef.current &&
        !profileDropdownRef.current.contains(e.target) &&
        e.target.id !== "nav-profile-btn"
      ) {
        setProfileDropdownOpen(false);
      }
    };
    document.addEventListener("click", listener);
    return () => {
      document.removeEventListener("click", listener);
    };
  }, [profileDropdownOpen]);

  const navOnClickHandler = (url: string) => {
    navigate(url);
  };

  return (
    <div className="nav-wrapper">
      {!userLoading && (
        <EditProfileModal
          isOpen={!userLoading && editProfileOpen}
          onClose={() => setEditProfileOpen(false)}
        />
      )}
      <div className="nav-title">Sample App</div>
      <div className="nav-items">
        <div className="nav-links">
          {NAV_ITEMS.map((navItem, index) => (
            <button
              key={index}
              className="nav-link"
              onClick={() => {
                navOnClickHandler(navItem.label);
              }}
            >
              {navItem.label}
            </button>
          ))}
        </div>
        <div className="nav-options">
          {userLoading || !user ? (
            <Loader size="small" />
          ) : (
            <>
              <button
                id="nav-profile-btn"
                className="profile-btn"
                onClick={() => setProfileDropdownOpen(!profileDropdownOpen)}
              >
                {user.name}
              </button>
              {profileDropdownOpen && (
                <div className="profile-dropdown" ref={profileDropdownRef}>
                  <div
                    className="profile-dropdown-item"
                    onClick={() => setEditProfileOpen(true)}
                  >
                    <FaPencil />
                    <button>Profle</button>
                  </div>
                  <div className="profile-dropdown-item">
                    <IoMdSettings />
                    <button>Settings</button>
                  </div>
                  <div
                    className="profile-dropdown-item"
                    onClick={() => {
                      pubsub.publish(pubsubTopic.AUTH_LOGOUT, "logout");
                    }}
                  >
                    <MdLogout />
                    <button>Logout</button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Nav;
