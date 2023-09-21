#!/bin/bash

# INSTALL KUBEFLOW PIPELINES WITH MINIO
export PIPELINE_VERSION="2.0.1"

kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"

# IF PROXY-AGENT ERROR...
# kubectl delete deploy proxy-agent -n kubeflow

# INSTALL KATIB
kubectl apply -k "github.com/kubeflow/katib.git/manifests/v1beta1/installs/katib-standalone?ref=master"

# SET ROLEBINDING, LABELING
export NAMESPACE=kubeflow

kubectl -n ${NAMESPACE} create rolebinding katib-editor --clusterrole=katib-controller --serviceaccount=${NAMESPACE}:default
kubectl label ns ${NAMESPACE} katib.kubeflow.org/metrics-collector-injection=enabled