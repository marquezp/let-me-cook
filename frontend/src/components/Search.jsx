import React from "react";

function Search() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <input
        className="text-center border border-gray-400 p-1 rounded"
        type="text"
        placeholder="Search for recipes..."
      />
    </div>
  );
}

export default Search;
