import { Route, Routes } from "react-router-dom"
import MainPage from "./pages/MainPage";
import SearchPage from './pages/SearchPage';
import CatalogPage from "./pages/CatalogPage";

function App() {
  return (
    <div className="container">
		<Routes>
			<Route path="/" element={<MainPage/>} />
			<Route path="/search" element={<SearchPage/>}/>
			<Route path="/catalog" element={<CatalogPage/>}/>
		</Routes>
    </div>
  );
}

export default App;
