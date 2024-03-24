import { configureStore } from '@reduxjs/toolkit';
import searchParamsReducer from './reducers/searchParamsSlice';

export default configureStore({
  reducer: {
    searchParams: searchParamsReducer,
  },
});