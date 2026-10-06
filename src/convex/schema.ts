// Convex schema sketch kept for architecture reference only.
// The current MVP gate is a lightweight client session so the static bundle
// stays self-contained. If you add Convex later, mirror this shape there.

export interface UserShape {
  name: string;
  avatarUrl?: string;
  proActivatedAt?: number;
  energyCount: number;
  lastEnergyAt?: number;
}

export interface SigilShape {
  userId: string;
  phrase: string;
  vibe: string;
  quality: string;
  imageBase64: string;
  createdAt: number;
}

export interface SettingsShape {
  userId: string;
  defaultVibe: string;
  defaultQuality: string;
}
