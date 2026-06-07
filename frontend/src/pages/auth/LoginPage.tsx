import { Alert, Box, Button, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { Link as RouterLink, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "@/store/AuthContext";
import { decodeJwt } from "@/utils/jwt";
import { storage } from "@/utils/storage";

const redirectByRole = (role: string) => {
  if (role === "seller") {
    return "/seller/dashboard";
  }
  if (role === "admin" || role === "support_admin") {
    return "/admin/dashboard";
  }
  return "/";
};

export const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await login({ email, password });
      const token = storage.getToken();
      const decoded = token ? decodeJwt(token) : null;
      const redirectPath = (location.state as { from?: string } | null)?.from;
      navigate(redirectPath ?? redirectByRole(decoded?.role ?? "customer"), { replace: true });
    } catch {
      setError("Login failed. Please check your credentials.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
      <Typography variant="h5" fontWeight={700}>
        Login
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Enter your credentials to continue.
      </Typography>
      {error ? <Alert severity="error">{error}</Alert> : null}
      <TextField
        label="Email"
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        required
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        required
      />
      <Button type="submit" variant="contained" disabled={isLoading}>
        {isLoading ? "Logging in..." : "Login"}
      </Button>
      <Typography variant="body2" color="text.secondary">
        Don&apos;t have an account? <RouterLink to="/signup">Sign up</RouterLink>
      </Typography>
    </Box>
  );
};
