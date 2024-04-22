import React from 'react'
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import axios from 'axios';
import debounce from 'lodash.debounce';

import arrow from '../assets/nav-arrow.svg';
import search from '../assets/search.png';
import VacancyCard from '../components/VacancyCard';
import ProfessionItem from '../components/ProfessionItem';
import SkillItem from '../components/SkillItem';
import Loader from '../components/Loader';

const loaderData = [0, 0, 0, 0, 0];

const SearchPage = () => {

  const [data, setData] = React.useState([]);
  const [isLoading, setIsLoading] = React.useState(false);

  const [showFavorites, setShowFavorites] = React.useState(false);

  const [offset, setOffset] = React.useState(10);

  const [searchP, setSearchP] = React.useState(''); 
  const [isLoadingP, setIsLoadingP] = React.useState(false);

  const [searchS, setSearchS] = React.useState('');
  const [isLoadingS, setIsLoadingS] = React.useState(false);

  const [filteredProfessions, setFilteredProfessions] = React.useState([]);
  const [filteredSkills, setFilteredSkills] = React.useState([]);

  const loadProfessions = React.useCallback(async (searchTerm) => {
    try {
      const response = await axios.get(`http://10.193.60.137:8000/api/search/?q=${searchTerm}`);
      const professions = response.data; 
      setFilteredProfessions(professions);
      setIsLoadingP(false);
    } catch (error) {
      console.error('Ошибка загрузки направлений:', error);
      setIsLoadingP(false);
    }
  }, []);
  const debouncedLoadProfessions = React.useCallback(debounce(loadProfessions, 300), [loadProfessions]);

  const loadSkills = React.useCallback(async (searchTerm) => {
    try {
      const response = await axios.get(`http://10.193.60.137:8000/api/search/?q=${searchTerm}`);
      const skills = response.data; 
      setFilteredSkills(skills);
      setIsLoadingS(false);
    } catch (error) {
      console.error('Ошибка загрузки направлений:', error);
      setIsLoadingS(false);
    }
  }, []);
  const debouncedLoadSkills = React.useCallback(debounce(loadSkills, 300), [loadSkills]);

  React.useEffect(() => {
    if (searchP) {
      setIsLoadingP(true);
      debouncedLoadProfessions(searchP);
    } else {
      setFilteredProfessions([]);
    }
    return () => debouncedLoadProfessions.cancel();
  }, [searchP, debouncedLoadProfessions]);

  React.useEffect(() => {
    if (searchS) {
      setIsLoadingS(true);
      debouncedLoadSkills(searchS);
    } else {
      setFilteredSkills([]);
    }
    return () => debouncedLoadSkills.cancel();
  }, [searchS, debouncedLoadSkills]);

  const skills = useSelector(state => state.searchParams.skills);
  const professions = useSelector(state => state.searchParams.professions);

  const selectedProfessionsCount = useSelector(state => state.searchParams.professions.filter(profession => profession.isSelected).length);
  const selectedSkillsCount = useSelector(state => state.searchParams.skills.filter(skill => skill.isSelected).length);

  const getData = () => {
    setIsLoading(true);
    axios.get(`http://10.193.60.137:8000/vacancies`)
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
  }, [])

  function getFavorites() {
    return JSON.parse(localStorage.getItem('favorites')) || [];
  }

  let favorites = getFavorites();

  return (
    <>
    <div className="page__title">
      <Link to='/'>
        <img src={arrow} alt="" />
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
            {(searchP == '') ? professions && professions.map((item) => {
                return <ProfessionItem id={item.id} name={item.name}/>
            }) : filteredProfessions.map((item) => {
              return <ProfessionItem id={item.id} name={item.name.charAt(0).toUpperCase() + item.name.slice(1)}/>
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
            {(searchS == '') ? skills && skills.map((item) => {
                  return <SkillItem id={item.id} name={item.name}/>
            }) : filteredSkills.map((item) => {
                return <SkillItem id={item.id} name={item.name.charAt(0).toUpperCase() + item.name.slice(1)}/>
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
              <button onClick={() => setShowFavorites(!showFavorites)}>Кнопка</button>
            </div>
            {data && !isLoading && data.slice(0, offset).map((item) =>  {
            if (!showFavorites) {
              return <VacancyCard vacancyName={item.vacancy_name}
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
              />} else {
                if (favorites.includes(item.vacancy_id)) {
                  return <VacancyCard vacancyName={item.vacancy_name}
                                  isFavorite={favorites.includes(item.vacancy_id) ? true : false}
                                  vacancyId={item.vacancy_id}
                                  projectId={item.project_id}
                                  projectName={item.project_name}
                                  projectType={item.project_type}
                                  projectHead={item.project_head}
                                  projectStage={item.project_stage}
                                  projectUrl={item.project_url}
                                  vacancyDisciplines={item.vacancy_disciplines}
                                  vacancyAdditionally={item.vacancy_additionally}/>
                }
              }
            }
            
            )}
            {isLoading && loaderData.map(item => {
              return <Loader/>
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