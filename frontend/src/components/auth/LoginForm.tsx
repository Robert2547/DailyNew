import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { LoginInputs } from '../../types';
import { Loader } from '../common/Loader/Loader'; 

const LoginForm: React.FC = () => {
  const [inputs, setInputs] = useState<LoginInputs>({
    email: '',
    password: '',
  });

  const { loading, login } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await login(inputs);
  };

  if (loading) return <Loader />;

  return (
    <form className="form" onSubmit={handleSubmit}>
      {/* Form inputs */}
    </form>
  );
};