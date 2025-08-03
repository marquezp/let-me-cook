import { useState } from "react";
import axios from "axios";

function Search() {
  const [recipes, setRecipes] = useState([]); // State to hold recipes

  const handleScrape = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/scrape");
      console.log("response.data:", response.data);
      setRecipes(response.data.data);
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
        {recipes.map((recipe, index) => (
          <li key={index} className="border-b border-gray-300 p-2">
            <h2 className="text-md font-bold">{recipe.title}</h2>
            <a href={recipe.url} target="_blank" rel="noopener noreferrer">
              {recipe.url}
            </a>
            <ul>
              {recipe.ingredients.map((ingredient, index) => (
                <li key={index}>{ingredient}</li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Search;
