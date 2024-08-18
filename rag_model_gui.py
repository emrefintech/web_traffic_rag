import tkinter as tk
from tkinter import ttk, messagebox
from rag_model import RAGModel
import time

# RAGModel sınıfını yükleyip gerekli işlemleri yapıyorum
rag_model = RAGModel('_web_traffic_2500.log')
rag_model.parse_logs()
rag_model.vectorize_logs()
rag_model.build_faiss_index()

def extract_statistics(df):
    #En yaygın hata kodunu buluyorum
    most_common_error = df['status_code'].mode()[0]

    #En sık erişilen URL'i buluyorum
    most_accessed_url = df['url'].mode()[0]

    #En yaygın HTTP metodunu belirliyorum
    most_common_http_method = df['request_method'].mode()[0]

    #En sık erişim yapan IP adresini tespit ediyorum
    most_frequent_ip = df['ip_address'].mode()[0]
    
    #En sık 404 hatası alan IP adresini buluyorum
    most_frequent_404_ip = df[df['status_code'] == '404']['ip_address'].mode()[0]

    #En sık 500 hatası alan URL'i buluyorum
    most_frequent_500_url = df[df['status_code'] == '500']['url'].mode()[0]

    return {
        "most_common_error": most_common_error,
        "most_accessed_url": most_accessed_url,
        "most_common_http_method": most_common_http_method,
        "most_frequent_ip": most_frequent_ip,
        "most_frequent_404_ip": most_frequent_404_ip,
        "most_frequent_500_url": most_frequent_500_url,
    }

class RAGModelGUI:
    def __init__(self, master):
        self.master = master
        master.title("RAG Model GUI")
        
        #Test Et Butonu
        self.test_button = ttk.Button(master, text="Test Model", command=self.test_model)
        self.test_button.pack(pady=10)
        
        #Soru Sor Butonu
        self.ask_button = ttk.Button(master, text="Ask Model", command=self.ask_model)
        self.ask_button.pack(pady=10)

        #Temizle Butonu
        self.clear_button = ttk.Button(master, text="Clear", command=self.clear_results)
        self.clear_button.pack(pady=10)

        #Sonuçların Gösterildiği Alan (Treeview kullanarak sonuçları tablo halinde gösteriyorum)
        self.result_tree = ttk.Treeview(master, columns=("Question", "Generated Answer", "Expected Answer", "Correct"), show='headings', height=15)
        self.result_tree.heading("Question", text="Question")
        self.result_tree.heading("Generated Answer", text="Generated Answer")
        self.result_tree.heading("Expected Answer", text="Expected Answer")
        self.result_tree.heading("Correct", text="Correct (Yes/No)")

        self.result_tree.column("Question", width=200)
        self.result_tree.column("Generated Answer", width=200)
        self.result_tree.column("Expected Answer", width=200)
        self.result_tree.column("Correct", width=100)

        self.result_tree.pack(pady=10)

    def test_model(self):
        self.clear_results()

        #İstatistiksel verileri dinamik olarak elde ediyorum
        stats = extract_statistics(rag_model.df)

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
            },
            {
                "question": "Which IP address received the most 404 errors?",
                "expected_answer": stats['most_frequent_404_ip']
            },
            {
                "question": "Which URL received the most 500 errors?",
                "expected_answer": stats['most_frequent_500_url']
            }
        ]

        correct_count = 0
        start_time = time.time()

        for qa in questions_and_expected_answers:
            question = qa["question"]
            expected_answer = qa["expected_answer"]
            generated_answer = rag_model.generate_answer(question)

            correct = "Yes" if str(expected_answer) in generated_answer else "No"
            if correct == "Yes":
                correct_count += 1

            self.result_tree.insert("", "end", values=(question, generated_answer, expected_answer, correct))

        total_questions = len(questions_and_expected_answers)
        accuracy = (correct_count / total_questions) * 100
        avg_response_time = (time.time() - start_time) / total_questions

        messagebox.showinfo("Test Results", f"Accuracy: {accuracy}%\nAverage Response Time: {avg_response_time:.2f} seconds")

    def ask_model(self):
        ask_window = tk.Toplevel(self.master)
        ask_window.title("Ask the Model")
        
        # Soru listesi
        question_label = tk.Label(ask_window, text="Select a Question:")
        question_label.pack(pady=5)

        questions = [
            "What are the most common errors?",
            "Which IP address accessed the most frequent URL the most?",
            "What is the most common HTTP method used?",
            "Which IP address received the most 404 errors?",
            "Which URL received the most 500 errors?",
            "Which country received the most rain in 2024?",  #Alakasız soru, nasıl cevap vereceğini merak ettim
            "What is the tallest mountain?"  #Alakasız soru, nasıl cevap vereceğini merak ettim
        ]

        
        self.question_combobox = ttk.Combobox(ask_window, values=questions, width=50)
        self.question_combobox.pack(pady=5)

        ask_button = ttk.Button(ask_window, text="Ask", command=self.generate_answer)
        ask_button.pack(pady=10)

    def generate_answer(self):
        selected_question = self.question_combobox.get()
        if not selected_question:
            messagebox.showwarning("Warning", "Please select a question.")
            return
        
        generated_answer = rag_model.generate_answer(selected_question)
        expected_answer = "N/A"  
        self.result_tree.insert("", "end", values=(selected_question, generated_answer, expected_answer, ""))

    def clear_results(self):
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

if __name__ == "__main__":
    root = tk.Tk()
    gui = RAGModelGUI(root)
    root.mainloop()
