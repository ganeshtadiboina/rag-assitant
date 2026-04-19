import { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Grid,
  Paper,
  Chip,
} from "@mui/material";
import FileUpload from "./components/FileUpload";
import QueryBox from "./components/QueryBox";
import ResponseBox from "./components/ResponseBox";
import "./App.css";

function App() {
  const [answer, setAnswer] = useState(null);
  const threadId = localStorage.getItem("thread_id");

  return (
    <Box className="background">
      <Container maxWidth="md" sx={{ py: 6 }}>
        {/* 🔹 Title */}
        <Typography
          variant="h3"
          align="center"
          gutterBottom
          sx={{
            fontWeight: "bold",
            color: "#00e5ff",
            letterSpacing: 1,
          }}
        >
          RAG Assistant
        </Typography>

        {/* 🔹 Subtitle */}
        <Typography
          variant="subtitle1"
          align="center"
          sx={{ mb: 3, color: "rgba(255,255,255,0.7)" }}
        >
          Hybrid Retrieval (BM25 + Vector Search) • Qdrant • Cross-Encoder Reranking • OpenAI
        </Typography>

        {/* 🔹 Active Thread Indicator */}
        {threadId && (
          <Box sx={{ textAlign: "center" }}>
            <Chip
              label={`Active Thread: ${threadId.slice(0, 8)}...`}
              color="primary"
              variant="outlined"
            />
          </Box>
        )}

        {/* 🔹 Layout */}
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper elevation={8} sx={{ p: 3, backdropFilter: "blur(10px)" }}>
              <FileUpload />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={8} sx={{ p: 3, backdropFilter: "blur(10px)" }}>
              <QueryBox setAnswer={setAnswer} />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={8} sx={{ p: 3, backdropFilter: "blur(10px)" }}>
              <ResponseBox answer={answer} />
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;