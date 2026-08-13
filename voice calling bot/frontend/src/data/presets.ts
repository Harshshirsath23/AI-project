import type { UserPreset, RegionOption } from '../types/auth';


export const DEMO_PRESETS: UserPreset[] = [
  {
    id: 'preset_1',
    name: 'Andrew Miller',
    email: 'andrew.ui@uisocial.com',
    role: 'Enterprise Admin',
  },
  {
    id: 'preset_2',
    name: 'Voxera Admin',
    email: 'admin@voxera.ai',
    role: 'Platform Super Admin',
  },
  {
    id: 'preset_3',
    name: 'Sarah SDR',
    email: 'sarah@voxera.ai',
    role: 'Sales SDR Lead',
  },
];

export const REGION_OPTIONS: RegionOption[] = [
  { id: 'en-gb', name: 'English (UK)', flag: '🇬🇧', locale: 'en-GB' },
  { id: 'en-us', name: 'English (US)', flag: '🇺🇸', locale: 'en-US' },
  { id: 'en-in', name: 'English (IN)', flag: '🇮🇳', locale: 'en-IN' },
];
