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

#ifndef MS_KERNELS_INTERNAL_KERNEL_MATMUL_MATMUL_STRIDEDSLICE_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_MATMUL_MATMUL_STRIDEDSLICE_IMPL_H_

#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"

#include "utils.h"
#include "backend_param.h"
#include "matmul_common/pp_matmul_info.h"
#include "matmul_common/tiling_utils.h"
#include "matmul_common/tiling_data.h"
#include "matmul_common/pp_matmul_common_tiling.h"
#include "param/matmul_qkv_param.h"
#include "tune_repo/utils.h"

#include "internal_kernel.h"

#include "acl_rt.h"
#include <unordered_map>

namespace mindspore {
namespace internal {

using namespace tiling;

enum class MultiMatMulAlgo { PP = 0, LLM_CUSTOM = 1 };
enum class MultiMatMulFusionLevel { NONE = 0, CUBE = 1, MIX= 2 };

class MatMulStridedSliceFusionImpl : public InternelKernelImpl {
 public:
  MatMulStridedSliceFusionImpl(const OpParamPtr &param) : InternelKernelImpl(param){};
  virtual ~MatMulStridedSliceFusionImpl() = default;
  bool Init(const ValidateInfo &info) override;
  void RegsiterCceKernels();
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  int LaunchMix();
  size_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  void TilingBasicFromPp(uint32_t &blockDim, PpTilingData &tilingdata);
  int TilingPp(HostRawBuf &tilingBuf, uint32_t tilingId, const uint32_t &blockDim, const PpTilingData &tilingdata);
  int TilingLLMCustom(HostRawBuf &tilingBuf, uint32_t tilingId, const uint32_t &blockDim,
                      const PpTilingData &tilingdata);
  void SetWorkSpace(const std::vector<DeviceRawBuf> &workspace) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;
  bool GenTilingId(uint32_t &tiling_id);
  void GetTunedKey();
  bool GetPpMatmulTiling(const MatMulInfo &mmInfo, const HardwareInfo &hwInfo_, uint32_t &blockDim,
                         PpTilingData &tilingData);
  uint32_t MixSwizzle(PpTilingData &tilingData);

 private:
  std::string soc_{"Ascend910B2"};
  HardwareInfo hwInfo_;
  uint32_t m_, k_, n0_, n1_, n2_;
  const char *func_name_ = "UnknownFunc";
  DeviceRawBuf tiling_addr_;
  TensorDType input_dtype_;
  TensorDType output_dtype_;
  int block_dim_ = 0;
  bool trans_a_{false};
  bool trans_b_{true};
  std::vector<int> tune_key_;
  MultiMatMulAlgo algo_ = MultiMatMulAlgo::PP;
  MultiMatMulFusionLevel fusion_level_ = MultiMatMulFusionLevel::NONE;
  int32_t silu_position_{-1};
  uint32_t fusion_type_{0};

  REPO tuningTable_;
  static bool _is_inited;
  void *workspace_addr = nullptr;
  // static std::unordered_map<const char *, const char *> internal_multi_matmul_kernels_map;
};

}  // namespace internal
}  // namespace mindspore
#endif
