import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";
import dotenv from "dotenv";

// Load environment variables from the .env file in the parent directory
const envPath = path.resolve(__dirname, "../.env");
const envVariables = dotenv.config({ path: envPath }).parsed;

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    "process.env": JSON.stringify(envVariables),
  },
});
