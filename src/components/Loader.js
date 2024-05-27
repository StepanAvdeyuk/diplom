import React from "react"
import ContentLoader from "react-content-loader"
import { useIsMobile } from "../hooks/useIsMobile"



const Loader = (props) => {

  const isMobile = useIsMobile();

  return (
    <ContentLoader 
    speed={2}
    width={'100%'}
    height={isMobile ? 200 : 110}
    viewBox={isMobile ? "0 0 350 200":"0 0 885 110"}
    backgroundColor="#ebf1f4"
    foregroundColor="#d8e0e9"
    {...props}
    >
    <rect x="0" y="10" rx="10" ry="10" width="100%" height={isMobile ? 190 : 95} />
  </ContentLoader>
)
}

export default Loader;