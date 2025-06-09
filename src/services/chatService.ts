import { ChatMessage, ChatResponse } from '../types/chat';
import { SYSTEM_PROMPT } from '../constants/prompts';

const API_URL = 'http://localhost:11434/api/generate';

// Store conversation history
let conversationHistory: ChatMessage[] = [];

export const sendMessage = async (message: string): Promise<ChatResponse> => {
  // Add user message to history
  const userMessage = createUserMessage(message);
  conversationHistory.push(userMessage);

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