import { createContext, useState } from "react";

const SearchContext = createContext();

const SearchContextProvider = ({ children }) => {
  const [searchFields, setSearchFields] = useState({});

  const changeSearchFields = (category, fields) => {
    const newSearchFields = searchFields;
    newSearchFields[category] = fields;
    setSearchFields(newSearchFields);
  };

  return (
    <SearchContext.Provider
      value={{
        searchFields,
        changeSearchFields,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
};

export { SearchContext, SearchContextProvider };
