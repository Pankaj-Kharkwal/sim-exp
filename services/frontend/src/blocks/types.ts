// Placeholder for Sub-Block types, based on errors and common usage.

export type SubBlockType =
  | 'short-input'
  | 'long-input'
  | 'number-input'
  | 'boolean-input'
  | 'select-input'
  | 'code-input'
  | 'credential-input'
  | 'file-input'
  | 'json-input';

// Placeholder for SubBlockConfig
export type SubBlockConfig = Record<string, any>;

// Placeholder for BlockOutput
export type BlockOutput = any;