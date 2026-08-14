import React, { createContext, useContext, useState, useEffect } from 'react';
import { UserPreset, LoginMode, RegionOption } from '../types';
import { REGION_OPTIONS } from '../data/presets';
import { backendApi } from '../api/client';

interface AuthContextType {
  currentUser: UserPreset | null;
  isLoggedIn: boolean;
  token: string | null;
  selectedRegion: RegionOption;
  setSelectedRegion: (region: RegionOption) => void;
  login: (email: string, pass: string, mode: LoginMode, preset?: UserPreset) => Promise<boolean>;
  logout: () => void;
  userPermissions: string[];
  userRoles: string[];
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<UserPreset | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(false);
  const [token, setToken] = useState<string | null>(null);
  const [selectedRegion, setSelectedRegion] = useState<RegionOption>(REGION_OPTIONS[0]);

  // Restore session on mount
  useEffect(() => {
    const savedToken = localStorage.getItem('talentsphere_session_token');
    const savedUser = localStorage.getItem('talentsphere_user');
    if (savedToken && savedUser) {
      try {
        const parsed = JSON.parse(savedUser);
        setCurrentUser(parsed);
        setToken(savedToken);
        setIsLoggedIn(true);
      } catch (e) {
        localStorage.removeItem('talentsphere_session_token');
        localStorage.removeItem('talentsphere_user');
      }
    }
  }, []);

  const login = async (
    email: string,
    pass: string,
    mode: LoginMode,
    preset?: UserPreset
  ): Promise<boolean> => {
    try {
      // 1. Authenticate with Backend
      const loginRes = await backendApi.login(email, pass);
      
      if (!loginRes || !loginRes.access_token) {
        console.error("Login failed: Invalid credentials or backend unavailable");
        return false;
      }
      
      // Temporarily store token so subsequent API calls use it
      const sessionToken = loginRes.access_token;
      localStorage.setItem('talentsphere_session_token', sessionToken);
      setToken(sessionToken);

      // 2. Fetch User Profile & Permissions
      const userRes = await backendApi.getMe();
      
      if (!userRes) {
        console.error("Failed to fetch user profile after login");
        localStorage.removeItem('talentsphere_session_token');
        setToken(null);
        return false;
      }
      
      // 3. Map to Frontend Preset Structure
      const fullName = userRes.profile?.first_name 
        ? `${userRes.profile.first_name} ${userRes.profile.last_name || ''}`.trim()
        : userRes.username;
        
      const userToLogin: UserPreset = {
        id: userRes.id,
        name: fullName,
        email: userRes.email,
        role: userRes.roles?.[0] || userRes.account_type || 'User',
        company: 'TalentSphere Inc.',
        avatar: userRes.profile?.profile_photo || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
        region: selectedRegion.name,
        badge: userRes.is_platform_admin ? 'Platform Admin' : userRes.is_organization_admin ? 'Org Admin' : 'Authenticated',
        scope: userRes.scope || (userRes.is_platform_admin ? 'PLATFORM' : 'ORGANIZATION'),
        is_platform_admin: userRes.is_platform_admin || userRes.account_type === 'PLATFORM_SUPER_ADMIN' || userRes.account_type === 'SUPER_ADMIN',
        is_organization_admin: userRes.is_organization_admin || userRes.account_type === 'ORGANIZATION_SUPER_ADMIN',
        permissions: userRes.permissions || [],
        roles: userRes.roles || [],
      };

      setCurrentUser(userToLogin);
      setIsLoggedIn(true);
      localStorage.setItem('talentsphere_user', JSON.stringify(userToLogin));

      return true;
    } catch (err) {
      console.error("Exception during login flow:", err);
      return false;
    }
  };

  const logout = () => {
    setCurrentUser(null);
    setToken(null);
    setIsLoggedIn(false);
    localStorage.removeItem('talentsphere_session_token');
    localStorage.removeItem('talentsphere_user');
    // Call backend logout API silently if we want to invalidate token server-side
    fetch('http://localhost:8000/api/v1/auth/logout', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    }).catch(() => {});
  };

  const userPermissions = currentUser?.permissions || [];
  const userRoles = currentUser?.roles || [];

  return (
    <AuthContext.Provider
      value={{
        currentUser,
        isLoggedIn,
        token,
        selectedRegion,
        setSelectedRegion,
        login,
        logout,
        userPermissions,
        userRoles,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
