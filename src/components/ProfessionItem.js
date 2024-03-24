import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toggleProfessionSelection } from '../redux/reducers/searchParamsSlice';

const ProfessionItem = ({ name }) => {
  const dispatch = useDispatch();

  const isSelected = useSelector(state =>
    state.searchParams.professions.find(profession => profession.name === name)?.isSelected || false
  );

  const handleCheckboxChange = () => {
    dispatch(toggleProfessionSelection(name));
  };

  return (
    <label className="checkbox">
      <input type='checkbox' name='checkbox' checked={isSelected} onChange={handleCheckboxChange} />
      {name}
      <span></span>
    </label>
  );
};

export default ProfessionItem;