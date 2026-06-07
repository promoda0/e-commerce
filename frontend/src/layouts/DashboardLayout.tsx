import { Box, Toolbar } from "@mui/material";
import { useState } from "react";
import { Outlet } from "react-router-dom";

import { AppSidebar } from "@/components/common/AppSidebar";
import { TopNavbar } from "@/components/common/TopNavbar";
import { useAuth } from "@/store/AuthContext";

export const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const { user } = useAuth();

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <TopNavbar onToggleSidebar={() => setSidebarOpen((prev) => !prev)} />
      {user ? <AppSidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} role={user.role} /> : null}
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
};

