import { Paper, Typography, Divider, Box } from "@mui/material";

export default function ResponseBox({ answer }) {
  if (!answer || !answer.answer) return null;

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        Answer
      </Typography>

      <Divider sx={{ mb: 2 }} />

      <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
        {answer.answer}
      </Typography>

      {answer.sources?.length > 0 && (
        <Box mt={2}>
          <Typography variant="subtitle2">Sources:</Typography>
          {answer.sources.map((src, idx) => (
            <Typography key={idx} variant="caption" display="block">
              {src.tag} → {src.source}
            </Typography>
          ))}
        </Box>
      )}
    </Paper>
  );
}