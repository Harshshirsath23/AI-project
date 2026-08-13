export type LoginMode = 'password' | 'sso' | 'passkey';

export interface UserPreset {
  id: string;
  name: string;
  email: string;
  role: string;
  avatar?: string;
}

export interface RegionOption {
  id: string;
  name: string;
  flag: string;
  locale: string;
}

export type AsciiPalette = 'mono' | 'gold' | 'cyan' | 'emerald';
export type AsciiMode = 'waves' | 'spotlight' | 'matrix';
