import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

const initialState = {
  skills: [],
  professions: [],
};

export const fetchProfessions = createAsyncThunk(
  'searchParams/fetchProfessions',
  async () => {
    const response = await fetch('http://10.193.60.137:8000/api/search/?q=');
    const professions = await response.json();
    return professions;
  }
);

export const fetchSkills = createAsyncThunk(
  'searchParams/fetchSkills',
  async () => {
    const response = await fetch('http://10.193.60.137:8000/api/search/?q=');
    const skills = await response.json();
    return skills;
  }
);

const searchParamsSlice = createSlice({
  name: 'searchParams',
  initialState,
  reducers: {
    addSkill: (state, action) => {
      state.skills.push({ name: action.payload.name, isSelected: false, id: action.payload.id });
    },
    addProfession: (state, action) => {
      state.professions.push({ name: action.payload.name, isSelected: false, id: action.payload.id });
    },
    removeSkill: (state, action) => {
      state.skills = state.skills.filter(skill => skill.id !== action.payload);
    },
    removeProfession: (state, action) => {
      state.professions = state.professions.filter(profession => profession.id !== action.payload);
    },
    toggleSkillSelection: (state, action) => {
      const skillIndex = state.skills.findIndex(skill => skill.id === action.payload);
      if (skillIndex !== -1) {
        state.skills[skillIndex].isSelected = !state.skills[skillIndex].isSelected;
      }
    },
    toggleProfessionSelection: (state, action) => {
      const professionIndex = state.professions.findIndex(profession => profession.id === action.payload);
      if (professionIndex !== -1) {
        state.professions[professionIndex].isSelected = !state.professions[professionIndex].isSelected;
      }
    },
    clearSearchParams: (state) => {
      state.skills = [];
      state.professions = [];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchProfessions.fulfilled, (state, action) => {
        state.professions = action.payload.map(profession => ({
          name: profession.name.charAt(0).toUpperCase() + profession.name.slice(1),
          id: profession.id,
          isSelected: false
        }));
      })
      .addCase(fetchSkills.fulfilled, (state, action) => {
        state.skills = action.payload.map(skill => ({
          name: skill.name.charAt(0).toUpperCase() + skill.name.slice(1),
          id: skill.id,
          isSelected: false
        }));
      });
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
