type Primitive = string | number | boolean | null

type SchemaNode =
  | { type: 'object'; properties: Record<string, SchemaNode> }
  | { type: 'array'; items: SchemaNode }
  | { type: 'string' | 'number' | 'boolean' | 'null' }
  | Primitive

export function parseResponseFormatSafely(input: unknown): SchemaNode | null {
  if (!input) {
    return null
  }

  if (typeof input === 'object') {
    return input as SchemaNode
  }

  if (typeof input !== 'string') {
    return null
  }

  try {
    return JSON.parse(input) as SchemaNode
  } catch {
    return null
  }
}

export function extractFieldsFromSchema(schema: SchemaNode, basePath = ''): string[] {
  if (!schema) {
    return []
  }

  if (typeof schema !== 'object' || Array.isArray(schema)) {
    return basePath ? [basePath] : []
  }

  if ('properties' in schema && schema.properties) {
    return Object.entries(schema.properties).flatMap(([key, child]) =>
      extractFieldsFromSchema(child, basePath ? `${basePath}.${key}` : key)
    )
  }

  if ('items' in schema && schema.items) {
    const arrayPath = basePath ? `${basePath}[]` : '[]'
    return [arrayPath, ...extractFieldsFromSchema(schema.items, arrayPath)]
  }

  if ('type' in schema) {
    return basePath ? [basePath] : ['']
  }

  return []
}
