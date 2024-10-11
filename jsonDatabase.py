from flask import Flask, request, jsonify
from jsonschema import validate, ValidationError
import json

file_path = 'PostsData.json' # путь к jsony

with open(file_path, 'r', encoding='utf-8') as f:
    data =  json.load(f)
 
def save_json(data, file_path): # сохранка в физ файл
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


posts = data['posts']
length = data['count']

app = Flask(__name__)



@app.route('/api/get/posts', methods=['GET'])
def get_posts():
    return jsonify(data)

@app.route('/api/post/passhqck7273', methods=['POST'])     #тут пароль на доступ к постингу прямо в urlке :), клиенты самостоятельно не постят
def receive_data():
    hookData = request.get_json()

    if hookData is None:
        return jsonify({'error': 'No JSON data provided'}), 400

    print(hookData)

    # схемочка json при запросе на пост
    schema = {
        "head": "string",
        "picture": "string",
        "file": "string",
        "username": "string"
    }

    # Проверка соответствия со схемочкой
    try:
        validate(instance=hookData, schema=schema)
        data['count'] += 1 
        data['posts'].append(hookData)
        save_json(data, file_path)
        return jsonify({'message': 'Data received successfully', 'received_data': hookData, 'post_number' : data['count']}), 200
    except ValidationError as e:    
        return jsonify({'error': 'JSON data not according to plan'}), 400

if __name__ == '__main__':
    app.run(host='www.oxnack.ru', port=8085, debug=True) # www.oxnack.ru:8085


