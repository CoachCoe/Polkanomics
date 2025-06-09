import { ChatMessage, ChatResponse } from '../types/chat';
import { SYSTEM_PROMPT } from '../constants/prompts';

const API_URL = 'http://localhost:11434/api/generate';
const MAX_HISTORY_LENGTH = 20; // Keep last 20 messages for context

// Store conversation history
let conversationHistory: ChatMessage[] = [];

export const sendMessage = async (message: string): Promise<ChatResponse> => {
  // Add user message to history
  const userMessage = createUserMessage(message);
  conversationHistory.push(userMessage);

  // Trim history if it exceeds max length
  if (conversationHistory.length > MAX_HISTORY_LENGTH) {
    conversationHistory = conversationHistory.slice(-MAX_HISTORY_LENGTH);
  }

  // Prepare the full prompt with system message and conversation history
  const fullPrompt = [
    SYSTEM_PROMPT,
    ...conversationHistory.map(msg => `${msg.role}: ${msg.content}`),
    `user: ${message}`,
  ].join('\n\n');

  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'mistral',
      prompt: fullPrompt,
      stream: false,
      options: {
        temperature: 0.7,
        top_p: 0.95,
        top_k: 40,
        num_ctx: 4096, // Increased context window
        repeat_penalty: 1.1,
        stop: ['user:', 'assistant:'], // Stop tokens to prevent model from continuing the conversation
      },
    }),
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  const data = await response.json();
  
  // Add assistant response to history
  const assistantMessage = createAssistantMessage(data.response);
  conversationHistory.push(assistantMessage);

  return data;
};

export const createUserMessage = (content: string): ChatMessage => ({
  role: 'user',
  content,
  timestamp: new Date(),
});

export const createAssistantMessage = (content: string): ChatMessage => ({
  role: 'assistant',
  content,
  timestamp: new Date(),
});

export const createErrorMessage = (): ChatMessage => ({
  role: 'assistant',
  content: 'Sorry, I encountered an error. Please try again.',
  timestamp: new Date(),
});

export const clearConversationHistory = () => {
  conversationHistory = [];
};

export const getConversationHistory = (): ChatMessage[] => {
  return [...conversationHistory];
}; 