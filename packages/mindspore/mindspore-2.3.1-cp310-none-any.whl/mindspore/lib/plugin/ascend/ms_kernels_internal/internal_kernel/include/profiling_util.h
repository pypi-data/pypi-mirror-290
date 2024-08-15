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

#ifndef _PROFILING_UTIL_H_
#define _PROFILING_UTIL_H_

#include <string>
#include <vector>
#include <map>
#include "include/types.h"

namespace mindspore {
namespace internal {
// rts_msprof
#if defined(__cplusplus)
extern "C" {
#endif
#if (defined(_WIN32) || defined(_WIN64) || defined(_MSC_VER))
#define MSVP_PROF_API __declspec(dllexport)
#else
#define MSVP_PROF_API __attribute__((visibility("default")))
#endif
#define MSPROF_REPORT_DATA_MAGIC_NUM 0x5A5AU
#define MSPROF_TASK_TIME_L0 0x00000800ULL  // mean PROF_TASK_TIME
#define MSPROF_EVENT_FLAG 0xFFFFFFFFFFFFFFFFULL
typedef void *VOID_PTR;
typedef int32_t (*ProfCommandHandle)(uint32_t type, VOID_PTR data, uint32_t len);
typedef int32_t (*MsprofReportHandle)(uint32_t moduleId, uint32_t type, VOID_PTR data, uint32_t len);
typedef int32_t (*MsprofCtrlHandle)(uint32_t type, VOID_PTR data, uint32_t len);
typedef int32_t (*MsprofSetDeviceHandle)(VOID_PTR data, uint32_t len);
typedef int32_t (*AicpuStartFunc)();

/* Msprof report level */
#define MSPROF_REPORT_PYTORCH_LEVEL 30000U
#define MSPROF_REPORT_PTA_LEVEL 25000U
#define MSPROF_REPORT_ACL_LEVEL 20000U
#define MSPROF_REPORT_MODEL_LEVEL 15000U
#define MSPROF_REPORT_NODE_LEVEL 10000U
#define MSPROF_REPORT_AICPU_LEVEL 6000U
#define MSPROF_REPORT_HCCL_NODE_LEVEL 5500U
#define MSPROF_REPORT_RUNTIME_LEVEL 5000U

/* Msprof report type of acl(20000) level(acl), offset: 0x000000 */
#define MSPROF_REPORT_ACL_OP_BASE_TYPE 0x010000U
#define MSPROF_REPORT_ACL_MODEL_BASE_TYPE 0x020000U
#define MSPROF_REPORT_ACL_RUNTIME_BASE_TYPE 0x030000U
#define MSPROF_REPORT_ACL_OTHERS_BASE_TYPE 0x040000U

/* Msprof report type of acl(20000) level(host api), offset: 0x050000 */
#define MSPROF_REPORT_ACL_NN_BASE_TYPE 0x050000U
#define MSPROF_REPORT_ACL_ASCENDC_TYPE 0x060000U
#define MSPROF_REPORT_ACL_HOST_HCCL_BASE_TYPE 0x070000U
#define MSPROF_REPORT_ACL_DVPP_BASE_TYPE 0x090000U
#define MSPROF_REPORT_ACL_GRAPH_BASE_TYPE 0x0A0000U

/* Msprof report type of model(15000) level, offset: 0x000000 */
#define MSPROF_REPORT_MODEL_GRAPH_ID_MAP_TYPE 0U      /* type info: graph_id_map */
#define MSPROF_REPORT_MODEL_EXECUTE_TYPE 1U           /* type info: execute */
#define MSPROF_REPORT_MODEL_LOAD_TYPE 2U              /* type info: load */
#define MSPROF_REPORT_MODEL_INPUT_COPY_TYPE 3U        /* type info: IntputCopy */
#define MSPROF_REPORT_MODEL_OUTPUT_COPY_TYPE 4U       /* type info: OutputCopy */
#define MSPROF_REPORT_MODEL_LOGIC_STREAM_TYPE 7U      /* type info: logic_stream_info */
#define MSPROF_REPORT_MODEL_EXEOM_TYPE 8U             /* type info: exeom */
#define MSPROF_REPORT_MODEL_UDF_BASE_TYPE 0x010000U   /* type info: udf_info */
#define MSPROF_REPORT_MODEL_AICPU_BASE_TYPE 0x020000U /* type info: aicpu */

/* Msprof report type of node(10000) level, offset: 0x000000 */
#define MSPROF_REPORT_NODE_BASIC_INFO_TYPE 0U      /* type info: node_basic_info */
#define MSPROF_REPORT_NODE_TENSOR_INFO_TYPE 1U     /* type info: tensor_info */
#define MSPROF_REPORT_NODE_FUSION_OP_INFO_TYPE 2U  /* type info: funsion_op_info */
#define MSPROF_REPORT_NODE_CONTEXT_ID_INFO_TYPE 4U /* type info: context_id_info */
#define MSPROF_REPORT_NODE_LAUNCH_TYPE 5U          /* type info: launch */
#define MSPROF_REPORT_NODE_TASK_MEMORY_TYPE 6U     /* type info: task_memory_info */
#define MSPROF_REPORT_NODE_HOST_OP_EXEC_TYPE 8U    /* type info: op exec */
#define MSPROF_REPORT_NODE_ATTR_INFO_TYPE 9U       /* type info: node_attr_info */

#define MSPROF_GE_TENSOR_DATA_RESERVE_BYTES 8
#define MSPROF_GE_TENSOR_DATA_SHAPE_LEN 8
#define MSPROF_GE_TENSOR_DATA_NUM 5

enum MsprofErrorCode {
  MSPROF_ERROR_NONE = 0,
  MSPROF_ERROR_MEM_NOT_ENOUGH,
  MSPROF_ERROR_GET_ENV,
  MSPROF_ERROR_CONFIG_INVALID,
  MSPROF_ERROR_ACL_JSON_OFF,
  MSPROF_ERROR,
  MSPROF_ERROR_UNINITIALIZE,
};

enum MsprofGeTensorType {
  MSPROF_GE_TENSOR_TYPE_INPUT = 0,
  MSPROF_GE_TENSOR_TYPE_OUTPUT,
};
const uint32_t MSPROF_DIFFERENCE = 200;

#pragma pack(1)
struct MsprofNodeBasicInfo {
  uint64_t opName;
  uint32_t taskType;
  uint64_t opType;
  uint32_t blockDim;
  uint32_t opFlag;
};
struct MsrofTensorData {
  uint32_t tensorType;
  uint32_t format;
  uint32_t dataType;
  uint32_t shape[MSPROF_GE_TENSOR_DATA_SHAPE_LEN];
};

struct MsprofTensorInfo {
  uint64_t opName;
  uint32_t tensorNum;
  struct MsrofTensorData tensorData[MSPROF_GE_TENSOR_DATA_NUM];
};
#pragma pack()

struct MsprofApi {  // for MsprofReportApi
#ifdef __cplusplus
  uint16_t magicNumber = MSPROF_REPORT_DATA_MAGIC_NUM;
#else
  uint16_t magicNumber;
#endif
  uint16_t level;
  uint32_t type;
  uint32_t threadId;
  uint32_t reserve;
  uint64_t beginTime;
  uint64_t endTime;
  uint64_t itemId;
};

struct MsprofEvent {  // for MsprofReportEvent
#ifdef __cplusplus
  uint16_t magicNumber = MSPROF_REPORT_DATA_MAGIC_NUM;
#else
  uint16_t magicNumber;
#endif
  uint16_t level;
  uint32_t type;
  uint32_t threadId;
  uint32_t requestId;  // 0xFFFF means single event
  uint64_t timeStamp;
#ifdef __cplusplus
  uint64_t eventFlag = MSPROF_EVENT_FLAG;
#else
  uint64_t eventFlag;
#endif
  uint64_t itemId;
};

struct MsprofRuntimeTrack {  // for MsprofReportCompactInfo buffer data
  uint16_t deviceId;
  uint16_t streamId;
  uint32_t taskId;
  uint64_t taskType;  // task message hash id
};

#define MSPROF_COMPACT_INFO_DATA_LENGTH (40)
struct MsprofCompactInfo {  // for MsprofReportCompactInfo buffer data
#ifdef __cplusplus
  uint16_t magicNumber = MSPROF_REPORT_DATA_MAGIC_NUM;
#else
  uint16_t magicNumber;
#endif
  uint16_t level;
  uint32_t type;
  uint32_t threadId;
  uint32_t dataLen;
  uint64_t timeStamp;
  union {
    uint8_t info[MSPROF_COMPACT_INFO_DATA_LENGTH];
    struct MsprofRuntimeTrack runtimeTrack;
    struct MsprofNodeBasicInfo nodeBasicInfo;
  } data;
};

#define MSPROF_ADDTIONAL_INFO_DATA_LENGTH (232)
struct MsprofAdditionalInfo {  // for MsprofReportAdditionalInfo buffer data
#ifdef __cplusplus
  uint16_t magicNumber = MSPROF_REPORT_DATA_MAGIC_NUM;
#else
  uint16_t magicNumber;
#endif
  uint16_t level;
  uint32_t type;
  uint32_t threadId;
  uint32_t dataLen;
  uint64_t timeStamp;
  uint8_t data[MSPROF_ADDTIONAL_INFO_DATA_LENGTH];
};
#if defined(__cplusplus)
}
#endif

struct TensorInfoWrapper {
  MsprofAdditionalInfo tensor_info;
  uint64_t tensor_num;
};

struct ProfNodeAdditionInfo {
  MsprofCompactInfo node_basic_info;
  std::vector<TensorInfoWrapper> tensor_info_wrappers;
  MsprofApi api;
};

// format
constexpr auto kOpFormat_DEFAULT = "DefaultFormat";
constexpr auto kOpFormat_ChannelFirst = "ChannelFirst";
constexpr auto kOpFormat_ChannelLast = "ChannelLast";
constexpr auto kOpFormat_NC1KHKWHWC0 = "NC1KHKWHWC0";
constexpr auto kOpFormat_ND = "ND";
constexpr auto kOpFormat_NCHW = "NCHW";
constexpr auto kOpFormat_NHWC = "NHWC";
constexpr auto kOpFormat_HWCN = "HWCN";
constexpr auto kOpFormat_CHWN = "CHWN";
constexpr auto kOpFormat_NC1HWC0 = "NC1HWC0";
constexpr auto kOpFormat_FRAC_Z = "FRACTAL_Z";
constexpr auto kOpFormat_FRACTAL_Z = "FRACTAL_Z";
constexpr auto kOpFormat_FRAC_NZ = "FRACTAL_NZ";
constexpr auto kOpFormat_C1HWNCoC0 = "C1HWNCoC0";
constexpr auto kOpFormat_NC1HWC0_C04 = "NC1HWC0_C04";
constexpr auto kOpFormat_FRACTAL_Z_C04 = "FRACTAL_Z_C04";
constexpr auto kOpFormat_NDHWC = "NDHWC";
constexpr auto kOpFormat_NCDHW = "NCDHW";
constexpr auto kOpFormat_DHWNC = "DHWNC";
constexpr auto kOpFormat_DHWCN = "DHWCN";
constexpr auto kOpFormat_NDC1HWC0 = "NDC1HWC0";
constexpr auto kOpFormat_FRACTAL_Z_3D = "FRACTAL_Z_3D";
constexpr auto kOpFormat_FRACTAL_ZN_LSTM = "FRACTAL_ZN_LSTM";
constexpr auto kOpFormat_FRACTAL_ZN_RNN = "FRACTAL_ZN_RNN";
constexpr auto kOpFormat_ND_RNN_BIAS = "ND_RNN_BIAS";

// 0 means unknown format
static std::map<std::string, uint32_t> OpFormat2Index{{kOpFormat_DEFAULT, 1},
                                                      {kOpFormat_NC1KHKWHWC0, 2},
                                                      {kOpFormat_ND, 3},
                                                      {kOpFormat_NCHW, 4},
                                                      {kOpFormat_NHWC, 5},
                                                      {kOpFormat_HWCN, 6},
                                                      {kOpFormat_NC1HWC0, 7},
                                                      {kOpFormat_FRAC_Z, 8},
                                                      {kOpFormat_C1HWNCoC0, 9},
                                                      {kOpFormat_FRAC_NZ, 10},
                                                      {kOpFormat_NC1HWC0_C04, 11},
                                                      {kOpFormat_FRACTAL_Z_C04, 12},
                                                      {kOpFormat_NDHWC, 13},
                                                      {kOpFormat_FRACTAL_ZN_LSTM, 14},
                                                      {kOpFormat_FRACTAL_ZN_RNN, 15},
                                                      {kOpFormat_ND_RNN_BIAS, 16},
                                                      {kOpFormat_NDC1HWC0, 17},
                                                      {kOpFormat_NCDHW, 18},
                                                      {kOpFormat_FRACTAL_Z_3D, 19},
                                                      {kOpFormat_DHWNC, 20},
                                                      {kOpFormat_DHWCN, 21}};

static const std::string UNKNOWN_STR = "UNKNOWN_";
static const std::map<int, std::string> MAP_FORMAT_TO_STRING_V2 = {
  {TensorFormat::TENSOR_FORMAT_NCHW, "NCHW"},
  {TensorFormat::TENSOR_FORMAT_NHWC, "NHWC"},
  {TensorFormat::TENSOR_FORMAT_ND, "ND"},
  {TensorFormat::TENSOR_FORMAT_NC1HWC0, "NC1HWC0"},
  {TensorFormat::TENSOR_FORMAT_FRACTAL_Z, "FRACTAL_Z"},
  {TensorFormat::TENSOR_FORMAT_NC1HWC0_C04, "NC1HWC0_C04"},
  {TensorFormat::TENSOR_FORMAT_HWCN, "HWCN"},
  {TensorFormat::TENSOR_FORMAT_NDHWC, "NDHWC"},
  {TensorFormat::TENSOR_FORMAT_FRACTAL_NZ, "FRACTAL_NZ"},
  {TensorFormat::TENSOR_FORMAT_NCDHW, "NCDHW"},
  {TensorFormat::TENSOR_FORMAT_NDC1HWC0, "NDC1HWC0"},
  {TensorFormat::TENSOR_FORMAT_FRACTAL_Z_3D, "FRACTAL_Z_3D"},
};
const std::string &GetStrWithFormatV2(const int &format);

static const int UNKNOWN_DTYPE = 0;
enum TensorDtypeMs : int {
  kTypeUnknown = 0,
  kObjectTypeString = 12,
  kObjectTypeList = 13,
  kObjectTypeTuple = 14,
  kObjectTypeTensorType = 17,
  kNumberTypeBegin = 29,
  kNumberTypeBool = 30,
  kNumberTypeInt8 = 32,
  kNumberTypeInt16 = 33,
  kNumberTypeInt32 = 34,
  kNumberTypeInt64 = 35,
  kNumberTypeUInt8 = 37,
  kNumberTypeUInt16 = 38,
  kNumberTypeUInt32 = 39,
  kNumberTypeUInt64 = 40,
  kNumberTypeFloat16 = 42,
  kNumberTypeFloat32 = 43,
  kNumberTypeFloat64 = 44,
  kNumberTypeBFloat16 = 45,
  kNumberTypeComplex64 = 48,
  kNumberTypeComplex128 = 49,
};
static const std::map<int, int> MAP_DTYPE_TO_MSDTYPE = {
  {TensorDType::TENSOR_DTYPE_UNDEFINED, kTypeUnknown},
  {TensorDType::TENSOR_DTYPE_FLOAT, kNumberTypeFloat32},
  {TensorDType::TENSOR_DTYPE_FLOAT16, kNumberTypeFloat16},
  {TensorDType::TENSOR_DTYPE_INT8, kNumberTypeInt8},
  {TensorDType::TENSOR_DTYPE_INT32, kNumberTypeInt32},
  {TensorDType::TENSOR_DTYPE_UINT8, kNumberTypeUInt8},
  {TensorDType::TENSOR_DTYPE_INT16, kNumberTypeInt16},
  {TensorDType::TENSOR_DTYPE_UINT16, kNumberTypeUInt16},
  {TensorDType::TENSOR_DTYPE_UINT32, kNumberTypeUInt32},
  {TensorDType::TENSOR_DTYPE_INT64, kNumberTypeInt64},
  {TensorDType::TENSOR_DTYPE_UINT64, kNumberTypeUInt64},
  {TensorDType::TENSOR_DTYPE_DOUBLE, kNumberTypeFloat64},
  {TensorDType::TENSOR_DTYPE_BOOL, kNumberTypeBool},
  {TensorDType::TENSOR_DTYPE_STRING, kObjectTypeString},
  {TensorDType::TENSOR_DTYPE_COMPLEX64, kNumberTypeComplex64},
  {TensorDType::TENSOR_DTYPE_COMPLEX128, kNumberTypeComplex128},
  {TensorDType::TENSOR_DTYPE_BF16, kNumberTypeBFloat16},
};
const int &GetMsDtype(const int &dtype);

struct NodeInfo {
  // dataCnodeName   NodeFullnameScope
  const char *op_name;
  const char *op_fullname;
  // 使用的核数
  uint32_t block_dim;
  uint64_t input_size{0};
  uint64_t output_size{0};
  std::vector<std::vector<int64_t>> shapes;
  std::vector<std::string> data_formats;
  std::vector<uint32_t> data_types;
};

class MsProfHelper {
 public:
  MsProfHelper(const NodeInfo &info) : info_(info){};
  ~MsProfHelper() = default;

  void InitReportNode();
  void ReportTask();

 private:
  void InitProfTensorData(const size_t index, const uint64_t offset_idx, MsprofTensorInfo *tensor_info);
  void BuildSingleTensorInfo(const uint64_t opName_hash_id, const size_t index, const uint32_t tensor_num,
                             TensorInfoWrapper *tensor_info_wrapper);

  ProfNodeAdditionInfo addition_info_;
  NodeInfo info_;
};
}  // namespace internal
}  // namespace mindspore
#endif  // _PROFILING_UTIL_H_