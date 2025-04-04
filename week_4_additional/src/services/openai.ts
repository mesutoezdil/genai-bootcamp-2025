import OpenAI from 'openai';
import { config } from '../config';

export class OpenAIService {
  private client: OpenAI;

  constructor(apiKey: string) {
    this.client = new OpenAI({ apiKey });
  }

  async analyzeText(text: string) {
    try {
      const completion = await this.client.chat.completions.create({
        model: config.openai.model,
        messages: [
          {
            role: "system",
            content: "You are a Chinese language learning assistant. Analyze the given text and provide learning insights."
          },
          {
            role: "user",
            content: text
          }
        ],
        temperature: config.openai.temperature,
      });

      return completion.choices[0].message.content;
    } catch (error) {
      console.error('Error analyzing text:', error);
      throw error;
    }
  }

  async generateExampleSentences(word: string) {
    try {
      const completion = await this.client.chat.completions.create({
        model: config.openai.model,
        messages: [
          {
            role: "system",
            content: "You are a Chinese language learning assistant. Generate 5 example sentences using the given word in different contexts."
          },
          {
            role: "user",
            content: `Word: ${word}`
          }
        ],
        temperature: config.openai.temperature,
      });

      return completion.choices[0].message.content;
    } catch (error) {
      console.error('Error generating example sentences:', error);
      throw error;
    }
  }
}
