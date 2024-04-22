import React from 'react'
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import debounce from 'lodash.debounce';
import axios from 'axios';

import SimpleSlider from '../components/SimpleSlider';

import arrow from '../assets/main-arrow.svg';
import search from '../assets/search.png';
import ProfessionItem from '../components/ProfessionItem';
import SkillItem from '../components/SkillItem';


const MainPage = () => {
  const [professionModal, setProffesionModal] = React.useState(false);
  const [skillsModal, setSkillsModal] = React.useState(false);

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

  return (
    <>
    <h1 className='main__title'>Найти вакансии в проектах МИЭМ</h1>
    <div className="main__params">
        <div className={professionModal ? 'main__professions active' : 'main__professions'} onClick={() => {setProffesionModal(!professionModal); setSkillsModal(false);}}>
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
                    {(searchP == '') ? professions && professions.map((item) => {
                          return <ProfessionItem id={item.id} name={item.name}/>
                    }) : filteredProfessions.map((item) => {
                        return <ProfessionItem id={item.id} name={item.name.charAt(0).toUpperCase() + item.name.slice(1)}/>
                    })}
                    {((searchP !== '') && (filteredProfessions.length == 0) && (!isLoadingP)) && <div className='search__param-none'>Ничего не найдено</div>}
              </div>
            </div>}
        </div>
        <div className={skillsModal ? 'main__skills active' : 'main__skills'} onClick={() => {setSkillsModal(!skillsModal); setProffesionModal(false);}}>
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
                    {(searchS == '') ? skills && skills.map((item) => {
                          return <SkillItem id={item.id} name={item.name}/>
                    }) : filteredSkills.map((item) => {
                        return <SkillItem id={item.id} name={item.name.charAt(0).toUpperCase() + item.name.slice(1)}/>
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