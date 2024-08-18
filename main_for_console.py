from rag_model import RAGModel
import time


def extract_statistics(df):
    #En yaygın hata kodunu buluyorum
    most_common_error = df['status_code'].mode()[0]

    #En sık erişilen URL'i buluyorum
    most_accessed_url = df['url'].mode()[0]

    #En sık kullanılan HTTP metodunu belirliyorum
    most_common_http_method = df['request_method'].mode()[0]

    #En sık erişim yapan IP adresini tespit ediyorum
    most_frequent_ip = df['ip_address'].mode()[0]

    return {
        "most_common_error": most_common_error,
        "most_accessed_url": most_accessed_url,
        "most_common_http_method": most_common_http_method,
        "most_frequent_ip": most_frequent_ip
    }

def evaluate_performance():
    #RAG modelini oluşturup gerekli işlemleri yapıyorum
    rag_model = RAGModel('_web_traffic_2500.log')
    rag_model.parse_logs()
    rag_model.vectorize_logs()
    rag_model.build_faiss_index()

    #Loglardan istatistiksel verileri çıkarıyorum
    stats = extract_statistics(rag_model.df)

    #Soru cevap eşleştirmelerini hazırlıyorum
    questions_and_expected_answers = [
        {
            "question": "What are the most common errors?",
            "expected_answer": stats['most_common_error']
        },
        {
            "question": "Which IP address accessed the most frequent URL the most?",
            "expected_answer": stats['most_frequent_ip']
        },
        {
            "question": "What is the most common HTTP method used?",
            "expected_answer": stats['most_common_http_method']
        }
    ]

    correct_count = 0
    total_time = 0

    #Her soru için modelin cevabını alıp doğru olup olmadığını kontrol ediyorum
    for qa in questions_and_expected_answers:
        question = qa["question"]
        expected_answer = qa["expected_answer"]

        start_time = time.time()
        generated_answer = rag_model.generate_answer(question)
        end_time = time.time()

        total_time += (end_time - start_time)

        print(f"Soru: {question}")
        print(f"Modelin Verdiği Cevap: {generated_answer}")
        print(f"Beklenen Cevap: {expected_answer}")

        if str(expected_answer) in generated_answer:
            print("Modelin cevabı doğru!")
            correct_count += 1
        else:
            print("Modelin cevabı yanlış.")

        print()

    #Genel performans değerlendirmesini yapıyorum
    total_questions = len(questions_and_expected_answers)
    accuracy = (correct_count / total_questions) * 100
    avg_response_time = total_time / total_questions

    print(f"Doğruluk: {accuracy}%")
    print(f"Ortalama Yanıt Süresi: {avg_response_time:.2f} saniye")

if __name__ == "__main__":
    evaluate_performance()

