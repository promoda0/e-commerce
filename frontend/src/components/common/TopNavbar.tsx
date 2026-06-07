import MenuIcon from "@mui/icons-material/Menu";
import LogoutIcon from "@mui/icons-material/Logout";
import { AppBar, Box, IconButton, Toolbar, Typography, Button } from "@mui/material";

import { useAuth } from "@/store/AuthContext";

interface TopNavbarProps {
  onToggleSidebar: () => void;
}

export const TopNavbar = ({ onToggleSidebar }: TopNavbarProps) => {
  const { user, logout } = useAuth();

  return (
    <AppBar position="fixed" color="inherit" elevation={1}>
      <Toolbar>
        <IconButton edge="start" onClick={onToggleSidebar} sx={{ mr: 2 }}>
          <MenuIcon />
        </IconButton>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>
          E-Commerce Portal
        </Typography>
        <Box display="flex" alignItems="center" gap={2}>
          <Typography variant="body2">{user?.role ?? "guest"}</Typography>
          <Button startIcon={<LogoutIcon />} color="inherit" onClick={logout}>
            Logout
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

