/**
 * Copyright 2023-2024 Huawei Technologies Co., Ltd
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
#ifndef MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_UTILS_H_
#include <iostream>
#include <map>
#include "include/op_param.h"
#include "utils/utils.h"

namespace mindspore::internal {
static std::ostream &operator<<(std::ostream &os, const OpParam &param) {
  os << "[" << OpIdToString(param.opId) << "]";
  os << ", in dtypes: ";
  for (size_t i = 0; i < param.in_dtypes_.size(); i++) {
    os << " " << param.in_dtypes_[i];
  }
  os << "; out dtypes: ";
  for (size_t i = 0; i < param.out_dtypes_.size(); i++) {
    os << " " << param.out_dtypes_[i];
  }
  return os;
}

static std::ostream &operator<<(std::ostream &os, const DtypesParam &param) {
  os << "[" << OpIdToString(param.op_id_) << "]";
  os << ", in dtypes: ";
  for (size_t i = 0; i < param.in_dtypes_.size(); i++) {
    os << " " << param.in_dtypes_[i];
  }
  os << "; out dtypes: ";
  for (size_t i = 0; i < param.out_dtypes_.size(); i++) {
    os << " " << param.out_dtypes_[i];
  }
  return os;
}

static std::ostream &operator<<(
  std::ostream &os,
  const std::vector<std::pair<std::vector<TensorDType>, std::vector<TensorDType>>> &support_dtype_list) {
  for (auto dtyp : support_dtype_list) {
    auto ins = dtyp.first;
    auto outs = dtyp.second;
    os << "(";
    for (size_t i = 0; i < ins.size(); i++) {
      os << ins[i] << " ";
    }
    os << ",";
    for (size_t i = 0; i < outs.size(); i++) {
      os << outs[i] << " ";
    }
    os << ")";
  }
  return os;
}
}  // namespace mindspore::internal
#endif  //    MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_UTILS_H_
