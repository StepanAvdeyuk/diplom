const dev = {
    API_URL: "http://10.193.62.131:8000"
  };
  
  const prod = {
    API_URL: "https://myproductiondomain.com/api"
  };
  
  const config = process.env.REACT_APP_STAGE === 'production' ? prod : dev;
  
  export default config;