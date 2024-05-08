import React from 'react'
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import axios from 'axios';
import search from '../assets/search.png';
import VacancyCard from '../components/VacancyCard';
import ProfessionItem from '../components/ProfessionItem';
import SkillItem from '../components/SkillItem';
import Loader from '../components/Loader';
import config from '../config';

import { useDebouncedSearch } from '../hooks/useDebouncedSearch';

const loaderData = [0, 0, 0, 0, 0];

const SearchPage = () => {

  const {
    input: searchP,
    setInput: setSearchP,
    data: filteredProfessions,
    isLoading: isLoadingP
  } = useDebouncedSearch(`${config.API_URL}/api/role_search/`, 300);

  const {
    input: searchS,
    setInput: setSearchS,
    data: filteredSkills,
    isLoading: isLoadingS
  } = useDebouncedSearch(`${config.API_URL}/api/skill_search/`, 300);

  const [data, setData] = React.useState([]);
  const [allData, setAllData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);

  const [showFavorites, setShowFavorites] = React.useState(false);

  const [offset, setOffset] = React.useState(10);

  const skills = useSelector(state => state.searchParams.skills);
  const professions = useSelector(state => state.searchParams.professions);
  

  const selectedProfessionsIds = professions.filter(professions => professions.isSelected);
  const selectedSkillsIds = skills.filter(skill => skill.isSelected);

  const selectedProfessionsCount = useSelector(state => state.searchParams.professions.filter(profession => profession.isSelected).length);
  const selectedSkillsCount = useSelector(state => state.searchParams.skills.filter(skill => skill.isSelected).length);

  const getData = () => {
    setIsLoading(true);
    const queryParamsProfessions = selectedProfessionsIds.map(item => `vacancy_tags=${item.sendName}`).join('&');
    const queryParamsSkills = selectedSkillsIds.map(item => `skill_tags=${item.sendName}`).join('&');
    axios.get(`${config.API_URL}/api/search_vacancies/?${queryParamsSkills}&${queryParamsProfessions}`)
    .then((data) => {   
        setData(data.data);
        setIsLoading(false);
    }).catch((e) => {
        alert('Ошибка получения вакансий')
        console.log(e);
        setIsLoading(false);
    })
  }

  const getAllData = () => {
    setIsLoading(true);
    axios.get(`${config.API_URL}/api/search_vacancies/?&$`)
    .then((data) => {   
        setAllData(data.data);
        setIsLoading(false);
    }).catch((e) => {
        alert('Ошибка получения вакансий')
        console.log(e);
        setIsLoading(false);
    })
  }

  React.useEffect(() => {
    getAllData();
  }, [])


  React.useEffect(() => {
    getData();
  }, [skills, professions])

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
      <h2>Поиск вакансий</h2>
    </div>
    <div className="search__content">
      <div className="search__params">
        <div className="search__param-wrapper">
          <div className="search__param-name">Направления
            <span>+{selectedProfessionsCount}</span> 
          </div>  
          <div className="search__param-line"></div>
          <div className="search__param-search">
            <input placeholder='Поиск направления' value={searchP} onChange={(e) => setSearchP(e.target.value)}></input>  
            <img src={search} alt="search" />
          </div>  
          <div className="search__param-select">
            {(searchP === '') ? professions && [...professions].sort((a, b) => {
                        if (a.isSelected && !b.isSelected) {
                          return -1; 
                        }
                        if (b.isSelected && !a.isSelected) {
                          return 1; 
                        }
                        return 0;
                        }).map((item) => {
                return <ProfessionItem id={item.id} key={item.id} name={item.name}/>
            }) : filteredProfessions.map((item) => {
              return <ProfessionItem id={item.id} key={item.id} name={item.name?.charAt(0).toUpperCase() + item.name?.slice(1)}/>
          })}
          {((searchP !== '') && (filteredProfessions.length == 0) && (!isLoadingP)) && <div className='search__param-none'>Ничего не найдено</div>}
          </div>
        </div>

        <div className="search__param-wrapper">
          <div className="search__param-name">Навыки
            <span>+{selectedSkillsCount}</span> 
          </div>  
          <div className="search__param-line"></div>
          <div className="search__param-search">
            <input placeholder='Поиск навыков' value={searchS} onChange={(e) => setSearchS(e.target.value)}></input>  
            <img src={search} alt="search" />
          </div>    
          <div className="search__param-select">
            {(searchS === '') ? skills && [...skills].sort((a, b) => {
                        if (a.isSelected && !b.isSelected) {
                          return -1; 
                        }
                        if (b.isSelected && !a.isSelected) {
                          return 1; 
                        }
                        return 0;
                        }).map((item) => {
                  return <SkillItem id={item.id} key={item.id} name={item.name}/>
            }) : filteredSkills.map((item) => {
                return <SkillItem id={item.id} key={item.id} name={item.name?.charAt(0).toUpperCase() + item.name?.slice(1)}/>
            })}
            {((searchS !== '') && (filteredSkills.length == 0) && (!isLoadingS)) && <div className='search__param-none'>Ничего не найдено</div>}
          </div>
        </div>
      </div>
      <div className="search__result">
            <div className="search__result-header">
              <div className="title">Вакансия</div>
              <div className="title">Проект</div>
              <div className="title">Стадия проекта</div>
              <button className='search__favorite' onClick={() => setShowFavorites(!showFavorites)}>{showFavorites ? 'Скрыть избранное' : 'Показать избранное'}</button>
            </div>
            {data && !isLoading && !showFavorites && data.slice(0, offset).map((item) =>  {
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
            {allData && !isLoading && showFavorites && allData.slice(0, offset).map((item) =>  {
              if (favorites.includes(item.vacancy_id)) {
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
              />}
            })}
            {isLoading && loaderData.map((item, i) => {
              return <Loader key={i}/>
            })}
            {!isLoading && !showFavorites && offset < data.length && <div className="search__more">
              <button onClick={() => {setOffset(offset + 10)}}>Показать еще</button>
            </div>}
      </div>
    </div>

    
    </>
  )
}

export default SearchPage;