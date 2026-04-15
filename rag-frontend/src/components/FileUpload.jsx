// src/components/FileUpload.jsx
import { useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Typography,
  LinearProgress,
  TextField,
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
    formData.append("file", file);
    formData.append("user_id", "user_1");
    formData.append("thread_id", "thread_ai");

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
    <Box textAlign="center">
      <Typography variant="h5" gutterBottom>
        Upload Document
      </Typography>

      <TextField
        type="file"
        fullWidth
        onChange={(e) => setFile(e.target.files[0])}
        sx={{ my: 2 }}
        InputLabelProps={{ shrink: true }}
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
    </Box>
  );
}