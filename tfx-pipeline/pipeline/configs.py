# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""TFX taxi template configurations.

This file defines environments for a TFX taxi pipeline.
"""

import os  # pylint: disable=unused-import

# TODO(b/149347293): Move more TFX CLI flags into python configuration.

# Pipeline name will be used to identify this pipeline.
PIPELINE_NAME = 'tfx-pipeline'

# GCP related configs.

# Following code will retrieve your GCP project. You can choose which project
# to use by setting GOOGLE_CLOUD_PROJECT environment variable.
try:
  import google.auth  # pylint: disable=g-import-not-at-top  # pytype: disable=import-error
  try:
    _, GOOGLE_CLOUD_PROJECT = google.auth.default()
  except google.auth.exceptions.DefaultCredentialsError:
    GOOGLE_CLOUD_PROJECT = ''
except ImportError:
  GOOGLE_CLOUD_PROJECT = ''

# Specify your GCS bucket name here. You have to use GCS to store output files
# when running a pipeline with Kubeflow Pipeline on GCP or when running a job
# using Dataflow. Default is '<gcp_project_name>-kubeflowpipelines-default'.
# This bucket is created automatically when you deploy KFP from marketplace.
GCS_BUCKET_NAME = GOOGLE_CLOUD_PROJECT + '-kubeflowpipelines-default'

# TODO(step 8,step 9): (Optional) Set your region to use GCP services including
#                      BigQuery, Dataflow and Cloud AI Platform.
GOOGLE_CLOUD_REGION = 'us-central1'  # ex) 'us-central1'

# Following image will be used to run pipeline components run if Kubeflow
# Pipelines used.
# This image will be automatically built by CLI if we use --build-image flag.
PIPELINE_IMAGE = f'gcr.io/{GOOGLE_CLOUD_PROJECT}/{PIPELINE_NAME}'

PREPROCESSING_FN = 'models.preprocessing.preprocessing_fn'
RUN_FN = 'models.keras_model.model.run_fn'
# NOTE: Uncomment below to use an estimator based model.
# RUN_FN = 'models.estimator_model.model.run_fn'

TRAIN_NUM_STEPS = 1000
EVAL_NUM_STEPS = 150

# Change this value according to your use cases.
EVAL_ACCURACY_THRESHOLD = 0.6

# Beam args to run data processing on DataflowRunner.
#
# TODO(b/151114974): Remove `disk_size_gb` flag after default is increased.
# TODO(b/156874687): Remove `machine_type` after IP addresses are no longer a
#                    scaling bottleneck.
# TODO(b/171733562): Remove `use_runner_v2` once it is the default for Dataflow.
# TODO(step 8): (Optional) Uncomment below to use Dataflow.
# DATAFLOW_BEAM_PIPELINE_ARGS = [
#    '--project=' + GOOGLE_CLOUD_PROJECT,
#    '--runner=DataflowRunner',
#    '--temp_location=' + os.path.join('gs://', GCS_BUCKET_NAME, 'tmp'),
#    '--region=' + GOOGLE_CLOUD_REGION,
#
#    # Temporary overrides of defaults.
#    '--disk_size_gb=50',
#    '--machine_type=e2-standard-8',
#    '--experiments=use_runner_v2',
# ]

# A dict which contains the training job parameters to be passed to Google
# Cloud AI Platform. For the full set of parameters supported by Google Cloud AI
# Platform, refer to
# https://cloud.google.com/ml-engine/reference/rest/v1/projects.jobs#Job
# TODO(step 9): (Optional) Uncomment below to use AI Platform training.
GCP_AI_PLATFORM_TRAINING_ARGS = {
    'project': GOOGLE_CLOUD_PROJECT,
    'region': GOOGLE_CLOUD_REGION,
    'scaleTier': 'BASIC_GPU',
    'masterConfig': {
      'imageUri': PIPELINE_IMAGE
    },
}

# A dict which contains the serving job parameters to be passed to Google
# Cloud AI Platform. For the full set of parameters supported by Google Cloud AI
# Platform, refer to
# https://cloud.google.com/ml-engine/reference/rest/v1/projects.models
# TODO(step 9): (Optional) Uncomment below to use AI Platform serving.
# GCP_AI_PLATFORM_SERVING_ARGS = {
#     'model_name': PIPELINE_NAME.replace('-','_'),  # '-' is not allowed.
#     'project_id': GOOGLE_CLOUD_PROJECT,
#     # The region to use when serving the model. See available regions here:
#     # https://cloud.google.com/ml-engine/docs/regions
#     # Note that serving currently only supports a single region:
#     # https://cloud.google.com/ml-engine/reference/rest/v1/projects.models#Model  # pylint: disable=line-too-long
#     'regions': [GOOGLE_CLOUD_REGION],
# }
