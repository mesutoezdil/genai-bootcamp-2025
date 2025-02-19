import chromadb
from chromadb.utils import embedding_functions
import json
import os
import boto3
from typing import Dict, List, Optional
from pypinyin import pinyin, Style

class BedrockEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model_id="amazon.titan-embed-text-v1"):
        """Initialize Bedrock embedding function"""
        self.bedrock_client = boto3.client('bedrock-runtime', region_name="us-east-1")
        self.model_id = model_id

    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Bedrock"""
        embeddings = []
        for text in texts:
            try:
                response = self.bedrock_client.invoke_model(
                    modelId=self.model_id,
                    body=json.dumps({
                        "inputText": text,
                        "inputType": "search_document"
                    })
                )
                response_body = json.loads(response['body'].read())
                embedding = response_body['embedding']
                embeddings.append(embedding)
            except Exception as e:
                print(f"生成嵌入时出错: {str(e)}")  # Error generating embedding
                embeddings.append([0.0] * 1536)
        return embeddings

class ChineseQuestionVectorStore:
    def __init__(self, persist_directory: str = "backend/data/vectorstore"):
        """Initialize the vector store for HSK listening questions"""
        self.persist_directory = persist_directory
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use Bedrock's Titan embedding model
        self.embedding_fn = BedrockEmbeddingFunction()
        
        # Create or get collections for each section type
        self.collections = {
            "section1": self.client.get_or_create_collection(
                name="hsk_basic_questions",
                embedding_function=self.embedding_fn,
                metadata={"description": "HSK听力理解题 - 基础对话"}
            ),
            "section2": self.client.get_or_create_collection(
                name="hsk_extended_questions",
                embedding_function=self.embedding_fn,
                metadata={"description": "HSK听力理解题 - 长对话"}
            ),
            "section3": self.client.get_or_create_collection(
                name="hsk_practical_questions",
                embedding_function=self.embedding_fn,
                metadata={"description": "HSK听力理解题 - 实际应用"}
            )
        }

    def _generate_pinyin(self, text: str) -> str:
        """Generate Pinyin for Chinese text"""
        try:
            pinyin_list = pinyin(text, style=Style.TONE)
            return ' '.join([item[0] for item in pinyin_list])
        except Exception as e:
            return str(e)

    def add_questions(self, section_num: int, questions: List[Dict], video_id: str, hsk_level: int = 4):
        """Add questions to the vector store with Chinese processing"""
        if section_num not in [1, 2, 3]:
            raise ValueError("支持的部分为1, 2, 3")  # Supported sections are 1, 2, 3
            
        collection = self.collections[f"section{section_num}"]
        
        ids = []
        documents = []
        metadatas = []
        
        for idx, question in enumerate(questions):
            question_id = f"{video_id}_{section_num}_{idx}"
            ids.append(question_id)
            
            # Process Chinese text and add Pinyin
            processed_question = self._process_question(question)
            
            metadatas.append({
                "video_id": video_id,
                "section": section_num,
                "question_index": idx,
                "hsk_level": hsk_level,
                "full_structure": json.dumps(processed_question, ensure_ascii=False)
            })
            
            # Create searchable document with both Chinese and Pinyin
            if section_num in [1, 2]:
                document = f"""
                介绍: {processed_question['Introduction']['text']}
                拼音: {processed_question['Introduction']['pinyin']}
                对话: {processed_question['Conversation']['text']}
                拼音: {processed_question['Conversation']['pinyin']}
                问题: {processed_question['Question']['text']}
                拼音: {processed_question['Question']['pinyin']}
                """
            else:  # section 3
                document = f"""
                情况: {processed_question['Situation']['text']}
                拼音: {processed_question['Situation']['pinyin']}
                问题: {processed_question['Question']['text']}
                拼音: {processed_question['Question']['pinyin']}
                """
            documents.append(document)
        
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def _process_question(self, question: Dict) -> Dict:
        """Process Chinese text in question with Pinyin"""
        processed = {}
        for key, value in question.items():
            if isinstance(value, str):
                processed[key] = {
                    'text': value,
                    'pinyin': self._generate_pinyin(value)
                }
            elif isinstance(value, list) and key == 'Options':
                processed[key] = [
                    {'text': opt, 'pinyin': self._generate_pinyin(opt)}
                    for opt in value
                ]
            else:
                processed[key] = value
        return processed

    def search_similar_questions(
        self, 
        section_num: int, 
        query: str, 
        n_results: int = 5,
        hsk_level: Optional[int] = None
    ) -> List[Dict]:
        """Search for similar questions with HSK level filtering"""
        if section_num not in [1, 2, 3]:
            raise ValueError("支持的部分为1, 2, 3")
            
        collection = self.collections[f"section{section_num}"]
        
        # Add Pinyin to query for better matching
        query_with_pinyin = f"{query}\n拼音: {self._generate_pinyin(query)}"
        
        where = {"section": section_num}
        if hsk_level is not None:
            where["hsk_level"] = hsk_level
        
        results = collection.query(
            query_texts=[query_with_pinyin],
            n_results=n_results,
            where=where
        )
        
        questions = []
        for idx, metadata in enumerate(results['metadatas'][0]):
            question_data = json.loads(metadata['full_structure'])
            question_data['similarity_score'] = results['distances'][0][idx]
            question_data['hsk_level'] = metadata['hsk_level']
            questions.append(question_data)
            
        return questions

    def parse_questions_from_file(self, filename: str) -> List[Dict]:
        """Parse questions from a structured text file with Chinese support"""
        questions = []
        current_question = {}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith('<question>'):
                    current_question = {}
                elif line.startswith(('介绍:', 'Introduction:')):
                    i += 1
                    current_question['Introduction'] = lines[i].strip()
                elif line.startswith(('对话:', 'Conversation:')):
                    i += 1
                    current_question['Conversation'] = lines[i].strip()
                elif line.startswith(('情况:', 'Situation:')):
                    i += 1
                    current_question['Situation'] = lines[i].strip()
                elif line.startswith(('问题:', 'Question:')):
                    i += 1
                    current_question['Question'] = lines[i].strip()
                elif line.startswith(('选项:', 'Options:')):
                    options = []
                    for _ in range(4):
                        i += 1
                        if i < len(lines):
                            option = lines[i].strip()
                            if option[0].isdigit() and option[1] == '.':
                                options.append(option[2:].strip())
                    current_question['Options'] = options
                elif line.startswith('</question>'):
                    if current_question:
                        questions.append(current_question)
                        current_question = {}
                i += 1
            return questions
        except Exception as e:
            print(f"解析问题时出错 {filename}: {str(e)}")  # Error parsing questions
            return []

    def index_questions_file(self, filename: str, section_num: int, hsk_level: int = 4):
        """Index questions from file with HSK level"""
        video_id = os.path.basename(filename).split('_section')[0]
        questions = self.parse_questions_from_file(filename)
        
        if questions:
            self.add_questions(section_num, questions, video_id, hsk_level)
            print(f"已索引 {len(questions)} 个问题，来自 {filename}")  # Indexed questions from file

if __name__ == "__main__":
    # Example usage
    store = ChineseQuestionVectorStore()
    
    # Index questions from files
    question_files = [
        ("backend/data/questions/sY7L5cfCWno_section2.txt", 2, 4),  # HSK4 level
        ("backend/data/questions/sY7L5cfCWno_section3.txt", 3, 4)   # HSK4 level
    ]
    
    for filename, section_num, hsk_level in question_files:
        if os.path.exists(filename):
            store.index_questions_file(filename, section_num, hsk_level)
    
    # Search for similar questions
    similar = store.search_similar_questions(
        section_num=2,
        query="关于在图书馆学习的对话",
        n_results=1,
        hsk_level=4
    )