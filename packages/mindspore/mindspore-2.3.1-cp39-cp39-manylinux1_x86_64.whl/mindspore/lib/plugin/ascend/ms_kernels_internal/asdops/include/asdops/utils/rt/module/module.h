/**
 * Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef COMMON_RT_MODULE_MODULE_H
#define COMMON_RT_MODULE_MODULE_H

#include "asdops/utils/rt/base/types.h"

#ifdef __cplusplus
extern "C" {
#endif
namespace AsdOps {
int AsdRtModuleCreate(AsdRtModuleInfo *moduleInfo, AsdRtModule *module);
int AsdRtModuleCreateFromFile(const char *moduleFilePath, AsdRtModuleType type, int version, AsdRtModule *module);
int AsdRtModuleDestory(AsdRtModule *module);
int AsdRtModuleBindFunction(AsdRtModule module, const char *funcName, void *func);
int AstRtRegisterAllFunction(AsdRtModuleInfo *moduleInfo, void **handle);
int AsdRtFunctionLaunch(const void *func, const AsdRtKernelParam *launchParam, AsdRtStream stream);
int AsdRtFunctionLaunchWithHandle(void *handle, const AsdRtKernelParam *launchParam, AsdRtStream stream,
    const RtTaskCfgInfoT *cfgInfo);
int AsdRtFunctionLaunchWithFlag(const void *func, const AsdRtKernelParam *launchParam, AsdRtStream stream,
    const RtTaskCfgInfoT *cfgInfo);
}
#ifdef __cplusplus
}
#endif
#endif