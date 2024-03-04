import {
  Auth,
  CarCRUD,
  CarList,
  DumpDB,
  DumpFields,
  DumpFieldsByCategory,
  SelectFieldCategories,
  FileUpload,
} from "./components";

import { SearchContextProvider } from "./contexts/SearchContext";

function App() {
  return (
    <>
      <Auth />
      <FileUpload />
      <DumpDB />
      <DumpFields />
      <DumpFieldsByCategory />
      <SearchContextProvider>
        <SelectFieldCategories />
        <CarList />
      </SearchContextProvider>
    </>
  );
}

export default App;
