import { Drawer, List, ListItemButton, ListItemText, Toolbar } from "@mui/material";
import { Link, useLocation } from "react-router-dom";

import type { UserRole } from "@/types/auth";

const drawerWidth = 260;

interface NavItem {
  label: string;
  path: string;
  roles: UserRole[];
}

const navItems: NavItem[] = [
  { label: "Home", path: "/", roles: ["customer"] },
  { label: "Products", path: "/products", roles: ["customer"] },
  { label: "Cart", path: "/cart", roles: ["customer"] },
  { label: "Orders", path: "/orders", roles: ["customer", "seller", "admin", "support_admin"] },
  { label: "Seller Dashboard", path: "/seller/dashboard", roles: ["seller"] },
  { label: "Seller Products", path: "/seller/products", roles: ["seller"] },
  { label: "Seller Inventory", path: "/seller/inventory", roles: ["seller"] },
  { label: "Admin Dashboard", path: "/admin/dashboard", roles: ["admin", "support_admin"] },
  { label: "Users", path: "/admin/users", roles: ["admin", "support_admin"] },
  { label: "Payments", path: "/admin/payments", roles: ["admin", "support_admin"] },
];

interface AppSidebarProps {
  open: boolean;
  onClose: () => void;
  role: UserRole;
}

export const AppSidebar = ({ open, onClose, role }: AppSidebarProps) => {
  const location = useLocation();
  const items = navItems.filter((item) => item.roles.includes(role));

  return (
    <Drawer
      variant="temporary"
      open={open}
      onClose={onClose}
      sx={{
        "& .MuiDrawer-paper": {
          width: drawerWidth,
          boxSizing: "border-box",
        },
      }}
    >
      <Toolbar />
      <List>
        {items.map((item) => (
          <ListItemButton
            key={item.path}
            component={Link}
            to={item.path}
            selected={location.pathname === item.path}
            onClick={onClose}
          >
            <ListItemText primary={item.label} />
          </ListItemButton>
        ))}
      </List>
    </Drawer>
  );
};

