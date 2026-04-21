export function resolveMediaUrl(path) {
  if (!path) return ''
  let sanitized = path
  
  // If the path comes back from Render with an absolute URL, strip it so the Vite proxy handles it
  if (sanitized.startsWith('http')) {
    try {
      const url = new URL(sanitized)
      sanitized = url.pathname
    } catch(e) {}
  }
  
  // Fix double /media/ path from neon database due to upload_to='media/'
  if (sanitized.includes('/media/media/')) {
    sanitized = sanitized.replace('/media/media/', '/media/')
  }

  // Use base URL from env if available, otherwise relative for proxy
  const base = import.meta.env.VITE_API_BASE_URL || ''
  return `${base}${sanitized}`
}
