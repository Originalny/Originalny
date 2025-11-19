from flask import Flask, jsonify
import pathlib

app = Flask(__name__)


def get_version() -> str:
    """Читает текущую версию приложения из файла VERSION."""
    version_file = pathlib.Path("VERSION")
    return version_file.read_text(encoding="utf-8").strip()


@app.route("/")
def index():
    return jsonify(
        {
            "status": "pipeline-test3",
            "version": get_version(),
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
