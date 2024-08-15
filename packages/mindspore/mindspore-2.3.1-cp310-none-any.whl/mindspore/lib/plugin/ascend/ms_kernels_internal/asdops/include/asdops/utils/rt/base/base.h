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
#ifndef COMMON_RT_BASE_BASE_H
#define COMMON_RT_BASE_BASE_H
#include "asdops/utils/rt/base/types.h"

#ifdef __cplusplus
extern "C" {
#endif
namespace AsdOps {
void AsdRtGetVersion(int &major, int &min, int &patch);
const char *AsdRtGetBuildInfo(void);
const char *AsdRtErrorName(int error);
const char *AsdRtErrorDesc(int error);
}
#ifdef __cplusplus
}
#endif
#endif