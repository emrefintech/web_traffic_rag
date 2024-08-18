import re
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class LogProcessor:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.log_entries = []
        self.df = None
        self.log_vectors = None
        self.index = None

    def parse_logs(self):

        #Log kayıtlarını regex yöntemi ile ayrıştırdım <> yaparak gruplandırma yaptım ki çağırırken çok daha
        #rahat olsun diye
        log_pattern = re.compile(
            r'(?P<ip_address>[\d\.]+) - - \[(?P<timestamp>[^\]]+)\] "(?P<request_method>\w+) (?P<url>[^\s]+) (?P<http_version>[^"]+)" (?P<status_code>\d+) - "(?P<user_agent>[^"]+)"'
        )

        # Log dosyasını okudum ve ayırdım
        with open(self.log_file_path, 'r') as file:
            for line in file:
                match = log_pattern.match(line)
                if match:
                    self.log_entries.append(match.groupdict())

        
        self.df = pd.DataFrame(self.log_entries)

    def vectorize_logs(self):
        model = SentenceTransformer('all-MiniLM-L6-v2')

        #Gruplandırma yaptığım için kolaylıkları verileri ayrıştırdım.
        log_texts = self.df.apply(
            lambda row: f"{row['ip_address']} {row['timestamp']} {row['request_method']} {row['url']} {row['http_version']} {row['status_code']} {row['user_agent']}", axis=1
        )

        #Vektörlere dönüştürdüm.
        self.log_vectors = model.encode(log_texts.tolist())

        print(f"Vektörlerin boyutu: {self.log_vectors.shape}")

    def build_faiss_index(self):
        #Boyut bilgisini dinamik olarak alıyorum
        d = self.log_vectors.shape[1]

        #FAISS indeksini oluşturuyorum (FlatL2 en temel indeks türlerinden biridir)
        self.index = faiss.IndexFlatL2(d)

        #Vektörleri FAISS indekse ekliyorum
        self.index.add(np.array(self.log_vectors))

        if self.index.ntotal > 0:
            print(f"FAISS indeksi başarıyla {self.index.ntotal} vektörle oluşturuldu.")
        else:
            print("Hata: FAISS indeksi düzgün oluşturulmadı.")

    def search_similar_logs(self, query_vector, k=5):
        #FAISS ile en yakın k komşuyu arıyorum çok fazla arttırmıyorum overfitting olmasın diye
        distances, indices = self.index.search(np.array([query_vector]), k)

        # Sonuçları derleyip geri döndürüyorum
        results = []
        for i, idx in enumerate(indices[0]):
            result = {
                "index": idx,
                "distance": distances[0][i],
                "log": self.df.iloc[idx].to_dict()
            }
            results.append(result)

        return results
