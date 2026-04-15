// src/components/ResponseBox.jsx
import { Box, Typography, Divider } from "@mui/material";
import SmartToyIcon from "@mui/icons-material/SmartToy";

export default function ResponseBox({ answer }) {
  if (!answer) return null;

  return (
    <Box textAlign="left">
      <Typography variant="h5" gutterBottom>
        <SmartToyIcon sx={{ mr: 1 }} />
        Answer
      </Typography>
      <Divider sx={{ mb: 2 }} />
      <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
        {answer}
      </Typography>
    </Box>
  );
}