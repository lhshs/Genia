from kubeflow import katib as ktb


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
    type="",
    goal=0,
    objective_metric_name="",
    metric_strategies=[
        ktb.V1beta1MetricStrategy(
            name="",
            value="",
        ),
    ],
)
PARAMETERS = [
    ktb.V1beta1ParameterSpec(
        name="",
        parameter_type="",
        feasible_space=ktb.V1beta1FeasibleSpace(
            min="",
            max="",
            step="",
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
                        "image": "",
                        "command": [
                            "python",
                            "",
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
        name="",
        description="",
        reference="",
    ),
]
