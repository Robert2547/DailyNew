import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    open: true,
    host: true,
    proxy: {
      "/api/v1/auth": {
        target: "http://localhost:8001",
        changeOrigin: true,
      },
      "/api/v1/profiles": {
        target: "http://localhost:8002",
        changeOrigin: true,
      },
    },
  },
});
