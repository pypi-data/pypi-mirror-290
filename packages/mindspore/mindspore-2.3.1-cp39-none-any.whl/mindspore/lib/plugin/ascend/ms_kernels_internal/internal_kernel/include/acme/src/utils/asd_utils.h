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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ASD_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ASD_UTILS_H_

#include "asdops/types.h"
#include "utils/log/log.h"
#include "acme/include/base_type.h"

namespace mindspore {
namespace acme {
inline AsdOps::TensorDType ToAsdType(DataType type) {
  switch (type) {
    // float data type
    case kTypeBF16:
      return AsdOps::TENSOR_DTYPE_BF16;
    case kTypeFloat16:
      return AsdOps::TENSOR_DTYPE_FLOAT16;
    case kTypeFloat32:
      return AsdOps::TENSOR_DTYPE_FLOAT;
    case kTypeFloat64:
      return AsdOps::TENSOR_DTYPE_DOUBLE;
    // uint data type
    case kTypeUint8:
      return AsdOps::TENSOR_DTYPE_UINT8;
    case kTypeUint16:
      return AsdOps::TENSOR_DTYPE_UINT16;
    case kTypeUint32:
      return AsdOps::TENSOR_DTYPE_UINT32;
    case kTypeUint64:
      return AsdOps::TENSOR_DTYPE_UINT64;
    // int data type
    case kTypeInt8:
      return AsdOps::TENSOR_DTYPE_INT8;
    case kTypeInt16:
      return AsdOps::TENSOR_DTYPE_INT16;
    case kTypeInt32:
      return AsdOps::TENSOR_DTYPE_INT32;
    case kTypeInt64:
      return AsdOps::TENSOR_DTYPE_INT64;
    // complex data type
    case kTypeComplex64:
      return AsdOps::TENSOR_DTYPE_COMPLEX64;
    case kTypeComplex128:
      return AsdOps::TENSOR_DTYPE_COMPLEX128;
    // other data type
    case kTypeString:
      return AsdOps::TENSOR_DTYPE_STRING;
    case kTypeBool:
      return AsdOps::TENSOR_DTYPE_BOOL;
    default:
      MSOP_LOG(EXCEPTION) << "Unsupported type: " << type;
      return AsdOps::TENSOR_DTYPE_UNDEFINED;
  }
}

inline AsdOps::TensorFormat ToAsdFormat(TensorFormat format) {
  switch (format) {
    case kFormatUnknown:
      return AsdOps::TENSOR_FORMAT_UNDEFINED;
    case kFormatNCHW:
      return AsdOps::TENSOR_FORMAT_NCHW;
    case kFormatND:
      return AsdOps::TENSOR_FORMAT_ND;
    case kFormatNHWC:
      return AsdOps::TENSOR_FORMAT_NHWC;
    default:
      MSOP_LOG(EXCEPTION) << "Unsupported format: " << format;
      return AsdOps::TENSOR_FORMAT_UNDEFINED;
  }
}

inline AsdOps::SVector<int64_t> ToAsdDims(const ShapeInfo &shape) {
  AsdOps::SVector<int64_t> asd_dims;
  for (auto s : shape) {
    asd_dims.emplace_back(s);
  }
  return asd_dims;
}

}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ASD_UTILS_H_