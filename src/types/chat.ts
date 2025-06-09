export type MessageRole = 'user' | 'assistant';

export interface ChatMessage {
  role: MessageRole;
  content: string;
  timestamp: Date;
}

export interface ChatResponse {
  response: string;
  model: string;
}

export interface ChatError {
  message: string;
  code?: string;
} 