import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        #self.create_log_table()
        self.create_table("t_log")
    
    def create_log_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                message TEXT
            )
        ''')
        self.conn.commit()
    
    
    def log(self, message):
        self.cursor.execute("INSERT INTO logs (message) VALUES (?)", (message,))
        self.conn.commit()

    def create_table(self, table_name):
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                IP TEXT PRIMARY KEY,
                nombre INTEGER,
                cnbripdst INTEGER,
                cnportdst INTEGER,
                permit INTEGER,
                inf1024permit INTEGER,
                sup1024permit INTEGER,
                adminpermit INTEGER,
                deny INTEGER,
                inf1024deny INTEGER,
                sup1024deny INTEGER,
                admindeny INTEGER
            )
        '''
        self.cursor.execute(query)
        self.conn.commit()
    
    def create_table(self, table_name, columns):
        columns_def = ", ".join([f"{col} TEXT" for col in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
        self.cursor.execute(query)
        self.conn.commit()
    
    def insert_data_from_file(self, file_path, table_name):
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".txt"):
            df = pd.read_csv(file_path, delimiter="\t")
        elif file_path.endswith(".parquet"):
            df = pd.read_parquet(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Format de fichier non supporté")
        
        self.create_table(table_name, df.columns)
        df.to_sql(table_name, self.conn, if_exists="append", index=False)
        self.log(f"Données insérées dans la table {table_name} depuis {file_path}")
    
    def close(self):
        self.conn.close()

#utilisation
if __name__ == "__main__":
    db = DBManager()
    db.insert_data_from_file("data.xlsx", "consommation")
    db.close()
