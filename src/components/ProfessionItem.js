import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toggleProfessionSelection } from '../redux/reducers/searchParamsSlice';

const ProfessionItem = ({ id, name }) => {
  const dispatch = useDispatch();

  const isSelected = useSelector(state =>
    state.searchParams.professions.find(profession => profession.id === id)?.isSelected || false
  );

  const handleCheckboxChange = () => {
    dispatch(toggleProfessionSelection(id));
  };

  return (
    <label className="checkbox">
      <input type='checkbox' name='checkbox' checked={isSelected} onChange={handleCheckboxChange}/>
      <div>{name}</div>
      <span></span>
    </label>
  );
};

export default ProfessionItem;