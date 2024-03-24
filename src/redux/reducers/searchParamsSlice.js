import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  skills: [{name: 'Frontend-разработка', isSelected: false}, {name: 'Backend-разработка', isSelected: false}, {name: 'Маркетинг', isSelected: false}, {name: 'Дизайн', isSelected: false}, {name: 'Тестировка', isSelected: false}, {name: '3д моделирование', isSelected: false}],
  professions: [{name: 'Frontend-разработка', isSelected: false}, {name: 'Backend-разработка', isSelected: false}, {name: 'Маркетинг', isSelected: false}, {name: 'Дизайн', isSelected: false}, {name: 'Тестировка', isSelected: false}, {name: '3д моделирование', isSelected: false}],
};

const searchParamsSlice = createSlice({
  name: 'searchParams',
  initialState,
  reducers: {
    addSkill: (state, action) => {
      state.skills.push({ name: action.payload, isSelected: false });
    },
    addProfession: (state, action) => {
      state.professions.push({ name: action.payload, isSelected: false });
    },
    removeSkill: (state, action) => {
      state.skills = state.skills.filter(skill => skill.name !== action.payload);
    },
    removeProfession: (state, action) => {
      state.professions = state.professions.filter(profession => profession.name !== action.payload);
    },
    toggleSkillSelection: (state, action) => {
      const skillIndex = state.skills.findIndex(skill => skill.name === action.payload);
      if (skillIndex !== -1) {
        state.skills[skillIndex].isSelected = !state.skills[skillIndex].isSelected;
      }
    },
    toggleProfessionSelection: (state, action) => {
      const professionIndex = state.professions.findIndex(profession => profession.name === action.payload);
      if (professionIndex !== -1) {
        state.professions[professionIndex].isSelected = !state.professions[professionIndex].isSelected;
      }
    },
    clearSearchParams: (state) => {
      state.skills = [];
      state.professions = [];
    },
  },
});

export const {
  addSkill,
  addProfession,
  removeSkill,
  removeProfession,
  toggleSkillSelection,
  toggleProfessionSelection,
  clearSearchParams,
} = searchParamsSlice.actions;

export default searchParamsSlice.reducer;
