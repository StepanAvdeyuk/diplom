import React from 'react'

import arrow from '../assets/vac-arrow.svg';
import link from '../assets/link.png';
import heart from '../assets/heart.svg'; 

const VacancyCard = ({vacancyName, vacancyCount, isFavorite, vacancyId, projectId, projectName, projectType, projectHead, projectStage, projectUrl, vacancyDisciplines, vacancyAdditionally}) => {

  const [isModal, setIsModal] = React.useState(false);  
  const [isLiked, setIsLiked] = React.useState(isFavorite);  

  vacancyDisciplines = vacancyDisciplines.substring(1, vacancyDisciplines.length - 1).replace("Обязательно знать и уметь: ", "").replace(/'/g, "");
  vacancyAdditionally = vacancyAdditionally.substring(1, vacancyAdditionally.length - 1).replace("Желательно знать и уметь: ", "").replace(/'/g, "");

    let projectStageStatus = '';

    if (projectStage.length === 0) {
        projectStageStatus = "Не указано";
    } else {
        let completedStages = projectStage.filter(stage => stage.stage_status === 2);

        if (completedStages.length > 0) {
            let lastCompletedStage = completedStages[completedStages.length - 1];
            projectStageStatus = lastCompletedStage.stage_name;
        } else {
            projectStageStatus = "Готов к работе";
        }

        if (projectStage.every(stage => stage.stage_status === 2)) {
            projectStageStatus = "Проект защищен";
        }
    }


    function addToFavorites(vacancyId) {
        let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
        if (!favorites.includes(vacancyId)) {
            favorites.push(vacancyId);
            localStorage.setItem('favorites', JSON.stringify(favorites));
        }
    }
        
        // Удаление вакансии из избранного
    function removeFromFavorites(vacancyId) {
        let favorites = JSON.parse(localStorage.getItem('favorites')) || [];
        const index = favorites.indexOf(vacancyId);
        if (index !== -1) {
            favorites.splice(index, 1);
            localStorage.setItem('favorites', JSON.stringify(favorites));
        }
    }

  const toggleIsLiked = (e) => {
    e.stopPropagation();
    if (isLiked) {
        removeFromFavorites(vacancyId);
    } else {
        addToFavorites(vacancyId);
    }
    setIsLiked(!isLiked);
  }  

  return (
    <>
    <div className={isModal ? "vc__wrapper active" : "vc__wrapper"}>
        <span className='vc__count'>x{vacancyCount}</span>
        <div className="vc__vacancy">{vacancyName.charAt(0).toUpperCase() + vacancyName.slice(1)}</div>
        <div className="vc__project">№{projectId} {projectName}</div>
        <div className="vc__stage">{projectStageStatus}</div>
        <div className="vc__links">
            <div className="vc__cab">
                <p>Открыть вакансию
            в кабинете МИЭМ</p>
                <a href={projectUrl} target='_blank' className='link'  onClick={(e) => e.stopPropagation()}>
                    <img src={link} alt="link"/>
                </a>
                <div className={isLiked ? 'heart active' : 'heart'} onClick={toggleIsLiked}>
                    {/* <img src={heart} alt="heart"/> */}
                    <svg width="24px" height="24px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M19.3 5.71002C18.841 5.24601 18.2943 4.87797 17.6917 4.62731C17.0891 4.37666 16.4426 4.2484 15.79 4.25002C15.1373 4.2484 14.4909 4.37666 13.8883 4.62731C13.2857 4.87797 12.739 5.24601 12.28 5.71002L12 6.00002L11.72 5.72001C10.7917 4.79182 9.53273 4.27037 8.22 4.27037C6.90726 4.27037 5.64829 4.79182 4.72 5.72001C3.80386 6.65466 3.29071 7.91125 3.29071 9.22002C3.29071 10.5288 3.80386 11.7854 4.72 12.72L11.49 19.51C11.6306 19.6505 11.8212 19.7294 12.02 19.7294C12.2187 19.7294 12.4094 19.6505 12.55 19.51L19.32 12.72C20.2365 11.7823 20.7479 10.5221 20.7442 9.21092C20.7405 7.89973 20.2218 6.64248 19.3 5.71002Z"/>
                    </svg>
                </div>
            </div>
            <div className="vc__more">
                <div className="vc__more-btn" onClick={() => setIsModal(!isModal)}>
                    Подробнее
                    <img className={isModal ? "active" : ""} src={arrow} alt="arrow" />
                </div>
            </div>
        </div>
    </div>
    {isModal && <div className="vc__modal">
        <div><span>Обязательно знать/уметь:</span>{vacancyDisciplines.length !== 0 ? vacancyDisciplines : 'Не указано'}</div>
        <div><span>Желательно знать/уметь:</span>{vacancyAdditionally.length !== 0 ? vacancyAdditionally : 'Не указано'}</div>
        <div><span>Руководитель проекта:</span>{projectHead.full_name}, <a target="_blanc" href={`mailto:${projectHead.email}`}>{projectHead.email}</a></div>
        {projectType == "soft" ? <div><span>Тип проекта:</span>Программный</div> : null}
        {projectType == "soft-hard" ? <div><span>Тип проекта:</span>Программно-аппаратный</div> : null}
        {projectType == "nir" ? <div><span>Тип проекта:</span>Научно-исследовательская работа</div> : null}
        {projectType == "educat" ? <div><span>Тип проекта:</span>Учебно-методический</div> : null}
    </div>}
    </>
  )
}

export default VacancyCard;