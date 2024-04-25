import React from 'react'
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';

import SimpleSlider from '../components/SimpleSlider';
import { useDebouncedSearch } from '../hooks/useDebouncedSearch';

import arrow from '../assets/main-arrow.svg';
import search from '../assets/search.png';
import ProfessionItem from '../components/ProfessionItem';
import SkillItem from '../components/SkillItem';
import config from '../config';

const MainPage = () => {

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

  const [professionModal, setProffesionModal] = React.useState(false);
  const [skillsModal, setSkillsModal] = React.useState(false);

  const skills = useSelector(state => state.searchParams.skills);
  const professions = useSelector(state => state.searchParams.professions);

  const selectedProfessionsCount = useSelector(state => state.searchParams.professions.filter(profession => profession.isSelected).length);
  const selectedSkillsCount = useSelector(state => state.searchParams.skills.filter(skill => skill.isSelected).length);

  const toggleProffesionsModal = () => {
    setProffesionModal(!professionModal); 
    setSkillsModal(false);
  }

  const toggleSkillsModal = () => {
    setSkillsModal(!skillsModal); 
    setProffesionModal(false);
  }

  return (
    <>
    <h1 className='main__title'>Найти вакансии в проектах МИЭМ</h1>
    <div className="main__params">
        <div className={professionModal ? 'main__professions active' : 'main__professions'} onClick={toggleProffesionsModal}>
            <span>Направления
              <div className="main__count">+{selectedProfessionsCount}</div>
            </span>
            <img className={professionModal ? 'active' : ''} src={arrow} alt="arrow"/>
            {professionModal && <div className="main__professions-modal" onClick={(e) => e.stopPropagation()}>
              <div className="main__search-input">
                <input type="text" placeholder='Поиск направления' value={searchP} onChange={(e) => setSearchP(e.target.value)}/>
                <img src={search} alt="search"/>                
              </div>
              <div className="main__search-list scrollBar">
                    {(searchP == '') ? professions && [...professions].sort((a, b) => {
                        if (a.isSelected && !b.isSelected) {
                          return -1; 
                        }
                        if (b.isSelected && !a.isSelected) {
                          return 1; 
                        }
                        return 0;
                        }).map((item) => {
                          return <ProfessionItem id={item.id} name={item.name}/>
                    }) : filteredProfessions.map((item) => {
                        return <ProfessionItem id={item.id} name={item.name?.charAt(0).toUpperCase() + item.name?.slice(1)}/>
                    })}
                    {((searchP !== '') && (filteredProfessions.length == 0) && (!isLoadingP)) && <div className='search__param-none'>Ничего не найдено</div>}
              </div>
            </div>}
        </div>
        <div className={skillsModal ? 'main__skills active' : 'main__skills'} onClick={toggleSkillsModal}>
            <span>Навыки
            <div className="main__count">+{selectedSkillsCount}</div>
            </span>
            <img src={arrow} className={skillsModal ? 'active' : ''} alt="arrow"/>
            {skillsModal && <div className="main__skills-modal" onClick={(e) => e.stopPropagation()} >
              <div className="main__search-input">
                <input type="text" placeholder='Поиск навыка' value={searchS} onChange={(e) => setSearchS(e.target.value)}/>
                <img src={search} alt="arrow"/>                
              </div>
              <div className="main__search-list scrollBar">
                    {(searchS == '') ? skills && [...skills].sort((a, b) => {
                        if (a.isSelected && !b.isSelected) {
                          return -1; 
                        }
                        if (b.isSelected && !a.isSelected) {
                          return 1; 
                        }
                        return 0;
                        }).map((item) => {
                          return <SkillItem id={item.id} name={item.name}/>
                    }) : filteredSkills.map((item) => {
                        return <SkillItem id={item.id} name={item.name?.charAt(0).toUpperCase() + item.name?.slice(1)}/>
                    })}
                    {((searchS !== '') && (filteredSkills.length == 0) && (!isLoadingS)) && <div className='search__param-none'>Ничего не найдено</div>}
              </div>
            </div>}
        </div>
        <Link to='/search'><button className="main__search">Найти вакансии</button></Link>
    </div>
    <h2 className="main__subtitle">
        Подборки вакансий
    </h2>
        <div className="main__slider">
            <SimpleSlider/>
        </div>   
    </>
  )
}

export default MainPage;