import { useState } from 'react';
import { toast } from 'react-hot-toast';
import { useAuthContext } from '../context/AuthContext';
import { LoginInputs, SignupInputs, User } from '../types';
import { api } from '../services/api';

export const useAuth = () => {
  const [loading, setLoading] = useState(false);
  const { setAuthUser } = useAuthContext();

  const login = async ({ email, password }: LoginInputs) => {
    setLoading(true);
    try {
      const data = await api.post<User>('/auth/login', { email, password });
      toast.success('Login successful');
      localStorage.setItem('authUser', JSON.stringify(data));
      setAuthUser(data);
    } catch (error) {
      console.error(error);
      toast.error('Login failed: ' + (error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const signup = async ({ email, password, confirmPassword }: SignupInputs) => {
    if (!handleInputErrors({  email, password, confirmPassword })) return;

    setLoading(true);
    try {
      const data = await api.post<User>('/auth/signup', { email, password });
      toast.success('Account created successfully');
      localStorage.setItem('authUser', JSON.stringify(data));
      setAuthUser(data);
    } catch (error) {
      toast.error((error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      await api.post('/auth/logout');
      toast.success('Logged out successfully');
      localStorage.removeItem('authUser');
      setAuthUser(null);
    } catch (error) {
      toast.error((error as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return { loading, login, signup, logout };
};

function handleInputErrors({ email, password, confirmPassword }: SignupInputs): boolean {
  if (!email || !password || !confirmPassword) {
    toast.error('Please fill in all fields');
    return false;
  }

  if (password !== confirmPassword) {
    toast.error('Passwords do not match');
    return false;
  }

  if (password.length < 6) {
    toast.error('Password must be at least 6 characters');
    return false;
  }

  return true;
}