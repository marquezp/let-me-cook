import { useState } from "react";
import axios from "axios";

function Search() {
  const [books, setBooks] = useState([]); // State to hold books

  const handleScrape = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/scrape");
      console.log("response.data:", response.data);
      setBooks(response.data.data);
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
        {books.map((book, index) => (
          <li key={index} className="border-b border-gray-300 p-2">
            <h2 className="text-md font-bold">
              {book.title} - {book.price}
            </h2>
            <p>{book.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Search;
