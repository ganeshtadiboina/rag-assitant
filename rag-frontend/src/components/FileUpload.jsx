import { useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Typography,
  LinearProgress,
  Paper,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";

const API_URL = import.meta.env.VITE_API_URL;

export default function FileUpload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    const threadId = crypto.randomUUID();

    formData.append("file", file);
    formData.append("user_id", "user_1");
    formData.append("thread_id", threadId);

    // ✅ Store thread_id for querying
    localStorage.setItem("thread_id", threadId);

    setLoading(true);
    try {
      await axios.post(`${API_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      alert("Document uploaded successfully!");
      setFile(null);
    } catch (error) {
      console.error("Upload error:", error);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
      <Typography variant="h5" gutterBottom>
        Upload Document
      </Typography>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        style={{ margin: "1rem 0" }}
      />

      {loading && <LinearProgress sx={{ mb: 2 }} />}

      <Button
        variant="contained"
        startIcon={<CloudUploadIcon />}
        onClick={handleUpload}
        disabled={loading}
      >
        {loading ? "Uploading..." : "Upload"}
      </Button>

      {/* ✅ Show active thread */}
      <Typography variant="caption" display="block" sx={{ mt: 2 }}>
        Active Thread: {localStorage.getItem("thread_id") || "None"}
      </Typography>
    </Paper>
  );
}