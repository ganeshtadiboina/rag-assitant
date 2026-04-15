// src/App.jsx
import { useState } from "react";
import { Container, Typography, Box, Grid, Paper } from "@mui/material";
import FileUpload from "./components/FileUpload";
import QueryBox from "./components/QueryBox";
import ResponseBox from "./components/ResponseBox";
import "./App.css";

function App() {
  const [answer, setAnswer] = useState("");

  return (
    <Box className="background">
      <Container maxWidth="md" sx={{ py: 6 }}>
        <Typography
          variant="h3"
          align="center"
          gutterBottom
          sx={{ fontWeight: "bold", color: "#00e5ff" }}
        >
          🤖 RAG Assistant
        </Typography>

        <Typography
          variant="subtitle1"
          align="center"
          sx={{ mb: 4, color: "rgba(255,255,255,0.7)" }}
        >
          Built with LangChain, Qdrant Vector Search, BM25, Cross-Encoder Reranking, and OpenAI GPT.
        </Typography>

        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Paper elevation={6} sx={{ p: 3 }}>
              <FileUpload />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={6} sx={{ p: 3 }}>
              <QueryBox setAnswer={setAnswer} />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper elevation={6} sx={{ p: 3 }}>
              <ResponseBox answer={answer} />
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;