import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { SignupInputs } from '../../types';
import Loader from '../common/Loader/Loader';

const SignupForm: React.FC = () => {
  const [inputs, setInputs] = useState<SignupInputs>({
    email: '',
    password: '',
    confirmPassword: '',
  });

  const { loading, signup } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await signup(inputs);
  };

  if (loading) return <Loader />;

  return (
    <form className="form" onSubmit={handleSubmit}>
      {/* Form inputs */}
    </form>
  );
};