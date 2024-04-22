import React from 'react'
import { Route, Routes } from "react-router-dom";
import { useDispatch } from 'react-redux';
import MainPage from "./pages/MainPage";
import SearchPage from './pages/SearchPage';
import CatalogPage from "./pages/CatalogPage";

import { fetchProfessions } from './redux/reducers/searchParamsSlice';

function App() {

	const dispatch = useDispatch();

	React.useEffect(() => {
		dispatch(fetchProfessions());
	}, [dispatch]);


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