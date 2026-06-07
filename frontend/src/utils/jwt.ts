import { jwtDecode } from "jwt-decode";

import type { JwtPayload } from "@/types/auth";

export const decodeJwt = (token: string): JwtPayload | null => {
  try {
    return jwtDecode<JwtPayload>(token);
  } catch {
    return null;
  }
};

