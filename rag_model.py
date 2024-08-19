from transformers import T5ForConditionalGeneration, T5Tokenizer
from log_processor import LogProcessor
from sentence_transformers import SentenceTransformer

class RAGModel(LogProcessor):
    def __init__(self, log_file_path):
        super().__init__(log_file_path)
        #Daha hızlı olması açısından t5-small kullandım t5-large kullandığımda programın çok uzun sürede açılıyor doğrulukta
        #artmadı large kullandığımda.
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small', legacy=False)
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')

    def generate_answer(self, query, top_k=5):
        # 1. Retrieval, aldığım bilgileri vektörlere çeviriyorum
        query_vector = self.vectorize_query(query)

        #Benzer logları arıyorum
        retrieved_logs = self.search_similar_logs(query_vector, k=top_k)

        # 2. Jeneratif Model (Generation) 
        context_list = []
        for log in retrieved_logs:
            log_data = log['log']
            context_list.append(
                f"IP: {log_data['ip_address']} accessed {log_data['url']} with status {log_data['status_code']} at {log_data['timestamp']}"
            )

        context = " ".join(context_list)
        
        
        #Girdiğim texti tokenize ediyorum
        input_text = f"answer question: {query} context: {context}"
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')

        
        output_ids = self.model.generate(input_ids, max_length=50)

        #Decode ediyorum ki insan için anlamlı bir cümle haline dönüşsün
        answer = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        

        return answer

    def vectorize_query(self, query):
        #Sorguyu vektörleştirme
        model = SentenceTransformer('all-MiniLM-L6-v2')
        return model.encode([query])[0]
