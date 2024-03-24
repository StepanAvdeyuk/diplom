import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { toggleSkillSelection } from '../redux/reducers/searchParamsSlice';

const SkillItem = ({ name }) => {
  const dispatch = useDispatch();

  const isSelected = useSelector(state =>
    state.searchParams.skills.find(skill => skill.name === name)?.isSelected || false
  );

  const handleCheckboxChange = () => {
    dispatch(toggleSkillSelection(name));
  };

  return (
    <label className="checkbox">
      <input type='checkbox' name='checkbox' checked={isSelected} onChange={handleCheckboxChange} />
      {name}
      <span></span>
    </label>
  );
};

export default SkillItem;