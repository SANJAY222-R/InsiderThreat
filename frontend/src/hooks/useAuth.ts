import { useDispatch, useSelector } from 'react-redux';
import type { RootState } from '../store';
import { loginSuccess, logout } from '../store/slices/authSlice';

export const useAuth = () => {
  const dispatch = useDispatch();
  const authState = useSelector((state: RootState) => state.auth);

  const login = (user: any, token: string) => {
    dispatch(loginSuccess({ user, token }));
  };

  const performLogout = () => {
    dispatch(logout());
  };

  return {
    ...authState,
    login,
    logout: performLogout,
  };
};
