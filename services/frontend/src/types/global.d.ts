declare module 'next/image' {
  import * as React from 'react'
  export interface ImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
    fill?: boolean
    quality?: number
    sizes?: string
    priority?: boolean
  }
  const Image: React.FC<ImageProps>
  export default Image
}
