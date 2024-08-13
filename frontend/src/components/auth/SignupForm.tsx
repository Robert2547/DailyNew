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
    <div className="form-container">
      <p className="title">Get started today</p>
      <form className="form" onSubmit={handleSubmit}>
        <input
          type="email"
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
        <input
          type="password"
          className="input"
          placeholder="Confirm Password"
          value={inputs.confirmPassword}
          onChange={(e) => setInputs({ ...inputs, confirmPassword: e.target.value })}
        />
        <button className="form-btn" disabled={loading}>
          {loading ? <span className="loading loading-spinner" /> : 'Sign Up'}
        </button>
      </form>
      <p className="sign-up-label">
        Already have an account?
        <Link to="/login" className="sign-up-link">
          Login
        </Link>
      </p>
      {/* Social signup buttons */}
    </div>
  );
};

export default SignupForm;