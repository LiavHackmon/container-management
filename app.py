from flask import Flask, render_template, request, redirect
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/')
def home():
    containers = client.containers.list(all=True)
    return render_template('index.html', containers=containers)

@app.route('/create', methods=['GET', 'POST'])
def create_container():
    if request.method == 'POST':
        name = request.form['name']
        image = request.form['image']
        host_port = request.form['host_port']
        container_port = request.form['container_port']
        try:
            container = client.containers.run(
                image,
                name=name,
                ports={f"{container_port}/tcp": host_port},
                detach=True
            )
            return redirect(f"http://localhost:{host_port}")
        except Exception as e:
            return f"שגיאה ביצירת הקונטיינר: {e}"
    return render_template('create.html')

@app.route('/delete/<container_id>')
def delete_container(container_id):
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return redirect('/')
    except Exception as e:
        return f"שגיאה במחיקת הקונטיינר: {e}"

if __name__ == '__main__':
    app.run(debug=True)
