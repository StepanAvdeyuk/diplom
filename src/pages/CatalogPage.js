import React from 'react'
import { Link } from 'react-router-dom';

import arrow from '../assets/nav-arrow.svg';
import VacancyCard from '../components/VacancyCard';        

const CatalogPage = () => {
  return (
        <>
        <div className="page__title">
          <Link to='/'>
            <img src={arrow} alt="" />
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