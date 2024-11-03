import { useEffect, useMemo, useState } from "react";
import { useGetUsersMutation } from "../../ducks/user/api";
import Modal from "../Modal";
import "./index.scss";
import Loader from "../Loader";
import { CgProfile } from "react-icons/cg";
import { IoClose } from "react-icons/io5";
import { User } from "../../types/common";
import { useSelector } from "react-redux";
import { RootState } from "../../ducks/store";
import { useCreateNewChatMutation } from "../../ducks/chat/api";

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
  const [errMsg, setErrMsg] = useState("");
  const { user: currentUser } = useSelector((state: RootState) => state.user);
  const [getUsers, { data: usersData, isLoading: usersIsLoading }] =
    useGetUsersMutation();
  const userList = usersData?.data?.data ?? [];
  const [createUser, { data: newChatData, isLoading: newChatLoading }] =
    useCreateNewChatMutation();

  useEffect(() => {
    getUsers(undefined);
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
      const res = await createUser({
        name: chatName,
        type: "group",
        members: [...selectedMembers.map((member) => member.email)],
      }).unwrap();
      if (res?.meta?.response?.status === 200) {
        onClose();
      } else {
        throw res?.data;
      }
    } catch (err: any) {
      console.log(err);
      setErrMsg(err.data.error);
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
          <input
            className="chat-name-input"
            placeholder="Enter Chat Name"
            value={chatName}
            onChange={(e) => {
              setErrMsg("");
              setChatName(e.target.value);
            }}
          />
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
                      <CgProfile className="member-profile-icon" />
                      <div className="member-profile-content">
                        <div className="member-name">{user.name}</div>
                        <div className="member-email">Email: {user.email}</div>
                      </div>
                      <input
                        className="member-list-checkbox"
                        type="checkbox"
                        checked={user.selected}
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
            {newChatLoading ? (
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
