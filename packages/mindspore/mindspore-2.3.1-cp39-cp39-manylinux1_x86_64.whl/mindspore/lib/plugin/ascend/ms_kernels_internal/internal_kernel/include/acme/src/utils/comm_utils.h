/**
 * Copyright 2024 Huawei Technologies Co., Ltd
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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_COMM_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_COMM_UTILS_H_

#include <unordered_map>
#include "acme/include/base_type.h"
#include "utils/log/log.h"

#define CeilDiv(dividend, divisor) (((divisor) == 0) ? 0 : (((dividend) + (divisor)-1) / (divisor)))
#define UpRound(in, round) ((((in) + (round)-1) / (round)) * (round))

namespace mindspore {
namespace acme {
inline size_t GetTypeSize(DataType type) {
  static const std::unordered_map<DataType, size_t> kTypeSize = {
    {kTypeFloat16, sizeof(float) / 2},
    {kTypeFloat32, sizeof(float)},
    {kTypeFloat64, sizeof(double)},
    {kTypeInt8, sizeof(int8_t)},
    {kTypeInt16, sizeof(int16_t)},
    {kTypeInt32, sizeof(int32_t)},
    {kTypeInt64, sizeof(int64_t)},
    {kTypeUint8, sizeof(uint8_t)},
    {kTypeUint16, sizeof(uint16_t)},
    {kTypeUint32, sizeof(uint32_t)},
    {kTypeUint64, sizeof(uint64_t)},
    {kTypeBF16, sizeof(float) / 2},
    {kTypeBool, sizeof(bool)},
    {kTypeComplex64, 64},
    {kTypeComplex128, 128},
  };

  auto it = kTypeSize.find(type);
  if (it == kTypeSize.end()) {
    MSOP_LOG(EXCEPTION) << "Unsupported type: " << type;
    return 0;
  }

  return it->second;
}

bool IsOpEnabled(const std::string &op_name);
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_COMM_UTILS_H_