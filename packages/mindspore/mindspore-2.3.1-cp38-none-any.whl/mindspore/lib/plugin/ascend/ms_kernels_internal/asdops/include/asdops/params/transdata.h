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
#ifndef ASDOPS_PARAMS_TRANSDATA_H
#define ASDOPS_PARAMS_TRANSDATA_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
namespace OpParam {
struct Transdata {
    enum TransdataType { UNDEFINED = 0, FRACTAL_NZ_TO_ND, ND_TO_FRACTAL_NZ };
    TransdataType transdataType = UNDEFINED;
    SVector<int64_t> outCrops = {0, 0};
    enum SpecialType { NORMAL = 0, ATTENTION_INPUT_QKV, ATTENTION_INPUT_MASK};
    int64_t specialTransdata = NORMAL;

    bool operator==(const Transdata &other) const
    {
        return this->transdataType == other.transdataType && this->outCrops == other.outCrops;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif // ASDOPS_PARAMS_TRANSDATA_H