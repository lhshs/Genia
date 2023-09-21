from kubernetes import client as k8s_client
from kubeflow import katib as ktb

from utils.katib_config import (
    ALGORITHM_SPEC,
    OBJECTIVE_SPEC,
    PARAMETERS,
    TRIAL_SPEC,
    TRIAL_PARAMETERS,
)
import time


class KatibController(object):
    def __init__(
        self,
        experiment_name: str,
        pip_name: str,
        model_type: str,
        namespace: str,
        max_trial_count: int = 5,
        parallel_trial_count: int = 2,
        max_failed_trial_count: int = 2,
        config_file: str = None,
    ):
        self.experiment_name = experiment_name
        self.kclient = ktb.KatibClient(config_file=config_file)
        self.pip_name = pip_name
        self.model_type = model_type
        self.max_trial_count = max_trial_count
        self.parallel_trial_count = parallel_trial_count
        self.max_failed_trial_count = max_failed_trial_count
        self.namespace = namespace

    def set_experiment_spec(self):
        add_arguments = [
            f"--pip_name={self.pip_name}",
            f"--model_type={self.model_type}",
        ]

        for arg in add_arguments:
            TRIAL_SPEC["spec"]["template"]["spec"]["containers"][0]["command"].append(
                arg
            )

        TRIAL_TEMPLATE = ktb.V1beta1TrialTemplate(
            primary_container_name="training-container",
            success_condition='status.conditions.#(type=="Complete")#|#(status=="True")#',
            failure_condition='status.conditions.#(type=="Failed")#|#(status=="True")#',
            retain=False,
            trial_parameters=TRIAL_PARAMETERS,
            trial_spec=TRIAL_SPEC,
        )

        return ktb.V1beta1ExperimentSpec(
            max_trial_count=self.max_trial_count,
            parallel_trial_count=self.parallel_trial_count,
            max_failed_trial_count=self.max_failed_trial_count,
            algorithm=ALGORITHM_SPEC,
            objective=OBJECTIVE_SPEC,
            parameters=PARAMETERS,
            trial_template=TRIAL_TEMPLATE,
        )

    def set_experiment_conf(self):
        METADATA = k8s_client.V1ObjectMeta(
            name=self.experiment_name,
            namespace=self.namespace,
        )
        EXPERIMENT_SPEC = self.set_experiment_spec()
        EXPERIMENT_CONFIG = ktb.V1beta1Experiment(
            api_version="kubeflow.org/v1beta1",
            kind="Experiment",
            metadata=METADATA,
            spec=EXPERIMENT_SPEC,
        )

        return EXPERIMENT_CONFIG

    def create_experiment(self):
        experiment = self.set_experiment_conf()
        res = self.kclient.create_experiment(experiment, namespace=self.namespace)
        return res

    def delete_experiment(self):
        res = self.kclient.delete_experiment(
            name=self.experiment_name, namespace=self.namespace
        )
        return res

    def is_experiment_succeeded(self):
        res = self.kclient.is_experiment_succeeded(
            name=self.experiment_name, namespace=self.namespace
        )
        return res

    def get_experiment_status(self):
        res = self.kclient.get_experiment_status(
            name=self.experiment_name, namespace=self.namespace
        )
        return res

    def get_optimal_hyperparameters(self):
        res = self.kclient.get_optimal_hyperparameters(
            name=self.experiment_name, namespace=self.namespace
        )
        return res

    def check_experiment_done(self):
        while True:
            time.sleep(15)
            status = self.get_experiment_status()

            if status in ["Created", "Running"]:
                print("!!Katib Experiment status: ", status)
                continue

            if self.is_experiment_succeeded() or status == "Failed":
                print("!!Katib Experiment finished: ", status)
                return False if status == "Failed" else True

            else:
                print("!!Unexpected status: ", status)
                return False