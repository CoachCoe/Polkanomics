from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferMemory
from config import settings

class EconomicsChatbot:
    def __init__(self):
        # Load the fine-tuned model and tokenizer
        model_path = "./fine_tuned_model"
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto"
        )
        
        # Create the pipeline
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=512,
            temperature=0.7,
            top_p=0.95,
            repetition_penalty=1.15
        )
        
        # Create the LangChain pipeline
        self.llm = HuggingFacePipeline(pipeline=pipe)
        self.memory = ConversationBufferMemory()
        
        # System prompt for economics focus
        self.system_prompt = """You are an expert economics chatbot with specialized knowledge in tokenomics and blockchain economics, particularly focused on Polkadot's token economics. You are powered by a fine-tuned Phi-2 model. You provide clear, accurate, and detailed explanations about economic concepts, token mechanics, and blockchain economics. Always maintain a professional and educational tone while making complex economic concepts accessible."""
    
    def get_response(self, user_input: str) -> str:
        # Get conversation history
        history = self.memory.load_memory_variables({})
        
        # Prepare messages
        messages = [
            SystemMessage(content=self.system_prompt),
            *[HumanMessage(content=msg) for msg in history.get("history", [])],
            HumanMessage(content=user_input)
        ]
        
        # Get response from model
        response = self.llm.predict_messages(messages)
        
        # Update memory
        self.memory.save_context({"input": user_input}, {"output": response.content})
        
        return response.content

# Example usage
if __name__ == "__main__":
    chatbot = EconomicsChatbot()
    response = chatbot.get_response("Explain the tokenomics of Polkadot's DOT token.")
    print(response) 