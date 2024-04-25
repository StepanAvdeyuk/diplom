import { useState, useEffect, useCallback } from 'react';
import debounce from 'lodash.debounce';
import axios from 'axios';

export const useDebouncedSearch = (url, delay) => {
  const [input, setInput] = useState('');
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchData = useCallback(async (searchTerm) => {
    setIsLoading(true);
    try {
      const response = await axios.get(`${url}?q=${encodeURIComponent(searchTerm)}`);
      const newData = response.data.map(item => ({
        id: item.id,
        name: item.annotation  
      }));
      setData(newData);
    } catch (error) {
        console.error('Ошибка загрузки:', error);
    } finally {
      setIsLoading(false);
    }
  }, [url]);

  const debouncedFetchData = useCallback(debounce(fetchData, delay), [fetchData, delay]);

  useEffect(() => {
    if (input) {
      debouncedFetchData(input);
    } else {
      setData([]); // Очистка данных, если строка поиска пуста
    }
    return () => debouncedFetchData.cancel();
  }, [input, debouncedFetchData]);

  return { input, setInput, data, isLoading };
};
