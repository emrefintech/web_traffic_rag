
---

# **RAG Model for Web Traffic Log Analysis**

## **Overview**

This project is focused on analyzing web traffic logs using a Retrieval-Augmented Generation (RAG) model built on the T5 language model. The system retrieves relevant log entries based on a user query and generates meaningful answers. The primary goal is to process large volumes of log data, find patterns, and generate insightful responses based on the data.

## **Features**

- **Log Data Generation:** Simulate web traffic log entries using the `Faker` library to create a realistic dataset.
- **Log Data Processing:** Parse and structure log data using regex patterns.
- **Vectorization:** Convert log entries and user queries into vector representations using the `SentenceTransformer` model.
- **FAISS Indexing:** Efficiently search and retrieve the most relevant log entries using the FAISS library.
- **RAG Model Implementation:** Generate answers based on the retrieved log entries using a T5 model.
- **GUI Interface:** Interact with the model through a user-friendly graphical interface built with Tkinter.
- **Model Scalability:** Easily switch between different T5 model sizes (`t5-small`, `t5-large`, etc.) to improve response accuracy.

## **Installation**

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/emrefintech/web_traffic_rag.git
   cd web_traffic_rag
   ```

2. **Install Required Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application:**
   ```bash
   python rag_model_gui.py
   ```

## **Project Structure**

- `create_log_file.py`: Generates synthetic web traffic log entries using the `Faker` library.
- `log_processor.py`: Processes and vectorizes log data, and implements FAISS indexing for efficient retrieval.
- `rag_model.py`: Defines the RAG model that uses a T5 model to generate answers based on retrieved log entries.
- `rag_model_gui.py`: Provides a graphical interface for interacting with the RAG model.
- `main_for_console.py`: Evaluates the model’s performance by testing it with predefined queries.
- `requirements.txt`: Lists all the dependencies required for the project.

## **How It Works**

### **1. Log Data Generation**
The `Faker` library is used to generate synthetic web traffic logs that mimic real-world data. These logs include fields such as IP address, timestamp, HTTP method, URL, status code, and user agent.

**Why use Faker?**  
The `Faker` library allows us to generate realistic data for testing purposes. This helps simulate real-world scenarios without needing access to sensitive or proprietary data.

### **2. Log Data Processing**
The logs are parsed using a regular expression pattern, extracting relevant fields like IP addresses, timestamps, HTTP methods, URLs, status codes, and user agents. This structured data is then stored in a Pandas DataFrame for further processing.

**Regex Explanation:**  
The regex pattern used to parse the logs is as follows:
```python
r'(?P<ip_address>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<request_method>\w+) (?P<url>[^\s]+) (?P<http_version>[^"]+)" (?P<status_code>\d+) - "(?P<user_agent>[^"]+)"'
```
This pattern is designed to extract specific components from each log entry, such as the IP address, timestamp, and request details, and assign them to named groups. These groups can then be accessed directly, as if they were columns in a table.

### **3. Vectorization**
Each log entry is converted into a vector representation using the `SentenceTransformer` model (`all-MiniLM-L6-v2`). This step is crucial for enabling the FAISS index to efficiently search and retrieve the most relevant logs.

**Why choose `all-MiniLM-L6-v2`?**  
This model is a lightweight, fast, and effective option for embedding sentences into vectors. It strikes a good balance between performance and computational efficiency, making it ideal for handling large datasets like web traffic logs.

### **4. FAISS Indexing**
The FAISS (Facebook AI Similarity Search) library is used to build an index of the log vectors. This allows for fast retrieval of the most relevant log entries based on a query vector. The `IndexFlatL2` is chosen as it performs a simple and efficient L2 (Euclidean) distance search.

**Nearest Neighbors Search:**  
When a query is vectorized, the FAISS index searches for the `k` nearest neighbors. The number of neighbors (`k`) affects the breadth of the results: a higher `k` retrieves more entries, while a lower `k` focuses on the most similar entries.

### **5. RAG Model Implementation**
The Retrieval-Augmented Generation (RAG) model is implemented using a T5 model. The process involves:
- Retrieving the top `k` most relevant log entries using the FAISS index.
- Constructing a context string from these entries.
- Feeding this context into the T5 model along with the user query to generate an answer.

**T5 Model Selection:**  
The T5 model (`t5-small`) is used for its versatility and efficiency in handling various text-to-text tasks. Depending on computational resources, larger T5 models (e.g., `t5-large`) can be used to potentially improve answer accuracy.

### **6. GUI Interface**
The Tkinter library is used to create a user-friendly graphical interface, allowing users to interact with the RAG model. Users can test the model with predefined queries or ask custom questions and receive generated answers. The GUI also includes a feature to clear previous results.

### **7. Performance Considerations**
The quality of the answers generated by the model can vary depending on the T5 model size and the number of neighbors retrieved by FAISS. Using a larger model (e.g., `t5-large`) can lead to more accurate answers, while tuning the `k` parameter in FAISS can improve the relevance of the retrieved logs.

**Why is accuracy low?**  
If accuracy is low, consider the following:
- **Model Size:** Upgrade to a larger T5 model.
- **k-Nearest Neighbors:** Experiment with different `k` values to balance relevance and diversity in retrieved logs.

## **FAQ**

### **Why use the `Faker` library?**
The `Faker` library is used to generate synthetic data for testing purposes, allowing the model to be trained and tested without relying on real, potentially sensitive data.

### **How does the regex pattern work?**
The regex pattern parses log entries into named groups (e.g., `ip_address`, `timestamp`), making it easy to extract and work with specific fields from the logs.

### **What is FAISS, and why is it used?**
FAISS is a library for efficient similarity search and clustering of dense vectors. It enables fast retrieval of the most relevant log entries based on a query vector, making it ideal for large-scale data like web logs.

### **How does the model generate answers?**
The model uses a two-step process: it first retrieves relevant log entries using FAISS, then generates an answer by feeding the retrieved context into the T5 model.

### **Will using a larger T5 model improve accuracy?**
Yes, using a larger T5 model can improve the quality and accuracy of the generated answers, as larger models have been trained on more data and have a better understanding of language nuances.

### **How can I improve the model's performance?**
- **Upgrade the T5 model size:** Consider using `t5-large` or even larger variants.
- **Tune FAISS parameters:** Experiment with the `k` value to find the optimal balance between precision and recall.
- **Fine-tune the model:** Consider fine-tuning the T5 model on your specific log data for better task-specific performance.

## **Contributing**

Contributions are welcome! If you have any suggestions, improvements, or bug fixes, please open an issue or submit a pull request.

## **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Acknowledgments**

- [Faker Library](https://faker.readthedocs.io/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)

---
