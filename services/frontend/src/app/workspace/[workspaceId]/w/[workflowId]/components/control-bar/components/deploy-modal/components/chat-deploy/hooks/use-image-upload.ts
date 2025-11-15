import type React from 'react'
import { useCallback, useRef, useState } from 'react'

interface UseImageUploadOptions {
  onUpload?: (url: string | null) => void
  onError?: (message: string) => void
  uploadToServer?: boolean
}

export function useImageUpload({ onUpload, onError }: UseImageUploadOptions) {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string | null>(null)
  const [isUploading, setIsUploading] = useState(false)

  const revokePreview = () => {
    if (previewUrl?.startsWith('blob:')) {
      URL.revokeObjectURL(previewUrl)
    }
  }

  const handleFileChange = useCallback(
    async (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0]
      if (!file) return

      setIsUploading(true)
      revokePreview()

      try {
        const objectUrl = URL.createObjectURL(file)
        setPreviewUrl(objectUrl)
        setFileName(file.name)
        onUpload?.(objectUrl)
      } catch (error) {
        onError?.(error instanceof Error ? error.message : 'Unable to load image')
        onUpload?.(null)
      } finally {
        setIsUploading(false)
      }
    },
    [onUpload, onError, previewUrl]
  )

  const handleThumbnailClick = () => {
    fileInputRef.current?.click()
  }

  const handleRemove = useCallback(() => {
    revokePreview()
    setPreviewUrl(null)
    setFileName(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
    onUpload?.(null)
  }, [onUpload, previewUrl])

  return {
    previewUrl,
    fileName,
    fileInputRef,
    handleThumbnailClick,
    handleFileChange,
    handleRemove,
    isUploading,
  }
}
