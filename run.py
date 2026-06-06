from flask import Flask, jsonify
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置数据库（Render会自动提供DATABASE_URL环境变量）
app.config['SQLALCRECY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCRECY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 示例模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

@app.route('/')
def home():
    return jsonify({
        'status': 'Flask API is running!',
        'database_url': 'Configured' if 'DATABASE_URL' in os.environ else 'Local SQLite'
    })

@app.route('/api/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建表（开发环境）
    app.run(host='0.0.0.0', port=5000)