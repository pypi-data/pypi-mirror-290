#  Copyright (c) Huawei Technologies Co., Ltd. 2024-2024. All rights reserved.
import os
from pathlib import Path

import evaluate
from evaluate import config

import openmind_evaluate.patches.file_utils
import openmind_evaluate.patches.loading


def apply_config_patch():
    # Hub
    config.HF_ENDPOINT = os.environ.get("OPENMIND_HUB_ENDPOINT", "https://telecom.openmind.cn")
    config.HF_LIST_ENDPOINT = config.HF_ENDPOINT + "/api/spaces?filter={type}"
    config.HUB_EVALUATE_URL = config.HF_ENDPOINT + "/spaces/{path}/resolve/{revision}/{name}"

    # Metrics
    config.CLOUDFRONT_METRICS_DISTRIB_PREFIX = os.environ.get("OPENMIND_HUB_ENDPOINT", "https://telecom.openmind.cn")
    config.REPO_METRICS_URL = os.environ.get("OPENMIND_HUB_ENDPOINT", "https://telecom.openmind.cn")
    config.REPO_MEASUREMENTS_URL = os.environ.get("OPENMIND_HUB_ENDPOINT", "https://telecom.openmind.cn")
    config.REPO_COMPARISONS_URL = os.environ.get("OPENMIND_HUB_ENDPOINT", "https://telecom.openmind.cn")

    # Cache location
    config.DEFAULT_HF_CACHE_HOME = os.path.join(config.XDG_CACHE_HOME, "openmind")
    config.HF_CACHE_HOME = os.path.expanduser(os.getenv("HF_HOME", config.DEFAULT_HF_CACHE_HOME))

    config.DEFAULT_HF_EVALUATE_CACHE = os.path.join(config.HF_CACHE_HOME, "evaluate")
    config.HF_EVALUATE_CACHE = Path(os.getenv("HF_EVALUATE_CACHE", config.DEFAULT_HF_EVALUATE_CACHE))

    config.DEFAULT_HF_METRICS_CACHE = os.path.join(config.HF_CACHE_HOME, "metrics")
    config.HF_METRICS_CACHE = Path(os.getenv("HF_METRICS_CACHE", config.DEFAULT_HF_METRICS_CACHE))

    config.DEFAULT_HF_MODULES_CACHE = os.path.join(config.HF_CACHE_HOME, "modules")
    config.HF_MODULES_CACHE = Path(os.getenv("HF_MODULES_CACHE", config.DEFAULT_HF_MODULES_CACHE))

    config.DEFAULT_DOWNLOADED_EVALUATE_PATH = os.path.join(config.HF_EVALUATE_CACHE, config.DOWNLOADED_DATASETS_DIR)
    config.DOWNLOADED_EVALUATE_PATH = Path(
        os.getenv("HF_DATASETS_DOWNLOADED_EVALUATE_PATH", config.DEFAULT_DOWNLOADED_EVALUATE_PATH))

    config.DEFAULT_EXTRACTED_EVALUATE_PATH = os.path.join(config.DEFAULT_DOWNLOADED_EVALUATE_PATH,
                                                          config.EXTRACTED_EVALUATE_DIR)
    config.EXTRACTED_EVALUATE_PATH = Path(
        os.getenv("HF_DATASETS_EXTRACTED_EVALUATE_PATH", config.DEFAULT_EXTRACTED_EVALUATE_PATH))


def evaluate_adaptation():
    evaluate.loading.HubEvaluationModuleFactory.download_loading_script = \
        openmind_evaluate.patches.loading.download_loading_scripts_path_patch
    evaluate.loading.HubEvaluationModuleFactory.get_module = openmind_evaluate.patches.loading.get_module_patch
    evaluate.loading.evaluation_module_factory = openmind_evaluate.patches.loading.evaluation_module_factory_patch
    evaluate.utils.file_utils._request_with_retry = openmind_evaluate.patches.file_utils.request_with_retry_wrapper(
        evaluate.utils.file_utils._request_with_retry)
    evaluate.utils.file_utils.get_authentication_headers_for_url = \
        openmind_evaluate.patches.file_utils.get_authentication_headers_for_url_wrapper(
            evaluate.utils.file_utils.get_authentication_headers_for_url)


def exe_adaptation():
    apply_config_patch()
    evaluate_adaptation()


exe_adaptation()
