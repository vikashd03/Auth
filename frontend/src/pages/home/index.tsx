import { useEffect } from "react";
import { useGetUsersMutation } from "../../ducks/user/api";

const Home = () => {
  const [getUsers, { data: usersData, isLoading: usersIsLoading }] =
    useGetUsersMutation();
  const { data: userList, total } = usersData || {};

  useEffect(() => {
    getUsers(undefined);
  }, []);

  return (
    <div className="home-wrapper">
      <div className="home-title">Home</div>
      <div className="users-wrapper">
        <div className="users-title"></div>
        <div className="users-lsit-wrapper">
          {usersIsLoading ? (
            <div>loading</div>
          ) : (
            <div>
              <div>Total Users: {total}</div>
              {userList &&
                userList.map((user: any, index: number) => (
                  <div key={index}>
                    <div>No: {index + 1}</div>
                    <div>Name: {user.name}</div>
                    <div>Email: {user.email}</div>
                  </div>
                ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Home;
