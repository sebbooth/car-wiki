import { Auth, CarCRUD, CarList, DumpDB, FileUpload } from "./components";

function App() {
  return (
    <>
      <Auth />
      <FileUpload />
      <DumpDB />
      <CarList />
    </>
  );
}

export default App;
