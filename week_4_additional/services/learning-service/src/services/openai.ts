import OpenAI from 'openai';
import { logger } from '../utils/logger';

export class OpenAIClient {
  private client: OpenAI;

  constructor(config: {
    apiKey: string;
    organizationId: string;
  }) {
    this.client = new OpenAI({
      apiKey: config.apiKey,
      organization: config.organizationId,
    });
  }

  async analyzeText(text: string) {
    try {
      const completion = await this.client.chat.completions.create({
        model: "gpt-4",
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
        temperature: 0.7,
      });

      return completion.choices[0].message.content;
    } catch (error) {
      logger.error('Error analyzing text:', error);
      throw error;
    }
  }

  async generateExampleSentences(word: string) {
    try {
      const completion = await this.client.chat.completions.create({
        model: "gpt-4",
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
        temperature: 0.7,
      });

      return completion.choices[0].message.content;
    } catch (error) {
      logger.error('Error generating example sentences:', error);
      throw error;
    }
  }
}
