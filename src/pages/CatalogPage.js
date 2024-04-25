import React from 'react'
import { Link } from 'react-router-dom';

import arrow from '../assets/nav-arrow.svg';
import VacancyCard from '../components/VacancyCard';        

const CatalogPage = () => {
  return (
        <>
        <div className="page__title">
          <Link to='/'>
            <svg width="8" height="14" viewBox="0 0 8 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M7 13L1 7L7 1" stroke="#072551" stroke-opacity="0.75" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </Link>
          <h2>Подборка вакансий: Вакансии для frontend-разработчиков</h2>
        </div>

        <div className="catalog__content-wrapper">
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
            </div>
            <div className="catalog__more">
                <span>Смотрите также:</span>
                <div className="catalog__more-content">
                    <div className="catalog__more-item">
                        <p>Вакансии для 3d&#160;разработчиков</p>
                    </div>  
                    <div className="catalog__more-item">
                        <p>Вакансии для 3d&#160;разработчиков</p>
                    </div>
                    <div className="catalog__more-item">
                        <p>Вакансии для 3d&#160;разработчиков</p> 
                    </div>
                </div>
            </div>
        </div>
        
        </>
  )
}

export default CatalogPage;