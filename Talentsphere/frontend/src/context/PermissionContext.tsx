import React, { createContext, useContext } from 'react';
import { useAuth } from './AuthContext';
import { Permission } from '../types';

interface PermissionContextType {
  hasPermission: (perm: Permission) => boolean;
  hasRole: (roleName: string) => boolean;
  can: (action: Permission) => boolean;
}

const PermissionContext = createContext<PermissionContextType | undefined>(undefined);

export const PermissionProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { userPermissions, userRoles } = useAuth();

  const hasPermission = (perm: Permission): boolean => {
    if (!userPermissions) return true; // Default admin mode
    return userPermissions.includes(perm) || userPermissions.includes('iam:admin' as Permission);
  };

  const hasRole = (roleName: string): boolean => {
    if (!userRoles) return true;
    return userRoles.some((r) => r.toLowerCase().includes(roleName.toLowerCase()));
  };

  const can = (action: Permission): boolean => {
    return hasPermission(action);
  };

  return (
    <PermissionContext.Provider value={{ hasPermission, hasRole, can }}>
      {children}
    </PermissionContext.Provider>
  );
};

export const usePermission = () => {
  const context = useContext(PermissionContext);
  if (!context) {
    throw new Error('usePermission must be used within a PermissionProvider');
  }
  return context;
};
