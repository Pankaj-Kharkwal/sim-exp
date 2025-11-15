import { BaseClientTool } from '../base-tool'

export class GetExamplesRagClientTool extends BaseClientTool {
  constructor() {
    super('get-examples-rag', 'Get examples using RAG')
  }
}
