import React, {Suspense} from 'react'
import { Route, Routes } from "react-router-dom";
import { useDispatch } from 'react-redux';
import { MainPage } from "./pages/MainPage";
import { SearchPage } from './pages/SearchPage';
import { CatalogPage } from "./pages/CatalogPage";
import { StatsPage } from './pages/StatsPage';

import { fetchProfessions, fetchSkills } from './redux/reducers/searchParamsSlice';

function App() {

	const dispatch = useDispatch();

	React.useEffect(() => {
		dispatch(fetchProfessions());
		dispatch(fetchSkills());
	}, [dispatch]);

	


	return (
	<div className="container">
		<Suspense fallback={<div>Loading...</div>}>
			<Routes>
				<Route path="/" element={<MainPage/>} />
				<Route path="/search" element={<SearchPage/>}/>
				<Route path="/stats" element={<StatsPage/>}/>
				<Route path="/catalog/:currentCatalog" element={<CatalogPage/>}/>
			</Routes>
		</Suspense>
	</div>
	);
}

export default App;
