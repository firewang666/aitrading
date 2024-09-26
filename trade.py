from flask import Flask, jsonify
import os
import gdown
import subprocess
app = Flask(__name__)

execution_status = {
    "status": "Not yet executed",  # 初始状态
    "details": ""
}

@app.route('/')
def home():
    # 显示当前的执行状态
    return f"""
        <h1>Welcome to the Colab Runner API</h1>
        <p>Current execution status: <strong>{execution_status['status']}</strong></p>
        <p>Details: {execution_status['details']}</p>
        <p>To trigger the Colab notebook, visit <a href='/run-colab'>/run-colab</a></p>
    """
    
    
@app.route('/run-colab', methods=['GET'])
def run_colab():
    global execution_status  # 使用全局变量
    try:
        execution_status['status'] = "Running"
        execution_status['details'] = "Colab notebook is being executed."
        output = "/tmp/notebook.py" 
        gdown.download('https://colab.research.google.com/drive/1q9xxQMu4r2rXtXfbFT98CPAOpSUba05Z?usp=sharing', output, quiet=False)
        # 执行 Colab 文档（你可以选择用 nbconvert 或其他工具运行）
        result = subprocess.run(['python3', output], capture_output=True, text=True)

        if result.returncode == 0:
            # 成功执行，更新状态为成功
            execution_status['status'] = "Success"
            execution_status['details'] = result.stdout
            return jsonify({"message": "Script executed successfully!", "output": result.stdout})
        else:
            # 执行失败，更新状态为失败
            execution_status['status'] = "Failed"
            execution_status['details'] = result.stderr
            return jsonify({"error": "Failed to execute script", "details": result.stderr}), 500

    except Exception as e:
        execution_status['status'] = "Error"
        execution_status['details'] = str(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
