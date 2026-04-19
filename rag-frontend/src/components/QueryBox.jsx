import { useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Typography,
  TextField,
  CircularProgress,
  Paper,
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

    const threadId = localStorage.getItem("thread_id");

    // ❗ Critical check
    if (!threadId) {
      alert("Please upload a document first.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/query`, {
        query,
        thread_id: threadId,
      });

      setAnswer(res.data);
    } catch (error) {
      console.error("Query error:", error);
      alert(
        error?.response?.data?.detail ||
          "Query failed. Ensure backend is running."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
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

      {/* ✅ Show thread context */}
      <Typography variant="caption" display="block" sx={{ mt: 2 }}>
        Querying Thread: {localStorage.getItem("thread_id") || "None"}
      </Typography>
    </Paper>
  );
}