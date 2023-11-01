import logging
from flask import Flask, request, render_template
import requests
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

TELEGRAM_TOKEN = 'Botunuzun Tokeni'
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

channel_id = None
message = None

def send_telegram_message():
    global channel_id, message
    if channel_id and message:
        payload = {'chat_id': channel_id, 'text': message}
        requests.post(TELEGRAM_URL, data=payload)

@app.route('/')
def home():
    app.logger.info('Home route accessed')
    return render_template('index.html')

@app.route('/set_message', methods=['POST'])
def set_message():
    app.logger.info('set_message route accessed')
    global channel_id, message
    channel_id = request.form['channel_id']
    message = request.form['message']
    interval = int(request.form['interval'])
    scheduler.add_job(send_telegram_message, 'interval', seconds=interval, id='telegram_message_job')
    return 'Mesaj Zamanlandı!', 200

@app.route('/stop_message', methods=['POST'])
def stop_message():
    app.logger.info('stop_message route accessed')
    scheduler.remove_job('telegram_message_job')
    return 'Mesaj Gönderimi Durduruldu!', 200

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.start()
    app.run(debug=True)
    atexit.register(lambda: scheduler.shutdown())
