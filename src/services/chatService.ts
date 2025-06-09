import { ChatMessage, ChatResponse } from '../types/chat';

const API_URL = 'http://localhost:11434/api/generate';

export const sendMessage = async (message: string): Promise<ChatResponse> => {
  const response = await fetch(API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'mistral',
      prompt: message,
      stream: false,
    }),
  });

  if (!response.ok) {
    throw new Error('Network response was not ok');
  }

  return response.json();
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