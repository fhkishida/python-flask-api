from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
taskIndex = 0

@app.route('/tasks', methods=["POST"])
def create_task():
    global taskIndex
    data = request.get_json()
    new_task = Task(title=data.get("title"), description=data.get("description", ""), id=taskIndex)
    taskIndex += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso"}), 201

@app.route('/tasks', methods=["GET"])
def get_tasks():
    tasks_list = [task.to_dict() for task in tasks]

    output = {
        "tasks": tasks_list,
        "total_tasks": len(tasks_list)
    }

    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
        if t.id == id:
            return jsonify(t.to_dict()), 200
    
    return jsonify({"message": "Não foi possível encontar atividade"}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task = t
    
    if task == None:
        return jsonify({"message": "Não foi possível encontrar atividade"}), 404

    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]

    return jsonify({"message": "Tarefa atualizada com sucesso"}), 200 

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = None
    for t in tasks: 
        if t.id == id:
            tasks.remove(t)
            return jsonify({"message": f"Tarefa {t.title} removida com sucesso"}), 200
        
    if task == None:
        return jsonify({'message': "Não foi possível encontrar atividade"}), 404

if __name__ == "__main__":
    app.run(debug=True)