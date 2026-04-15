// src/components/QueryBox.jsx
import { useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Typography,
  TextField,
  CircularProgress,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";

const API_URL = import.meta.env.VITE_API_URL;

export default function QueryBox({ setAnswer }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const handleQuery = async () => {
    if (!query.trim()) {
      alert("Please enter a question.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/query`, {
        query,
        thread_id: "thread_ai",
      });
      setAnswer(res.data.answer);
    } catch (error) {
      console.error("Query error:", error);
      alert("Query failed. Please ensure the backend server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box textAlign="center">
      <Typography variant="h5" gutterBottom>
        Ask a Question
      </Typography>

      <TextField
        fullWidth
        label="Enter your question"
        variant="outlined"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        sx={{ my: 2 }}
      />

      <Button
        variant="contained"
        startIcon={<SearchIcon />}
        onClick={handleQuery}
        disabled={loading}
      >
        {loading ? <CircularProgress size={24} /> : "Ask"}
      </Button>
    </Box>
  );
}