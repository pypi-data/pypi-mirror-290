# Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
# Copyright 2022 The HuggingFace Team. All rights reserved.
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

import importlib
import os
import re
from dataclasses import dataclass
from typing import Optional, Union

from datasets import DownloadConfig, DownloadMode
from datasets.utils.version import Version
from evaluate import SCRIPTS_VERSION
from evaluate.utils.file_utils import (
    cached_path,
    is_relative_path,
)
from evaluate.loading import get_imports, _download_additional_modules, init_dynamic_modules, _create_importable_file, \
    LocalEvaluationModuleFactory, HubEvaluationModuleFactory, CachedEvaluationModuleFactory
from openmind_hub import om_hub_url
from openmind_hub import OMValidationError


@dataclass
class ImportableModule:
    module_path: str
    hash: str


def download_loading_scripts_path_patch(self, revision) -> str:
    file_path = om_hub_url(repo_id=self.name, filename=self.name.split("/")[1] + ".py", revision=revision)
    download_config = self.download_config.copy()
    if download_config.download_desc is None:
        download_config.download_desc = "Downloading builder script"
    return cached_path(file_path, download_config=download_config)


def get_module_patch(self) -> ImportableModule:
    revision = self.revision or os.getenv("HF_SCRIPTS_VERSION", 'main')
    if re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}",
                revision):  # revision is version number (three digits separated by full stops)
        revision = "v" + revision  # tagging convention on evaluate repository starts with v
    # get script and other files
    try:
        local_path = self.download_loading_script(revision)
    except (FileNotFoundError, OMValidationError) as err:
        # if there is no file found with current revision tag try to load main
        if self.revision is None and os.getenv("HF_SCRIPTS_VERSION", SCRIPTS_VERSION) != "main":
            revision = "main"
            local_path = self.download_loading_script(revision)
        else:
            raise err
    imports = get_imports(local_path)
    local_imports = _download_additional_modules(
        name=self.name,
        base_path=om_hub_url(repo_id=self.name, filename="", revision=revision),
        imports=imports,
        download_config=self.download_config,
    )
    # copy the script and the files in an importable directory
    dynamic_modules_path = self.dynamic_modules_path if self.dynamic_modules_path else init_dynamic_modules()
    module_path, hash = _create_importable_file(
        local_path=local_path,
        local_imports=local_imports,
        additional_files=[],
        dynamic_modules_path=dynamic_modules_path,
        module_namespace=self.module_type,
        name=self.name,
        download_mode=self.download_mode,
    )
    # make the new module to be noticed by the import system
    importlib.invalidate_caches()
    return ImportableModule(module_path, hash)


def evaluation_module_factory_patch(
        path: str,
        module_type: Optional[str] = None,
        revision: Optional[Union[str, Version]] = None,
        download_config: Optional[DownloadConfig] = None,
        download_mode: Optional[DownloadMode] = None,
        force_local_path: Optional[str] = None,
        dynamic_modules_path: Optional[str] = None,
        **download_kwargs,
) -> ImportableModule:
    if download_config is None:
        download_config = DownloadConfig(**download_kwargs)
    download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)
    download_config.extract_compressed_file = True
    download_config.force_extract = True

    filename = list(filter(lambda x: x, path.replace(os.sep, "/").split("/")))[-1]
    if not filename.endswith(".py"):
        filename = filename + ".py"
    combined_path = os.path.join(path, filename)
    # Try locally
    if path.endswith(filename):
        if os.path.isfile(path):
            return LocalEvaluationModuleFactory(
                path, download_mode=download_mode, dynamic_modules_path=dynamic_modules_path
            ).get_module()
        else:
            raise FileNotFoundError(f"Couldn't find a metric script in the local path.")
    elif os.path.isfile(combined_path):
        return LocalEvaluationModuleFactory(
            combined_path, download_mode=download_mode, dynamic_modules_path=dynamic_modules_path
        ).get_module()
    elif is_relative_path(path) and path.count("/") <= 1 and not force_local_path:
        try:
            # load a canonical evaluation module from hub
            if path.count("/") == 0:
                # if no type provided look through all possible modules
                if module_type is None:
                    for current_type in ["metric", "comparison", "measurement"]:
                        try:
                            return HubEvaluationModuleFactory(
                                f"evaluate-{current_type}/{path}",
                                revision=revision,
                                download_config=download_config,
                                download_mode=download_mode,
                                dynamic_modules_path=dynamic_modules_path,
                            ).get_module()
                        except (ConnectionError, FileNotFoundError):
                            pass
                    raise FileNotFoundError
                # if module_type provided load specific module_type
                else:
                    return HubEvaluationModuleFactory(
                        f"evaluate-{module_type}/{path}",
                        revision=revision,
                        download_config=download_config,
                        download_mode=download_mode,
                        dynamic_modules_path=dynamic_modules_path,
                    ).get_module()
            # load community evaluation module from hub
            elif path.count("/") == 1:
                return HubEvaluationModuleFactory(
                    path,
                    revision=revision,
                    download_config=download_config,
                    download_mode=download_mode,
                    dynamic_modules_path=dynamic_modules_path,
                ).get_module()
        except Exception as e1:  # noqa: all the attempts failed, before raising the error we should check if the module is already cached.
            # if it's a canonical module we need to check if it's any of the types
            if path.count("/") == 0:
                for current_type in ["metric", "comparison", "measurement"]:
                    try:
                        return CachedEvaluationModuleFactory(
                            f"evaluate-{current_type}--{path}", dynamic_modules_path=dynamic_modules_path
                        ).get_module()
                    except Exception as e2:  # noqa: if it's not in the cache, then it doesn't exist.
                        pass
            # if it's a community module we just need to check on path
            elif path.count("/") == 1:
                try:
                    return CachedEvaluationModuleFactory(
                        path.replace("/", "--"), dynamic_modules_path=dynamic_modules_path
                    ).get_module()
                except Exception as e2:  # noqa: if it's not in the cache, then it doesn't exist.
                    pass
            if not isinstance(e1, (ConnectionError, FileNotFoundError)):
                raise e1 from None
            raise FileNotFoundError(
                f"Couldn't find a module script in the local path."
                f"Module doesn't exist on the Openmind Hub either."
            ) from None
    else:
        raise FileNotFoundError(f"Couldn't find a module script in the local path.")
