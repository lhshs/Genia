from utils.katib_controller import KatibController

import settings

if __name__ == "__main__":
    
    pip_name = settings.PIP_NAME
    experiment_name = f"{pip_name}-mf"
    
    controller = KatibController(
        experiment_name=experiment_name,
        pip_name=pip_name,
        model_type="mf",
        namespace="kubeflow",
        max_trial_count=5,
        parallel_trial_count=2,
        max_failed_trial_count=2,
    )
    
    _ = controller.create_experiment()
    
    result = controller.check_experiment_done()
    print("result: ", result)
    