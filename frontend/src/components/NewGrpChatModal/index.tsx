import { useEffect, useMemo, useRef, useState } from "react";
import {
  useGetUsersMutation,
  useUploadProfileImgMutation,
} from "../../ducks/user/api";
import Modal from "../Modal";
import "./index.scss";
import Loader from "../Loader";
import { CgProfile } from "react-icons/cg";
import { IoClose } from "react-icons/io5";
import { IoCameraOutline } from "react-icons/io5";
import { GoPencil } from "react-icons/go";
import { User } from "../../types/common";
import { useSelector } from "react-redux";
import { RootState } from "../../ducks/store";
import { useCreateNewChatMutation } from "../../ducks/chat/api";
import { PROFILE_IMAGE_FILE_FORMATS } from "../../utils/config";
import { BASE_URL } from "../../ducks/api/slice";

const NewGrpChatModal = ({
  isOpen,
  onClose,
}: {
  isOpen: boolean;
  onClose: () => void;
}) => {
  const [chatName, setChatName] = useState<string>("");
  const [membersSearch, setMembersSearch] = useState<string>("");
  const [selectedMembers, setSelectedMembers] = useState<User[]>([]);
  const [profileImgFile, setProfileImgFile] = useState<File | null>(null);
  const [errMsg, setErrMsg] = useState("");
  const { user: currentUser } = useSelector((state: RootState) => state.user);
  const [getUsers, { data: usersData, isLoading: usersIsLoading }] =
    useGetUsersMutation();
  const userList = usersData?.data?.data ?? [];
  const [createNewChat, { data: newChatData, isLoading: newChatLoading }] =
    useCreateNewChatMutation();
  const [
    uploadProfileImg,
    { data: profileImgUploadData, isLoading: profileImgUploadLoading },
  ] = useUploadProfileImgMutation();
  const profileImgInputRef = useRef<HTMLInputElement | null>(null);
  const profileImgPreviewUrl = profileImgFile
    ? URL.createObjectURL(profileImgFile)
    : "";

  useEffect(() => {
    getUsers(undefined);
    return () => {
      profileImgPreviewUrl && URL.revokeObjectURL(profileImgPreviewUrl);
    };
  }, []);

  const membersList = useMemo(
    () =>
      userList.filter(
        (member) =>
          member.email !== currentUser?.email &&
          member.name.toUpperCase().includes(membersSearch.toUpperCase())
      ) ?? [],
    [userList, membersSearch, currentUser]
  );

  const handleMemberListClick = (member: User) => {
    setErrMsg("");
    let currentSelectedMembers = [...selectedMembers];
    const currentSelectedMembersEmails = currentSelectedMembers.map(
      (member) => member.email
    );
    if (currentSelectedMembersEmails.includes(member.email)) {
      currentSelectedMembers = currentSelectedMembers.filter(
        (member) => member.email !== member.email
      );
    } else {
      currentSelectedMembers = [...currentSelectedMembers, member];
    }
    setSelectedMembers(currentSelectedMembers);
  };

  const membersListWithSelection = useMemo(
    () =>
      membersList.map((member) => {
        const selectedMembersEmails = selectedMembers.map(
          (member) => member.email
        );
        return {
          ...member,
          selected: selectedMembersEmails.includes(member.email),
        };
      }),
    [membersList, selectedMembers]
  );

  const handleCreateNewGrpChat = async () => {
    if (!chatName || !selectedMembers.length) {
      setErrMsg("Not a Valid Group");
      return;
    }
    try {
      const res = await createNewChat({
        name: chatName,
        type: "group",
        members: [...selectedMembers.map((member) => member.email)],
      }).unwrap();
      if (res?.data?.chat?.id && profileImgFile) {
        await uploadProfileImg({
          file: profileImgFile,
          type: "group",
          id: res?.data?.chat?.id,
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
      title="New Chat"
      width={450}
      height={"fit-content"}
      showHeader={false}
      showFooter={false}
    >
      <div className="new-grp-chat-modal-wrapper">
        <div className="new-grp-chat-modal-header">
          <div className="new-grp-chat-modal-title">Create New Group Chat</div>
          <IoClose className="new-grp-chat-modal-close-btn" onClick={onClose} />
        </div>
        <div className="new-grp-chat-modal-content">
          <div className="chat-profile-input-wrapper">
            <div className="chat-profile-img-wrapper">
              {!profileImgFile ? (
                <IoCameraOutline
                  className="chat-profile-img-placeholder"
                  onClick={() =>
                    profileImgInputRef.current !== null &&
                    profileImgInputRef.current.click()
                  }
                />
              ) : (
                <div
                  className="chat-profile-selected-img-wrapper"
                  onClick={() =>
                    profileImgInputRef.current !== null &&
                    profileImgInputRef.current.click()
                  }
                >
                  <img
                    src={profileImgPreviewUrl}
                    className="chat-profile-selected-img"
                  />
                  <GoPencil className="chat-profile-selected-img-edit" />
                </div>
              )}
              <input
                type="file"
                className="chat-profile-img-input"
                ref={profileImgInputRef}
                accept={PROFILE_IMAGE_FILE_FORMATS.join(", ")}
                onChange={handleProfileImageChange}
              />
            </div>
            <input
              className="chat-name-input"
              placeholder="Enter Chat Name"
              value={chatName}
              onChange={(e) => {
                setErrMsg("");
                setChatName(e.target.value);
              }}
            />
          </div>
          <div className="add-members-wrapper">
            <input
              className="add-members-search"
              placeholder="Add Members ..."
              value={membersSearch}
              onChange={(e) => setMembersSearch(e.target.value)}
            />
            <div className="members-added">
              {selectedMembers.map((user, index) => (
                <div key={index} className="members-added-item">
                  {user.name}
                </div>
              ))}
            </div>
            {usersIsLoading ? (
              <Loader />
            ) : (
              <div className="members-list">
                {membersListWithSelection.length > 0 ? (
                  membersListWithSelection.map((user, index) => (
                    <div
                      key={index}
                      className="member-list-item"
                      onClick={() => handleMemberListClick(user)}
                    >
                      {user.img_url ? (
                        <img
                          src={`${BASE_URL}${user.img_url}`}
                          className="member-profile-img"
                        />
                      ) : (
                        <CgProfile className="member-profile-icon" />
                      )}
                      <div className="member-profile-content">
                        <div className="member-name">{user.name}</div>
                        <div className="member-email">Email: {user.email}</div>
                      </div>
                      <input
                        className="member-list-checkbox"
                        type="checkbox"
                        checked={user.selected}
                        onChange={() => null}
                      />
                    </div>
                  ))
                ) : (
                  <div>No Users Found</div>
                )}
              </div>
            )}
          </div>
        </div>
        <div className="create-new-grp-chat-wrapper">
          <div className="create-new-grp-chat-error">{errMsg}</div>
          <div className="create-new-grp-chat-btn-laoding">
            {newChatLoading || profileImgUploadLoading ? (
              <Loader />
            ) : (
              <button
                className="create-new-grp-chat-btn"
                onClick={handleCreateNewGrpChat}
              >
                Create Group
              </button>
            )}
          </div>
        </div>
      </div>
    </Modal>
  );
};

export default NewGrpChatModal;
