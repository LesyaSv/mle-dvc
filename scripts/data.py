## scripts/data.py


import os
import yaml

# 2 — вспомогательные функции
def create_connection():
    from dotenv import load_dotenv

    load_dotenv()
    host = os.environ.get('DB_DESTINATION_HOST')
    port = os.environ.get('DB_DESTINATION_PORT')
    db = os.environ.get('DB_DESTINATION_NAME')
    username = os.environ.get('DB_DESTINATION_USER')
    password = os.environ.get('DB_DESTINATION_PASSWORD')
    from sqlalchemy import create_engine
    print(f'postgresql://{username}:{password}@{host}:{port}/{db}')
    conn = create_engine(f'postgresql://{username}:{password}@{host}:{port}/{db}', connect_args={'sslmode':'require'})
    return conn

# 3 — главная функция
def get_data():
    import pandas
    # 3.1 — загрузка гиперпараметров
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
    # 3.2 — загрузки предыдущих результатов нет, так как это первый шаг

    # 3.3 — основная логика
    conn = create_connection()
    data = pandas.read_sql('select * from users_churn', conn, index_col=params['index_col'])
    print(data)
    #conn.dispose()
    
    # 3.4 — сохранение результата шага
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/initial_data.csv', index=True)

# 4 — защищённый вызов главной функции
if __name__ == '__main__':
    get_data() 