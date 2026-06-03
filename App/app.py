import time
import os
import io
import base64
import pandas as pd
import matplotlib.pyplot as plt
import redis
from flask import Flask, render_template
from dotenv import load_dotenv

# Configuratie: laadt variabelen uit het .env bestand
load_dotenv() 

# Verbinden met Redis
cache = redis.Redis(
    host=os.getenv('REDIS_HOST', 'redis'), 
    port=6379, 
    password=os.getenv('REDIS_PASSWORD')
)
app = Flask(__name__)

# Functie om het aantal hits op te halen uit Redis
def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

# Route voor de Homepagina
@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name="BIPM", count=count)

# Route voor de Titanic Pagina
@app.route('/titanic')
def titanic():
    # 1. Data inladen
    df = pd.read_csv('titanic.csv')
    
    # 2. Tabel (eerste 5 rijen)
    table = df.head(5).to_html(classes='table table-striped')
    
    # 3. Grafiek (Overlevenden per geslacht)
    # Let op: hier gebruiken we de kleine letters 'sex' en 'survived'
    fig, ax = plt.subplots()
    df.groupby('sex')['survived'].sum().plot(kind='bar', ax=ax)
    plt.title('Survivors by Sex')
    plt.tight_layout()
    
    # Grafiek omzetten naar plaatje (base64)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    
    return render_template('titanic.html', table=table, chart=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)