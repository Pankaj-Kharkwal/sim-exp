import {
  Code,
  Zap,
  Database,
  Mail,
  MessageSquare,
  FileText,
  Globe,
  Calendar,
  Clock,
  GitBranch,
  Repeat,
  Filter,
  Settings,
  Search,
  Send,
  Download,
  Upload,
  Image,
  Video,
  Music,
  File,
  Folder,
  Cloud,
  Server,
  Lock,
  Unlock,
  Key,
  User,
  Users,
  Bell,
  Smartphone,
  Laptop,
  Monitor,
  Printer,
  Camera,
  Mic,
  Speaker,
  Play,
  Pause,
  SkipForward,
  SkipBack,
  Volume2,
  VolumeX,
  Wifi,
  WifiOff,
  Bluetooth,
  Cast,
  Wrench,
  Package,
  Terminal,
  type LucideIcon,
} from 'lucide-react'

export interface BlockParameter {
  name: string
  type: 'string' | 'number' | 'boolean' | 'json' | 'array' | 'select'
  required?: boolean
  default?: any
  description?: string
  options?: Array<{ label: string; value: string }>
}

export interface BlockDefinition {
  type: string
  name: string
  description: string
  category: 'logic' | 'data' | 'ai' | 'integration' | 'automation' | 'triggers' | 'tools'
  icon: LucideIcon
  color: string
  parameters: BlockParameter[]
  outputs: string[]
}

export const blockCategories = {
  logic: { label: 'Logic & Control', icon: GitBranch },
  data: { label: 'Data & Storage', icon: Database },
  ai: { label: 'AI & ML', icon: Zap },
  integration: { label: 'Integrations', icon: Globe },
  automation: { label: 'Automation', icon: Settings },
  triggers: { label: 'Triggers', icon: Play },
  tools: { label: 'Tools & MCP', icon: Wrench },
}

export const blockDefinitions: BlockDefinition[] = [
  // Logic & Control
  {
    type: 'function',
    name: 'Function',
    description: 'Execute custom JavaScript/TypeScript code',
    category: 'logic',
    icon: Code,
    color: 'purple',
    parameters: [
      {
        name: 'code',
        type: 'string',
        required: true,
        description: 'Function code to execute',
      },
      {
        name: 'timeout',
        type: 'number',
        default: 30,
        description: 'Execution timeout in seconds',
      },
    ],
    outputs: ['result', 'error'],
  },
  {
    type: 'condition',
    name: 'Condition',
    description: 'Branch workflow based on conditions',
    category: 'logic',
    icon: GitBranch,
    color: 'blue',
    parameters: [
      {
        name: 'condition',
        type: 'string',
        required: true,
        description: 'Condition expression to evaluate',
      },
    ],
    outputs: ['true', 'false'],
  },
  {
    type: 'loop',
    name: 'Loop',
    description: 'Iterate over items or repeat actions',
    category: 'logic',
    icon: Repeat,
    color: 'indigo',
    parameters: [
      {
        name: 'items',
        type: 'array',
        required: true,
        description: 'Array to iterate over',
      },
      {
        name: 'maxIterations',
        type: 'number',
        default: 1000,
        description: 'Maximum iterations allowed',
      },
    ],
    outputs: ['item', 'index', 'results'],
  },
  {
    type: 'filter',
    name: 'Filter',
    description: 'Filter data based on criteria',
    category: 'logic',
    icon: Filter,
    color: 'cyan',
    parameters: [
      {
        name: 'data',
        type: 'array',
        required: true,
        description: 'Data to filter',
      },
      {
        name: 'condition',
        type: 'string',
        required: true,
        description: 'Filter condition',
      },
    ],
    outputs: ['filtered', 'count'],
  },

  // Data & Storage
  {
    type: 'database',
    name: 'Database Query',
    description: 'Query SQL or NoSQL databases',
    category: 'data',
    icon: Database,
    color: 'green',
    parameters: [
      {
        name: 'connection',
        type: 'string',
        required: true,
        description: 'Database connection string',
      },
      {
        name: 'query',
        type: 'string',
        required: true,
        description: 'SQL query to execute',
      },
      {
        name: 'timeout',
        type: 'number',
        default: 30,
        description: 'Query timeout in seconds',
      },
    ],
    outputs: ['rows', 'count', 'error'],
  },
  {
    type: 'file',
    name: 'File Operations',
    description: 'Read, write, or process files',
    category: 'data',
    icon: FileText,
    color: 'gray',
    parameters: [
      {
        name: 'operation',
        type: 'select',
        required: true,
        options: [
          { label: 'Read', value: 'read' },
          { label: 'Write', value: 'write' },
          { label: 'Delete', value: 'delete' },
          { label: 'List', value: 'list' },
        ],
        description: 'File operation to perform',
      },
      {
        name: 'path',
        type: 'string',
        required: true,
        description: 'File path',
      },
    ],
    outputs: ['content', 'success', 'error'],
  },
  {
    type: 'storage',
    name: 'Cloud Storage',
    description: 'Interact with cloud storage (S3, GCS, Azure)',
    category: 'data',
    icon: Cloud,
    color: 'sky',
    parameters: [
      {
        name: 'provider',
        type: 'select',
        required: true,
        options: [
          { label: 'AWS S3', value: 's3' },
          { label: 'Google Cloud Storage', value: 'gcs' },
          { label: 'Azure Blob', value: 'azure' },
        ],
        description: 'Storage provider',
      },
      {
        name: 'bucket',
        type: 'string',
        required: true,
        description: 'Bucket/container name',
      },
      {
        name: 'key',
        type: 'string',
        required: true,
        description: 'Object key/path',
      },
    ],
    outputs: ['url', 'success', 'error'],
  },

  // AI & ML
  {
    type: 'llm',
    name: 'LLM Chat',
    description: 'Generate responses using large language models',
    category: 'ai',
    icon: MessageSquare,
    color: 'pink',
    parameters: [
      {
        name: 'model',
        type: 'select',
        required: true,
        options: [
          { label: 'GPT-4', value: 'gpt-4' },
          { label: 'GPT-3.5', value: 'gpt-3.5-turbo' },
          { label: 'Claude 3', value: 'claude-3' },
          { label: 'Gemini', value: 'gemini' },
        ],
        description: 'LLM model to use',
      },
      {
        name: 'prompt',
        type: 'string',
        required: true,
        description: 'Prompt for the model',
      },
      {
        name: 'temperature',
        type: 'number',
        default: 0.7,
        description: 'Temperature (0-1)',
      },
      {
        name: 'maxTokens',
        type: 'number',
        default: 1000,
        description: 'Maximum tokens to generate',
      },
    ],
    outputs: ['response', 'tokens', 'error'],
  },
  {
    type: 'embedding',
    name: 'Generate Embeddings',
    description: 'Convert text to vector embeddings',
    category: 'ai',
    icon: Zap,
    color: 'amber',
    parameters: [
      {
        name: 'text',
        type: 'string',
        required: true,
        description: 'Text to embed',
      },
      {
        name: 'model',
        type: 'select',
        required: true,
        options: [
          { label: 'OpenAI Ada', value: 'text-embedding-ada-002' },
          { label: 'Cohere', value: 'cohere' },
        ],
        description: 'Embedding model',
      },
    ],
    outputs: ['embedding', 'dimensions', 'error'],
  },
  {
    type: 'vision',
    name: 'Image Analysis',
    description: 'Analyze images with computer vision',
    category: 'ai',
    icon: Image,
    color: 'violet',
    parameters: [
      {
        name: 'image',
        type: 'string',
        required: true,
        description: 'Image URL or base64',
      },
      {
        name: 'task',
        type: 'select',
        required: true,
        options: [
          { label: 'Caption', value: 'caption' },
          { label: 'Object Detection', value: 'detect' },
          { label: 'OCR', value: 'ocr' },
        ],
        description: 'Vision task',
      },
    ],
    outputs: ['result', 'confidence', 'error'],
  },

  // Integrations
  {
    type: 'api',
    name: 'HTTP Request',
    description: 'Make HTTP/REST API calls',
    category: 'integration',
    icon: Globe,
    color: 'blue',
    parameters: [
      {
        name: 'method',
        type: 'select',
        required: true,
        options: [
          { label: 'GET', value: 'GET' },
          { label: 'POST', value: 'POST' },
          { label: 'PUT', value: 'PUT' },
          { label: 'DELETE', value: 'DELETE' },
          { label: 'PATCH', value: 'PATCH' },
        ],
        description: 'HTTP method',
      },
      {
        name: 'url',
        type: 'string',
        required: true,
        description: 'API endpoint URL',
      },
      {
        name: 'headers',
        type: 'json',
        description: 'Request headers',
      },
      {
        name: 'body',
        type: 'json',
        description: 'Request body',
      },
    ],
    outputs: ['response', 'status', 'error'],
  },
  {
    type: 'email',
    name: 'Send Email',
    description: 'Send emails via SMTP or email services',
    category: 'integration',
    icon: Mail,
    color: 'orange',
    parameters: [
      {
        name: 'to',
        type: 'string',
        required: true,
        description: 'Recipient email',
      },
      {
        name: 'subject',
        type: 'string',
        required: true,
        description: 'Email subject',
      },
      {
        name: 'body',
        type: 'string',
        required: true,
        description: 'Email body',
      },
      {
        name: 'html',
        type: 'boolean',
        default: false,
        description: 'Send as HTML',
      },
    ],
    outputs: ['messageId', 'success', 'error'],
  },
  {
    type: 'webhook',
    name: 'Webhook',
    description: 'Receive webhook events',
    category: 'integration',
    icon: Server,
    color: 'teal',
    parameters: [
      {
        name: 'path',
        type: 'string',
        required: true,
        description: 'Webhook path',
      },
      {
        name: 'method',
        type: 'select',
        options: [
          { label: 'POST', value: 'POST' },
          { label: 'GET', value: 'GET' },
          { label: 'PUT', value: 'PUT' },
        ],
        description: 'HTTP method',
      },
    ],
    outputs: ['payload', 'headers', 'query'],
  },
  {
    type: 'slack',
    name: 'Slack',
    description: 'Send messages to Slack',
    category: 'integration',
    icon: MessageSquare,
    color: 'purple',
    parameters: [
      {
        name: 'channel',
        type: 'string',
        required: true,
        description: 'Slack channel ID',
      },
      {
        name: 'message',
        type: 'string',
        required: true,
        description: 'Message text',
      },
    ],
    outputs: ['timestamp', 'success', 'error'],
  },

  // Automation
  {
    type: 'wait',
    name: 'Wait/Delay',
    description: 'Pause workflow execution',
    category: 'automation',
    icon: Clock,
    color: 'yellow',
    parameters: [
      {
        name: 'duration',
        type: 'number',
        required: true,
        description: 'Wait duration in seconds',
      },
    ],
    outputs: ['completed'],
  },
  {
    type: 'schedule',
    name: 'Schedule',
    description: 'Run workflow on a schedule',
    category: 'automation',
    icon: Calendar,
    color: 'red',
    parameters: [
      {
        name: 'cron',
        type: 'string',
        required: true,
        description: 'Cron expression',
      },
      {
        name: 'timezone',
        type: 'string',
        default: 'UTC',
        description: 'Timezone',
      },
    ],
    outputs: ['timestamp'],
  },
  {
    type: 'transform',
    name: 'Transform Data',
    description: 'Map, filter, or transform data',
    category: 'automation',
    icon: Settings,
    color: 'slate',
    parameters: [
      {
        name: 'input',
        type: 'json',
        required: true,
        description: 'Input data',
      },
      {
        name: 'transformation',
        type: 'string',
        required: true,
        description: 'Transformation logic',
      },
    ],
    outputs: ['output', 'error'],
  },

  // Triggers
  {
    type: 'manual_trigger',
    name: 'Manual Trigger',
    description: 'Start workflow manually',
    category: 'triggers',
    icon: Play,
    color: 'green',
    parameters: [],
    outputs: ['timestamp'],
  },
  {
    type: 'api_trigger',
    name: 'API Trigger',
    description: 'Start workflow via API call',
    category: 'triggers',
    icon: Zap,
    color: 'blue',
    parameters: [
      {
        name: 'endpoint',
        type: 'string',
        required: true,
        description: 'API endpoint path',
      },
    ],
    outputs: ['payload', 'headers'],
  },
  {
    type: 'schedule_trigger',
    name: 'Schedule Trigger',
    description: 'Start workflow on schedule',
    category: 'triggers',
    icon: Calendar,
    color: 'purple',
    parameters: [
      {
        name: 'cron',
        type: 'string',
        required: true,
        description: 'Cron expression',
      },
    ],
    outputs: ['timestamp'],
  },

  // Tools & MCP
  {
    type: 'mcp_tool',
    name: 'MCP Tool',
    description: 'Execute tools from MCP (Model Context Protocol) servers',
    category: 'tools',
    icon: Wrench,
    color: 'indigo',
    parameters: [
      {
        name: 'server_id',
        type: 'string',
        required: true,
        description: 'MCP server ID',
      },
      {
        name: 'tool_name',
        type: 'string',
        required: true,
        description: 'Tool name to execute',
      },
      {
        name: 'arguments',
        type: 'json',
        description: 'Tool arguments (JSON)',
      },
    ],
    outputs: ['result', 'error'],
  },
  {
    type: 'custom_tool',
    name: 'Custom Tool',
    description: 'Execute custom JavaScript tools',
    category: 'tools',
    icon: Terminal,
    color: 'cyan',
    parameters: [
      {
        name: 'name',
        type: 'string',
        required: true,
        description: 'Tool name',
      },
      {
        name: 'code',
        type: 'string',
        required: true,
        description: 'Tool implementation (JavaScript)',
      },
      {
        name: 'arguments',
        type: 'json',
        description: 'Tool arguments',
      },
    ],
    outputs: ['result', 'error'],
  },
  {
    type: 'tool_registry',
    name: 'Tool Registry',
    description: 'Manage and discover available tools',
    category: 'tools',
    icon: Package,
    color: 'violet',
    parameters: [
      {
        name: 'action',
        type: 'select',
        required: true,
        options: [
          { label: 'List Tools', value: 'list' },
          { label: 'Get Tool Info', value: 'info' },
          { label: 'Test Tool', value: 'test' },
        ],
        description: 'Registry action',
      },
      {
        name: 'server_id',
        type: 'string',
        description: 'MCP server ID (for list/info)',
      },
      {
        name: 'tool_name',
        type: 'string',
        description: 'Tool name (for info/test)',
      },
    ],
    outputs: ['tools', 'info', 'result'],
  },
]

export const getBlockDefinition = (type: string): BlockDefinition | undefined => {
  return blockDefinitions.find((def) => def.type === type)
}

export const getBlocksByCategory = (category: string): BlockDefinition[] => {
  return blockDefinitions.filter((def) => def.category === category)
}

export const searchBlocks = (query: string): BlockDefinition[] => {
  const lowerQuery = query.toLowerCase()
  return blockDefinitions.filter(
    (def) =>
      def.name.toLowerCase().includes(lowerQuery) ||
      def.description.toLowerCase().includes(lowerQuery) ||
      def.type.toLowerCase().includes(lowerQuery)
  )
}
