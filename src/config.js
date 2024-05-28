const dev = {
    API_URL: "https://api.miem-vacancy.ru"
};
  
const prod = {
  API_URL: "https://api.miem-vacancy.ru"
};
  
const config = process.env.REACT_APP_STAGE === 'production' ? prod : dev;

export default config;