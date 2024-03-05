import { defineConfig } from "vite";
import { splitVendorChunkPlugin } from "vite";
import react from "@vitejs/plugin-react";

import path from "path";
import dotenv from "dotenv";

// Load environment variables from the .env file in the parent directory
const envPath = path.resolve(__dirname, "./.env");
const envVariables = dotenv.config({ path: envPath }).parsed;

// https://vitejs.dev/config/
export default defineConfig({
  base: "/car-wiki/",
  plugins: [react(), splitVendorChunkPlugin()],
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (id.includes("node_modules")) {
            return id
              .toString()
              .split("node_modules/")[1]
              .split("/")[0]
              .toString();
          }
        },
      },
    },
  },
  define: {
    "process.env": JSON.stringify(envVariables),
  },
});
