import React from 'react'
import Slider from 'react-slick';
import { useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

import arrow2 from '../assets/main-arrow-2.svg';

function SampleNextArrow(props) {
    const { className, style, onClick } = props;
    return (
      <div
        className={className}
        style={{ ...style, display: "block", transform: "rotate(180deg) translateY(50%)"}}
        onClick={onClick}
      >
        <img src={arrow2} alt="arrow2" />
      </div>
    );
  }
  
function SamplePrevArrow(props) {
    const { className, style, onClick } = props;
    return (
        <div
          className={className}
          style={{ ...style, display: "block", transform: "translateY(-50%)"}}
          onClick={onClick}
        >
          <img src={arrow2} alt="arrow2" />
        </div>
      );
}

export default function SimpleSlider() {

    const catalogItems = useSelector(state => state.searchParams.catalogItems);

    var settings = {
      dots: false,
      arrows: true,
      infinite: true,
      speed: 500,
      slidesToShow: 3,
      slidesToScroll: 1,
      nextArrow: <SampleNextArrow/>,
      prevArrow: <SamplePrevArrow/>,
      responsive: [
        {
          breakpoint: 992,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 1,
          }
        },
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
          }
        },
      ]
    };
    return (
      <Slider {...settings}>
        {catalogItems && catalogItems.map(item => {
          return <Link to={`/catalog/${item.tag}`}>
              <div className='main__slider-item'>
            <span>Вакансии для {item.name}</span>
          </div>
          </Link>
        })}
      </Slider>
    );
  }