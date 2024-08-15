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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_BACKOFF_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_BACKOFF_H_

#include <any>
#include "acme/src/ops/host_src/asd_ops.h"

namespace mindspore {
namespace acme {
class AsdBackOffKernel : public AcmeOp {
 public:
  AsdBackOffKernel(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii);
  ~AsdBackOffKernel() = default;

  AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape) override;
  void SetTilingInfo(const TilingInfoPtr &tiling_info) override;

  virtual AsdOps::Any BuildAsdParam() = 0;
  virtual bool CanAsdSupport();
  virtual bool NeedBackOff();
  virtual const std::string &TargetKernelName() const;
  virtual AsdOpPtr CreateBackOffKernel(const InputsImmutableInfoList &inputs_ii,
                                       const OutputsImmutableInfoList &outputs_ii, const AsdOps::Any &param,
                                       const std::string &kernel_name);
  
  std::string DumpTiling(const RawHostAddr host_ptr) const override;

 protected:
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;

  virtual bool NeedBackOffImpl();
  virtual AcmeStatus TilingNoBackOff(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) = 0;
  virtual AcmeStatus LaunchNoBackOff(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                                     const WsAddrList &ws_ptrs, void *stream) = 0;
  virtual std::string DumpTilingNoBackOff(const RawHostAddr host_ptr) const = 0;

 private:
  bool backoff_{false};
  AsdOpPtr asd_op_{nullptr};
};

}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_BACKOFF_H_