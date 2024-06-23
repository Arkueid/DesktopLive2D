from flask import Flask

app = Flask("chat-server")


@app.route("/")
def index():
    return "hello, world"


if __name__ == '__main__':
    app.run("::", 80)
