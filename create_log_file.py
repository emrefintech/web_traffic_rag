import random
from faker import Faker


# Faker kütüphanesi ile sahte veriler oluşturmak için bir nesne oluşturuyorum
fake = Faker()


def generate_log_entry():
    #Faker ile rastgele verileri oluşturdum, çünkü internette bulamadım.
    
    
    ip_address = fake.ipv4()  
    
    
    timestamp = fake.date_time_this_year().strftime('%d/%b/%Y:%H:%M:%S %z')  
    
    
    method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])  
    
    url = random.choice(['/index.html', '/contact.html', '/about.html', '/products.html', '/cart.html'])  
    status_code = random.choice([200, 404, 500, 301])  
    user_agent = fake.user_agent()  

    log_entry = f'{ip_address} - - [{timestamp}] "{method} {url} HTTP/1.1" {status_code} - "{user_agent}"'
    return log_entry



def generate_logs(num_entries=1000):
    #generate log entry 1 kere çalışınca 1 tane log kaydı oluşuyor bu fonksiyon sayesinde kaç tane 
    #oluşturabileceğimi ayarlamış oldum.
    logs = [generate_log_entry() for i in range(num_entries)]  
    return logs


def save_logs_to_file(logs, filename='_web_traffic_2500.log'):
    with open(filename, 'w') as f:
        for log in logs:
            f.write(log + '\n')  #


logs = generate_logs(num_entries=2500)
save_logs_to_file(logs)

print("Log dosyası başarıyla oluşturuldu.")
