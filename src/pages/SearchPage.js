import React from 'react'
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import axios from 'axios';

import arrow from '../assets/nav-arrow.svg';
import search from '../assets/search.png';
import VacancyCard from '../components/VacancyCard';
import ProfessionItem from '../components/ProfessionItem';
import SkillItem from '../components/SkillItem';

const SearchPage = () => {

  const skills = useSelector(state => state.searchParams.skills);
  const professions = useSelector(state => state.searchParams.professions);

  const selectedProfessionsCount = useSelector(state => state.searchParams.professions.filter(profession => profession.isSelected).length);
  const selectedSkillsCount = useSelector(state => state.searchParams.skills.filter(skill => skill.isSelected).length);

  console.log('kek');

  const getData = () => {
    axios.get(`http://10.193.61.85:8000/vacancies`)
    .then((data) => {   
        console.log(data)
        alert('then')
    }).catch((e) => {
        alert('catch')
        console.log(e);
    })
}
  
  
  React.useEffect(() => {
    getData();
  }, [])

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
          <div className="search__param-name">Направление
            <span>+{selectedProfessionsCount}</span> 
          </div>  
          <div className="search__param-line"></div>
          <div className="search__param-search">
            <input placeholder='Поиск направления'></input>  
            <img src={search} alt="search" />
          </div>    
          <div className="search__param-select">
            {professions && professions.map((item) => {
                return <ProfessionItem name={item.name}/>
            })}
          </div>
        </div>

        <div className="search__param-wrapper">
          <div className="search__param-name">Навыки
            <span>+{selectedSkillsCount}</span> 
          </div>  
          <div className="search__param-line"></div>
          <div className="search__param-search">
            <input placeholder='Поиск навыков'></input>  
            <img src={search} alt="search" />
          </div>    
          <div className="search__param-select">
            {skills && skills.map((item) => {
                return <SkillItem name={item.name}/>
            })}
          </div>
        </div>
      </div>
      <div className="search__result">
            <div className="search__result-header">
              <div className="title">Вакансия</div>
              <div className="title">Проект</div>
              <div className="title">Стадия проекта</div>
            </div>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
            <VacancyCard/>
      </div>
    </div>

    
    </>
  )
}

export default SearchPage;