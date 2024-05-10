import React from 'react'
import { Link, useParams } from 'react-router-dom';
import { useSelector } from 'react-redux';
import axios from 'axios'

import VacancyCard from '../components/VacancyCard';       
import Loader from '../components/Loader';
import config from '../config';


// const currentCatalog = 'intern';
const loaderData = [0, 0, 0, 0, 0];
const moreData=[0,0,0];

const CatalogPage = () => {

  let { currentCatalog } = useParams();

  const currentCatalogItem = useSelector(state => state.searchParams.catalogItems).filter(item => item.tag == currentCatalog);
  const catalogItems = useSelector(state => state.searchParams.catalogItems).filter(item => item.tag != currentCatalog);
  
console.log(currentCatalogItem)

  const [data, setData] = React.useState([]);
  const [offset, setOffset] = React.useState(10);
  const [isLoading, setIsLoading] = React.useState(false);

  const getData = () => {
    setIsLoading(true);
    axios.get(`${config.API_URL}/api/search_vacancies/?vacancy_tags=${encodeURIComponent(currentCatalog)}`)
    .then((data) => {   
        setData(data.data);
        setIsLoading(false);
    }).catch((e) => {
        alert('Ошибка получения вакансий')
        console.log(e);
        setIsLoading(false);
    })
  }

  React.useEffect(() => {
    getData();
  }, [currentCatalog])

  function getFavorites() {
    return JSON.parse(localStorage.getItem('favorites')) || [];
  }

  let favorites = getFavorites();

  return (
        <>
        <div className="page__title">
          <Link to='/'>
            <svg width="8" height="14" viewBox="0 0 8 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 13L1 7L7 1" stroke="#072551" strokeOpacity="0.75" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </Link>
          <h2>Подборка вакансий: Вакансии для {currentCatalogItem[0].name}</h2>
        </div>

        <div className="catalog__content-wrapper">
            <div className="search__result">
                <div className="search__result-header">
                <div className="title">Вакансия</div>
                <div className="title">Проект</div>
                <div className="title">Стадия проекта</div>
                </div>
                {data && !isLoading && data.slice(0, offset).map((item) =>  {
                return <VacancyCard vacancyName={item.vacancy_name}
                                    vacancyCount={item.vacancy_count}
                                    isFavorite={favorites.includes(item.vacancy_id) ? true : false}
                                    vacancyId={item.vacancy_id}
                                    projectId={item.project_id}
                                    projectName={item.project_name}
                                    projectType={item.project_type}
                                    projectHead={item.project_head}
                                    projectStage={item.project_stage}
                                    projectUrl={item.project_url}
                                    vacancyDisciplines={item.vacancy_disciplines}
                                    vacancyAdditionally={item.vacancy_additionally}
                                    key={item.vacancy_id}
                />
                })}
                {isLoading && loaderData.map((item, i) => {
                return <Loader key={i}/>
                })}
                {!isLoading && offset < data.length && <div className="search__more">
                    <button onClick={() => {setOffset(offset + 10)}}>Показать еще</button>
                </div>}
            </div>
            <div className="catalog__more">
                <span>Смотрите также:</span>
                <div className="catalog__more-content">
                    {moreData.map((item, i) => {
                        return <Link to={`/catalog/${catalogItems[i].tag}`}>
                        <div className='catalog__more-item'>
                      <span>Вакансии для {catalogItems[i].name}</span>
                    </div>
                    </Link> 
                    })}
                </div>
            </div>
        </div>
        
        </>
  )
}

export default CatalogPage;