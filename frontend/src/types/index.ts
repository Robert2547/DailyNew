export interface User {
    id: string;
    email: string;
  }
  
  export interface LoginInputs {
    email: string;
    password: string;
  }
  
  export interface SignupInputs {
    email: string;
    password: string;
    confirmPassword: string;
  }
  
  export interface AuthContextType {
    authUser: User | null;
    setAuthUser: (user: User | null) => void;
  }