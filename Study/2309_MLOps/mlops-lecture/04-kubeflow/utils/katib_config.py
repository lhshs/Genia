from kubeflow import katib as ktb
import settings

IMAGE_URL = settings.KTB_IMAGE_URL

ALGORITHM_SPEC = ktb.V1beta1AlgorithmSpec(
    algorithm_name="bayesianoptimization",
    algorithm_settings=[
        ktb.V1beta1AlgorithmSetting(name="base_estimator", value="GP"),
        ktb.V1beta1AlgorithmSetting(name="n_initial_points", value="10"),
        ktb.V1beta1AlgorithmSetting(name="acq_func", value="gp_hedge"),
        ktb.V1beta1AlgorithmSetting(name="acq_optimizer", value="auto"),
    ],
)

# Objective specification.
OBJECTIVE_SPEC = ktb.V1beta1ObjectiveSpec(
    type="minimize",
    goal=0.8,
    objective_metric_name="VAL_LOSS",
    metric_strategies=[
        ktb.V1beta1MetricStrategy(
            name="VAL_LOSS",
            value="min",
        ),
    ],
)

PARAMETERS = [
    ktb.V1beta1ParameterSpec(
        name="epochs",
        parameter_type="int",
        feasible_space=ktb.V1beta1FeasibleSpace(
            min="10",
            max="50",
            step="2",
        ),
    ),
    ktb.V1beta1ParameterSpec(
        name="batch_size",
        parameter_type="int",
        feasible_space=ktb.V1beta1FeasibleSpace(
            min="48",
            max="256",
            step="16",
        ),
    ),
]

# JSON template specification for the Trial's Worker Kubernetes Job.
TRIAL_SPEC = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "spec": {
        "template": {
            "metadata": {"annotations": {"sidecar.istio.io/inject": "false"}},
            "spec": {
                "containers": [
                    {
                        "name": "training-container",
                        "image": IMAGE_URL,
                        "command": [
                            "python",
                            "02-training.py",
                            "--epochs=${trialParameters.epochs}",
                            "--batch_size=${trialParameters.batch_size}",
                        ],
                        "env": [
                            {
                                "name": "TF_CPP_MIN_LOG_LEVEL",
                                "value": "3",
                            },
                            # ADD YOUR ENVIONMENT VARIABLES...
                        ],
                    }
                ],
                "restartPolicy": "Never",
            },
        }
    },
}

TRIAL_PARAMETERS = [
    ktb.V1beta1TrialParameterSpec(
        name="epochs",
        description="epoch for the training model",
        reference="epochs",
    ),
    ktb.V1beta1TrialParameterSpec(
        name="batch_size",
        description="batch_size for the training model",
        reference="batch_size",
    ),
]