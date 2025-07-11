import { useState } from "react";
import axios from "axios";

function Search() {
  const [quotes, setQuotes] = useState([]); // State to hold quotes

  const handleScrape = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/scrape");
      setQuotes(response.data);
    } catch (error) {
      console.error("Error scraping data:", error);
    }
  };

  return (
    <div className="mt-6">
      <button
        onClick={handleScrape}
        className="bg-blue-500 text-white p-2 rounded"
      >
        Scrape
      </button>
      <ul>
        {quotes.map((quote, index) => (
          <li key={index} className="border-b border-gray-300 p-2">
            {quote.text}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Search;
