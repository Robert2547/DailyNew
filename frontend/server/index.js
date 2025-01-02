// server/index.js
const express = require("express");
const cors = require("cors");
const axios = require("axios");

const app = express();
app.use(cors());

app.get("/api/search", async (req, res) => {
  try {
    const { query } = req.query;
    const response = await axios.get(
      `https://query2.finance.yahoo.com/v6/finance/autocomplete`,
      {
        params: {
          query,
          lang: "en",
          region: "US",
        },
        headers: {
          "User-Agent": "Mozilla/5.0",
        },
      }
    );
    res.json(response.data);
  } catch (error) {
    console.error("Search error:", error);
    res.status(500).json({ error: "Failed to fetch data" });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
