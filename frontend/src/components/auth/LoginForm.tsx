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
    <div className="form-container">
      <p className="title">Welcome back</p>
      <form className="form" onSubmit={handleSubmit}>
        <input
          type="text"
          className="input"
          placeholder="Email"
          value={inputs.email}
          onChange={(e) => setInputs({ ...inputs, email: e.target.value })}
        />
        <input
          type="password"
          className="input"
          placeholder="Password"
          value={inputs.password}
          onChange={(e) => setInputs({ ...inputs, password: e.target.value })}
        />
        <p className="page-link">
          <span className="page-link-label">Forgot Password?</span>
        </p>
        <button className="form-btn" disabled={loading}>
          {loading ? <span className="loading loading-spinner" /> : 'Login'}
        </button>
      </form>
      <p className="sign-up-label">
        Don't have an account?
        <Link to="/signup" className="sign-up-link">
          Sign up
        </Link>
      </p>
      {/* Social login buttons */}
    </div>
  );
};

export default LoginForm;