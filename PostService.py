from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

@app.route('/api/userpost', methods=['POST'])
def upload():
    if 'json' not in request.files or 'image' not in request.files or 'file' not in request.files:
        return jsonify({"error": "Missing files in the request"}), 400

    json_file = request.files['json']
    json_data = json_file.read().decode('utf-8')
    
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON"}), 400

    head = data.get('head')
    picture_name = data.get('picture')
    file_name = data.get('file')
    username = data.get('username')

    # Проверяем, что все необходимые поля присутствуют
    if not all([head, picture_name, file_name, username]):
        return jsonify({"error": "Missing fields in JSON"}), 400

    # Сохраняем файлы
    image_file = request.files['image']
    unknown_file = request.files['file']

    # Создаем директорию для сохранения файлов, если она не существует
    os.makedirs('uploads', exist_ok=True)

    # Сохраняем файлы
    image_path = os.path.join('uploads', picture_name)
    unknown_path = os.path.join('uploads', file_name)

    image_file.save(image_path)
    unknown_file.save(unknown_path)

    return jsonify({"message": "Files uploaded successfully", "username": username}), 200

if __name__ == '__main__':
    app.run(host='www.oxnack.ru', port=8087, debug=True)
