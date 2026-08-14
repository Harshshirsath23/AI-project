import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import './index.css';
import { NotificationProvider } from './context/NotificationContext';
import { AuthProvider } from './context/AuthContext';
import { PermissionProvider } from './context/PermissionContext';
import { OrganizationProvider } from './context/OrganizationContext';
import { ThemeProvider } from './context/ThemeContext';

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ThemeProvider>
      <AuthProvider>
        <PermissionProvider>
          <OrganizationProvider>
            <NotificationProvider>
              <App />
            </NotificationProvider>
          </OrganizationProvider>
        </PermissionProvider>
      </AuthProvider>
    </ThemeProvider>
  </StrictMode>,
);
