import React from "react"
import ContentLoader from "react-content-loader"

const Loader = (props) => (
    <ContentLoader 
    speed={2}
    width={'100%'}
    height={110}
    viewBox="0 0 885 110"
    backgroundColor="#ebf1f4"
    foregroundColor="#d8e0e9"
    {...props}
    >
    <rect x="0" y="10" rx="10" ry="10" width="100%" height="95" />
  </ContentLoader>
)

export default Loader;