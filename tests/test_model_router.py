from core.model_manager import ModelManager


def test_general_model():
    manager = ModelManager()
    assert manager.choose_model("explain photosynthesis") == "qwen3:0.6b"


def test_coding_model():
    manager = ModelManager()
    assert manager.choose_model("write Python code for a Flask API") == "qwen2.5-coder:1.5b"
