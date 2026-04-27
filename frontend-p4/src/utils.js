export function resolveMediaUrl(path) {
  if (!path) return ''
  let sanitized = path

  if (sanitized.startsWith('http')) {
    try {
      const url = new URL(sanitized)
      sanitized = url.pathname
    } catch (e) { }
  }

  if (sanitized.includes('/media/media/')) {
    sanitized = sanitized.replace('/media/media/', '/media/')
  }

  const base = import.meta.env.VITE_API_BASE_URL || ''
  return `${base}${sanitized}`
}
