import React from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import config from '../../config'

const StatsPage = () => { 
    const [data, setData] = React.useState(null);
    const [isLoading, setIsLoading] = React.useState(false);
  
    const getData = () => {
      setIsLoading(true);
      axios.get(`${config.API_URL}/api/stats/`)
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

    // console.log(data)
  
    return (
          <>
          <div className="page__title">
            <Link to='/'>
              <svg width="8" height="14" viewBox="0 0 8 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M7 13L1 7L7 1" stroke="#072551" strokeOpacity="0.75" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </Link>
            <h2>Статистика по вакансиям</h2>
          </div>
  
          <div className="stats__content-wrapper">
             <div className="stats__total">Всего вакансий: {data && data.total_vacancies}</div>
             <div className="stats__content">
                <div className="stats__vacancy">
                    <div className="stats__content-name">Самые популярные вакансии</div>
                    {data && data.role_tags.slice(0, 10).map((item, i) => {
                        return <div className="stats__item">
                            <div className="stats__item-name">{item.role_name__annotation}</div>
                            <div className="stats__item-bar">
                                <div className="stats__item-bar-progress" style={{'width': `${(item.count/data.total_vacancies*100)+20}%`}}>
                                    {item.count}
                                </div>
                                {data.total_vacancies}
                            </div>
                        </div>
                    })}
                </div>
                <div className="stats__skills">
                    <div className="stats__content-name">Самые популярные навыки</div>
                    {data && data.skill_tags.slice(0, 10).map((item, i) => {
                        return <div className="stats__item">
                            <div className="stats__item-name">{item.skill_name__annotation}</div>
                            <div className="stats__item-bar">
                                <div className="stats__item-bar-progress" style={{'width': `${(item.count/data.total_vacancies*100)+20}%`}}>
                                    {item.count}
                                </div>
                                {data.total_vacancies}
                            </div>
                        </div>
                    })}
                </div>
             </div>
          </div>
          
          </>
    )
}

export default StatsPage;