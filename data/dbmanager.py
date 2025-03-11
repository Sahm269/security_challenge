import sqlite3
import pandas as pd

class DBManager:
    def __init__(self, db_name="database1.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # self.create_log_table("logs_data")
        

    def create_log_table(self, table_name):
        query = f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ipsrc,
                ipdst,
                portdst,
                proto,
                action,
                date,
                regle
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
            df = pd.read_csv(file_path,sep=",",names=["ipsrc","ipdst","portdst","proto","action","date","regle"])
        elif file_path.endswith(".txt"):
            df = pd.read_csv(file_path, sep = "\t", encoding="utf-8", names=["date","ipsrc", "ipdst", "proto", "portsrc","portdst","regle","action", "interface_In","interface_out"])  # header=0 pour utiliser la première ligne comme noms de colonnes

        elif file_path.endswith(".parquet"):
            df = pd.read_parquet(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Format de fichier non supporté")
        
        self.create_table(table_name, df.columns)
        df.to_sql(table_name, self.conn, if_exists="append", index=False)

    def query_select(self, sql_query, params=()):
        self.cursor.execute(sql_query, params)
        return self.cursor.fetchall()
    
    
    def close(self):
        self.conn.close()

#utilisation
# Exemple d'utilisation
if __name__ == "__main__":
    db = DBManager()
    db.insert_data_from_file("log_cleaned.txt", "logs_data")
    result = db.query_select("SELECT * from logs_data LIMIT 5")
    print(result)
    db.close()
