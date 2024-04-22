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
  const [searchS, setSearchS] = React.useState('');

  const [filteredProfessions, setFilteredProfessions] = React.useState([]);

  const loadProfessions = React.useCallback(async (searchTerm) => {
    try {
      const response = await axios.get(`http://10.193.60.137:8000/api/search/?q=${searchTerm}`);
      const professions = response.data; 
      setFilteredProfessions(professions);
    } catch (error) {
      console.error('Ошибка загрузки направлений:', error);
    }
  }, []);
  const debouncedLoadProfessions = React.useCallback(debounce(loadProfessions, 300), [loadProfessions]);

  React.useEffect(() => {
    if (searchP) {
      debouncedLoadProfessions(searchP);
    } else {
      setFilteredProfessions([]);
    }
    return () => debouncedLoadProfessions.cancel();
  }, [searchP, debouncedLoadProfessions]);

  const skills = useSelector(state => state.searchParams.skills);
  const professions = useSelector(state => state.searchParams.professions);

  // const filteredProfessions = professions.filter(item =>
  //   item.name.toLowerCase().includes(searchP.toLowerCase())
  // );

  const filteredSkills = skills.filter(item =>
    item.name.toLowerCase().includes(searchS.toLowerCase())
  );

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
                    {filteredSkills && filteredSkills.map((item) => {
                      return <SkillItem name={item.name}/>
                    })}
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