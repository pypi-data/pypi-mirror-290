# custom_model/linear_model.py

import mlflow.pyfunc
import os

class LinearModel(mlflow.pyfunc.PythonModel):
    """
    A custom MLflow model that implements the linear function y = 2x + 3.
    """

    def predict(self, context, model_input):
        return model_input * 2 + 3

def log_linear_model():
    """
    Logs the custom linear model to MLflow and packages it as a wheel file.
    """
    model = LinearModel()
    with mlflow.start_run() as run:
        mlflow.pyfunc.log_model(artifact_path="linear_model", python_model=model)
        print(f"Model logged under run_id: {run.info.run_id}")

    # Save the wheel file
    model_dir = "linear_model"
    mlflow.pyfunc.save_model(path=model_dir, python_model=model)
    os.system(f"cd {model_dir} && python setup.py bdist_wheel")
    print(f"Wheel file created in {model_dir}/dist/")

if __name__ == "__main__":
    log_linear_model()
