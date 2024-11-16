import { useEffect, useRef, useState } from "react";
import {
  useUpdateUserNameMutation,
  useUploadProfileImgMutation,
} from "../../ducks/user/api";
import Modal from "../Modal";
import "./index.scss";
import Loader from "../Loader";
import { IoClose } from "react-icons/io5";
import { IoCameraOutline } from "react-icons/io5";
import { GoPencil } from "react-icons/go";
import { useSelector } from "react-redux";
import { RootState } from "../../ducks/store";
import { PROFILE_IMAGE_FILE_FORMATS } from "../../utils/config";
import { BASE_URL } from "../../ducks/api/slice";

const EditProfileModal = ({
  isOpen,
  onClose,
}: {
  isOpen: boolean;
  onClose: () => void;
}) => {
  const [profileImgFile, setProfileImgFile] = useState<File | null>(null);
  const [errMsg, setErrMsg] = useState("");
  const { user: currentUser } = useSelector((state: RootState) => state.user);
  const [name, setname] = useState<string>(currentUser?.name || "");
  const [uploadProfileImg, { isLoading: profileImgUploadLoading }] =
    useUploadProfileImgMutation();
  const [updateUsername, { isLoading: updateUserNameLoading }] =
    useUpdateUserNameMutation();
  const profileImgInputRef = useRef<HTMLInputElement | null>(null);
  const profileImgPreviewUrl = profileImgFile
    ? URL.createObjectURL(profileImgFile)
    : currentUser?.img_url
    ? `${BASE_URL}${currentUser?.img_url}`
    : "";

  useEffect(() => {
    return () => {
      profileImgPreviewUrl && URL.revokeObjectURL(profileImgPreviewUrl);
    };
  }, []);

  const handleSave = async () => {
    if (!name) {
      setErrMsg("Not a Valid Profile");
      return;
    }
    try {
      const res = await updateUsername({
        name: name,
      }).unwrap();
      if (res?.data?.data?.id && profileImgFile) {
        await uploadProfileImg({
          file: profileImgFile,
          type: "user",
          id: res?.data?.data?.id,
        }).unwrap();
      }
      onClose();
    } catch (err: any) {
      console.log("new group creation error -", err);
      setErrMsg(err.data.error);
    }
  };

  const handleProfileImageChange = (e: any) => {
    const files: File[] = Array.from(e?.target?.files ?? []);
    if (
      Array.isArray(files) &&
      files.length === 1 &&
      PROFILE_IMAGE_FILE_FORMATS.includes(files[0].type)
    ) {
      setProfileImgFile(files[0]);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title="Edit Profile"
      width={450}
      height={"fit-content"}
      showHeader={false}
      showFooter={false}
    >
      <div className="edit-profile-modal-wrapper">
        <div className="edit-profile-modal-header">
          <div className="edit-profile-modal-title">Edit Profile</div>
          <IoClose className="edit-profile-modal-close-btn" onClick={onClose} />
        </div>
        <div className="edit-profile-modal-content">
          <div className="edit-profile-input-wrapper">
            <div className="edit-profile-img-wrapper">
              {!profileImgPreviewUrl ? (
                <IoCameraOutline
                  className="edit-profile-img-placeholder"
                  onClick={() =>
                    profileImgInputRef.current !== null &&
                    profileImgInputRef.current.click()
                  }
                />
              ) : (
                <div
                  className="edit-profile-selected-img-wrapper"
                  onClick={() =>
                    profileImgInputRef.current !== null &&
                    profileImgInputRef.current.click()
                  }
                >
                  <img
                    src={profileImgPreviewUrl}
                    className="edit-profile-selected-img"
                  />
                  <GoPencil className="edit-profile-selected-img-edit" />
                </div>
              )}
              <input
                type="file"
                className="edit-profile-img-input"
                ref={profileImgInputRef}
                accept={PROFILE_IMAGE_FILE_FORMATS.join(", ")}
                onChange={handleProfileImageChange}
              />
            </div>
            <input
              className="user-name-input"
              placeholder="Enter User Name"
              value={name}
              onChange={(e) => {
                setErrMsg("");
                setname(e.target.value);
              }}
            />
          </div>
          <div>Email: {currentUser?.email}</div>
          <button className="reset-password-btn">Reset Password</button>
        </div>
        <div className="create-edit-profile-wrapper">
          <div className="create-edit-profile-error">{errMsg}</div>
          <div className="create-edit-profile-btn-laoding">
            {updateUserNameLoading || profileImgUploadLoading ? (
              <Loader />
            ) : (
              <button className="create-edit-profile-btn" onClick={handleSave}>
                Save
              </button>
            )}
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default EditProfileModal;
