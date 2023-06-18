from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Kết nối tới MQTT broker
broker_address = "broker.hivemq.com"
client = mqtt.Client()
client.connect(broker_address)

# Khởi tạo temperature và humidity
temperature = 0
humidity = 0


# Trang chủ của ứng dụng web
@app.route("/")
def index():
    return render_template("index.html")


# API trả về dữ liệu nhiệt độ và độ ẩm mới nhất
@app.route("/api/data")
def get_data():
    # Gửi yêu cầu lấy dữ liệu mới nhất tới MQTT broker
    client.publish("antgroup0905/get_data", "get_data")
    # Trả về dữ liệu dưới dạng JSON
    return jsonify({"temperature": temperature, "humidity": humidity})


# Hàm xử lý khi nhận được dữ liệu từ MQTT broker
def on_message(client, userdata, message):
    global temperature, humidity
    # Lấy dữ liệu từ message payload
    data = message.payload.decode()
    temperature, humidity = data.split(",")
    temperature = float(temperature)
    humidity = float(humidity)


# Thiết lập callback function cho MQTT client
client.on_message = on_message
client.subscribe("newtesting")

if __name__ == "__main__":
    # Start MQTT client
    client.loop_start()
    # Start Flask app
    app.run(debug=True)
