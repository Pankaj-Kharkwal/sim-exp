import {
  getBlockDefinition,
  type BlockDefinition,
} from '@/lib/blocks/blockDefinitions'

export interface ParameterCompletion {
  totalParameters: number
  requiredTotal: number
  requiredComplete: number
}

export const isParameterValueSet = (value: any): boolean => {
  if (value === null || value === undefined) return false
  if (typeof value === 'string') return value.trim().length > 0
  if (Array.isArray(value)) return value.length > 0
  if (typeof value === 'object') return Object.keys(value).length > 0
  return true
}

export const getParameterCompletion = (
  type: string,
  config?: Record<string, any>
): { definition?: BlockDefinition } & ParameterCompletion => {
  const definition = getBlockDefinition(type)
  if (!definition) {
    return {
      definition: undefined,
      totalParameters: 0,
      requiredTotal: 0,
      requiredComplete: 0,
    }
  }

  const requiredParameters = definition.parameters.filter((param) => param.required)
  const requiredComplete = requiredParameters.filter((param) =>
    isParameterValueSet(config?.[param.name])
  ).length

  return {
    definition,
    totalParameters: definition.parameters.length,
    requiredTotal: requiredParameters.length,
    requiredComplete,
  }
}

export const buildDefaultConfig = (
  definition: BlockDefinition
): Record<string, any> => {
  return definition.parameters.reduce<Record<string, any>>((acc, param) => {
    if (param.default !== undefined) {
      acc[param.name] = param.default
    }
    return acc
  }, {})
}
