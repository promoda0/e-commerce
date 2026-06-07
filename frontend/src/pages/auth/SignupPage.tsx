import { Alert, Box, Button, MenuItem, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";

import { authService } from "@/services/auth.service";
import type { UserRole } from "@/types/auth";

const roleOptions: { label: string; value: UserRole }[] = [
  { label: "Customer", value: "customer" },
  { label: "Seller", value: "seller" },
  { label: "Admin", value: "admin" },
  { label: "Support Admin", value: "support_admin" },
];

export const SignupPage = () => {
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<UserRole>("customer");
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setSuccess(null);
    setIsLoading(true);
    try {
      await authService.signup({
        first_name: firstName,
        last_name: lastName,
        email,
        phone_number: phoneNumber,
        password,
        role,
      });
      setSuccess("Signup successful. Please login with your new account.");
      setTimeout(() => navigate("/login", { replace: true }), 800);
    } catch {
      setError("Signup failed. Check details or try a different email.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} display="flex" flexDirection="column" gap={2}>
      <Typography variant="h5" fontWeight={700}>
        Create Account
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Register a new account with the required role.
      </Typography>

      {error ? <Alert severity="error">{error}</Alert> : null}
      {success ? <Alert severity="success">{success}</Alert> : null}

      <TextField label="First Name" value={firstName} onChange={(event) => setFirstName(event.target.value)} required />
      <TextField label="Last Name" value={lastName} onChange={(event) => setLastName(event.target.value)} required />
      <TextField label="Email" type="email" value={email} onChange={(event) => setEmail(event.target.value)} required />
      <TextField
        label="Phone Number"
        value={phoneNumber}
        onChange={(event) => setPhoneNumber(event.target.value)}
        required
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        required
      />
      <TextField
        select
        label="Role"
        value={role}
        onChange={(event) => setRole(event.target.value as UserRole)}
        required
      >
        {roleOptions.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </TextField>

      <Button type="submit" variant="contained" disabled={isLoading}>
        {isLoading ? "Creating account..." : "Sign up"}
      </Button>

      <Typography variant="body2" color="text.secondary">
        Already have an account? <RouterLink to="/login">Login</RouterLink>
      </Typography>
    </Box>
  );
};

