const dev = {
    API_URL: "http://10.193.61.65:8000"
};
  
const prod = {
  API_URL: "https://90.156.219.15:8000"
};
  
const config = process.env.REACT_APP_STAGE === 'production' ? prod : dev;

export default config;