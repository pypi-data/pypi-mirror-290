# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

from mindspore.common import dtype as mstype
from mindspore.ops.auto_generate.pyboost_inner_prim import *


def add(input, other, alpha=1):
    r"""
    Adds scaled other value to input Tensor.
    
    .. math::
    
        out_{i} = input_{i} + alpha \times other_{i}
    
    Note:
        - When the two inputs have different shapes,
          they must be able to broadcast to a common shape.
        - The two inputs and alpha comply with the implicit type conversion rules to make the data types
          consistent.
    
    Args:
        input (Union[Tensor, number.Number, bool]): The first input is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        other (Union[Tensor, number.Number, bool]): The second input, is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        alpha (number.Number): A scaling factor applied to `other`, default 1.
    
    Returns:
        Tensor with a shape that is the same as the broadcasted shape of the input `input` and `other`,
        and the data type is the one with higher precision or higher digits among the two inputs and alpha.
    
    Raises:
        TypeError: If the type of `input`, `other`, or `alpha` is not one of the following: Tensor, number.Number, bool.
        TypeError: If `alpha` is of type float but `input` and `other` are not of type float.
        TypeError: If `alpha` is of type bool but `input` and `other` are not of type bool.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore import Tensor
        >>> from mindspore import ops
        >>> x = Tensor(1, mindspore.int32)
        >>> y = Tensor(np.array([4, 5, 6]).astype(np.float32))
        >>> alpha = 0.5
        >>> output = ops.auto_generate.add_ext(x, y, alpha)
        >>> print(output)
        [3. 3.5 4.]
        >>> # the data type of x is int32, the data type of y is float32,
        >>> # alpha is a float, and the output is the data format of higher precision float32.
        >>> print(output.dtype)
        Float32
    """
    return add_impl(input, other, alpha)


def argmax(input, dim=None, keepdim=False):
    r"""
    Return the indices of the maximum values of a tensor across a dimension.
    
    Args:
        input (Tensor): Input tensor.
        dim (Union[int, None], optional): The dimension to reduce. If `dim` is ``None`` , the indices of the maximum
            value within the flattened input will be returned. Default: ``None`` .
        keepdim (bool, optional): Whether the output tensor retains the specified
            dimension. Ignored if `dim` is None. Default: ``False`` .
    
    Returns:
        Tensor, indices of the maximum values across a dimension.
    
    Raises:
        TypeError: If `keepdim` is not bool.
        ValueError: If `dim` is out of range.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> from mindspore import ops
        >>> x = Tensor(np.array([[1, 20, 5], [67, 8, 9], [130, 24, 15]]).astype(np.float32))
        >>> output = ops.auto_generate.argmax_ext(x, dim=-1)
        >>> print(output)
        [1 0 0]
    """
    return argmax_impl(input, dim, keepdim)


def atan2(input, other):
    r"""
    Returns arctangent of input/other element-wise.
    
    It returns :math:`\theta\ \in\ [-\pi, \pi]`
    such that :math:`input = r*\sin(\theta), other = r*\cos(\theta)`, where :math:`r = \sqrt{input^2 + other^2}`.
    
    Note:
        - Arg `input` and `other` comply with the implicit type conversion rules to make the data types consistent.
          If they have different data types, the lower precision data type will be converted to relatively the
          highest precision data type.
    
    Args:
        input (Tensor, Number.number): The input tensor or scalar.
        other (Tensor, Number.number): The input tensor or scalar. It has the same shape with `input` or
            its shape is able to broadcast with `input`.
    
    Returns:
        Tensor, the shape is the same as the one after broadcasting, and the data type is same as `input`.
    
    Raises:
        TypeError: If `input` or `other` is not a Tensor or scalar.
        RuntimeError: If the data type of `input` and `other` conversion of Parameter is required
                    when data type conversion of Parameter is not supported.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> input = Tensor(np.array([0, 1]), mindspore.float32)
        >>> other = Tensor(np.array([1, 1]), mindspore.float32)
        >>> output = mint.atan2(input, other)
        >>> print(output)
        [0.        0.7853982]
    """
    return atan2_impl(input, other)


def bmm(input, mat2):
    r"""
    Performs batch matrix-matrix multiplication of two three-dimensional tensors.
    
    .. math::
        \text{output}= \text{input} @ \text{mat2}
    
    Args:
        input (Tensor): The first batch of matrices to be multiplied. Must be a three-dimensional tensor of shape `(b, n, m)`.
        mat2 (Tensor): The second batch of matrices to be multiplied. Must be a three-dimensional tensor of shape `(b, m, p)`.
    
    Returns:
        Tensor, the output tensor of shape `(b, n, p)`, where each matrix is the product of the corresponding matrices in the input batches.
    
    Raises:
        ValueError: If `input` or `mat2` is not three-dimensional tensors.
        ValueError: If the length of the third dimension of `input` is not equal to the length of the second dimension of `mat2`.
        ValueError: If the batch size of the inputs is not equal to the batch size of the mat2.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> from mindspore import ops
        >>> a = Tensor(np.ones(shape=[2, 3, 4]), mindspore.float32)
        >>> b = Tensor(np.ones(shape=[2, 4, 5]), mindspore.float32)
        >>> output = ops.auto_generate.bmm_ext(a, b)
        >>> print(output)
        [[[4. 4. 4. 4. 4.]
          [4. 4. 4. 4. 4.]
          [4. 4. 4. 4. 4.]]
         [[4. 4. 4. 4. 4.]
          [4. 4. 4. 4. 4.]
          [4. 4. 4. 4. 4.]]]
    """
    return bmm_impl(input, mat2)


def fold(input, output_size, kernel_size, dilation=1, padding=0, stride=1):
    r"""
    Combines an array of sliding local blocks into a large containing tensor.
    
    Consider a batched input tensor of shape :math:`(N, C \times \prod(\text{kernel_size}), L)` ,
    where :math:`N` is the batch dimension, :math:`C \times \prod(\text{kernel_size})` is the
    total number of values within each block (a block has :math:`\prod(\text{kernel_size})` spatial
    locations each containing a `C`-channeled vector), and :math:`L` is the total number of such blocks:
    
    .. math::
        L = \prod_d \left\lfloor\frac{\text{output_size}[d] + 2 \times \text{padding}[d] %
            - \text{dilation}[d] \times (\text{kernel_size}[d] - 1) - 1}{\text{stride}[d]} + 1\right\rfloor,
    
    where :math:`d` is over all spatial dimensions.
    
    Therefore, `output_size` is the spatial shape of the large containing tensor of the sliding local blocks.
    
    The `dilation`, `padding` and `stride` arguments specify how the sliding blocks are retrieved.
    
    .. warning::
        Currently, only unbatched(3D) or batched(4D) image-like output tensors are supported.
    
    Args:
        input (Tensor): 2-D or 3-D Tensor.
        output_size (Union[int, tuple[int], list[int]]): The shape of the spatial dimensions of
            the output(i.e., output.shape[2:]).
        kernel_size (Union[int, tuple[int], list[int]]): The size of the kernel, should be two int
            for height and width. If type is int, it means that height equal with width. Must be specified.
        dilation (Union[int, tuple[int], list[int]], optional): The size of the dilation, should be two int
            for height and width. If type is int, it means that height equal with width. Default: ``1`` .
        padding (Union[int, tuple[int], list[int]], optional): The size of the padding, should be two int
            for height and width. If type is int, it means that height equal with width. Default: ``0`` .
        stride (Union[int, tuple[int], list[int]], optional): The size of the stride, should be two int
            for height and width. If type is int, it means that height equal with width. Default: ``1`` .
    
    Returns:
        A Tensor, with same type as `input` .
    
    Shape:
        - Input: :math:`(N, C \times \prod(\text{kernel_size}), L)` or
          :math:`(C \times \prod(\text{kernel_size}), L)`
        - Output: :math:`(N, C, output\_size[0], output\_size[1], ...)` or
          :math:`(C, output\_size[0], output\_size[1], ...)`
    
    Raises:
        TypeError: If `output_size`, `kernel_size`, `stride`, `dilation`, `padding` data type is not int, tuple or list.
        ValueError: If `output_size`, `kernel_size`, `dilation`, `stride` value is not
            greater than zero or elements number invalid.
        ValueError: If `padding` value is less than zero or elements number invalid.
        ValueError: If input.shape[-2] can't be divisible by the product of kernel_size.
        ValueError: If `input.shape[-1]` is not equal to the calculated number of sliding blocks `L`.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> x = Tensor(np.random.rand(16, 64, 25).astype(np.float32))
        >>> output = ops.auto_generate.fold_ext(x, (8, 8), [2, 2], [2, 2], [2, 2], [2, 2])
        >>> print(output.shape)
        (16, 16, 8, 8)
    """
    return fold_impl(input, converted_output_size, converted_kernel_size, converted_dilation, converted_padding, converted_stride)


def cumsum(input, dim, dtype=None):
    r"""
    Computes the cumulative sum of input Tensor along `dim`.
    
    .. math::
    
        y_i = x_1 + x_2 + x_3 + ... + x_i
    
    Args:
        input (Tensor): The input Tensor.
        dim (int): Dim along which the cumulative sum is computed.
        dtype (:class:`mindspore.dtype`, optional): The desired dtype of returned Tensor. If specified,
            the input Tensor will be cast to `dtype` before the computation. This is useful for preventing overflows.
            If not specified, stay the same as original Tensor. Default: ``None`` .
    
    Returns:
        Tensor, the shape of the output Tensor is consistent with the input Tensor's.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        ValueError: If the `dim` is out of range.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import numpy as np
        >>> from mindspore import Tensor
        >>> import mindspore.ops as ops
        >>> x = Tensor(np.array([[3, 4, 6, 10], [1, 6, 7, 9], [4, 3, 8, 7], [1, 3, 7, 9]]).astype(np.float32))
        >>> # case 1: along the dim 0
        >>> y = ops.auto_generate.cumsum_ext(x, 0)
        >>> print(y)
        [[ 3.  4.  6. 10.]
        [ 4. 10. 13. 19.]
        [ 8. 13. 21. 26.]
        [ 9. 16. 28. 35.]]
        >>> # case 2: along the dim 1
        >>> y = ops.auto_generate.cumsum_ext(x, 1)
        >>> print(y)
        [[ 3.  7. 13. 23.]
        [ 1.  7. 14. 23.]
        [ 4.  7. 15. 22.]
        [ 1.  4. 11. 20.]]
    """
    return cumsum_impl(input, dim, dtype)


def elu(input, alpha=1.0):
    r"""
    Exponential Linear Unit activation function.
    
    Applies the exponential linear unit function element-wise.
    The activation function is defined as:
    
    .. math::
    
        \text{ELU}(x)= \left\{
        \begin{array}{align}
            \alpha(e^{x}  - 1) & \text{if } x \le 0\\
            x & \text{if } x \gt 0\\
        \end{array}\right.
    
    Where :math:`x` is the element of input Tensor `input`, :math:`\alpha` is param `alpha`,
    it determines the smoothness of ELU.
    
    ELU function graph:
    
    .. image:: ../images/ELU.png
        :align: center
    
    Args:
        input (Tensor): The input of ELU is a Tensor of any dimension.
        alpha (float, optional): The alpha value of ELU, the data type is float.
            Default: ``1.0`` .
    
    Returns:
        Tensor, has the same shape and data type as `input`.
    
    Raises:
        TypeError: If `alpha` is not a float.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> x = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> output = ops.auto_generate.elu_ext(x)
        >>> print(output)
        [[-0.63212055  4.         -0.99966455]
         [ 2.         -0.99326205  9.        ]]
    """
    return elu_impl(input, alpha)


def ffn(x, weight1, weight2, expertTokens=None, bias1=None, bias2=None, scale=None, offset=None, deqScale1=None, deqScale2=None, antiquant_scale1=None, antiquant_scale2=None, antiquant_offset1=None, antiquant_offset2=None, activation='fastgelu', inner_precise=0):
    r"""
    None
    """
    return ffn_impl(x, weight1, weight2, expertTokens, bias1, bias2, scale, offset, deqScale1, deqScale2, antiquant_scale1, antiquant_scale2, antiquant_offset1, antiquant_offset2, converted_activation, inner_precise)


def flatten(input, start_dim=0, end_dim=-1):
    r"""
    Flatten a tensor along dimensions from `start_dim` to `end_dim`.
    
    Args:
        input (Tensor): The input Tensor.
    
    Keyword Args:
        start_dim (int, optional): The first dimension to flatten. Default: ``0`` .
        end_dim (int, optional): The last dimension to flatten. Default: ``-1`` .
    
    Returns:
        Tensor. If no dimensions are flattened, returns the original `input`, otherwise return the flattened Tensor.
        If `input` is a 0-dimensional Tensor, a 1-dimensional Tensor will be returned.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        TypeError: If `start_dim` or `end_dim` is not int.
        ValueError: If `start_dim` is greater than `end_dim` after canonicalized.
        ValueError: If `start_dim` or `end_dim` is not in range of [-input.dim, input.dim-1].
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, mint
        >>> input_x = Tensor(np.ones(shape=[1, 2, 3, 4]), mindspore.float32)
        >>> output = mint.flatten(input_x)
        >>> print(output.shape)
        (24,)
    """
    return flatten_impl(input, start_dim, end_dim)


def unfold(input, kernel_size, dilation=1, padding=0, stride=1):
    r"""
    Extracts sliding local blocks from a batched input tensor.
    
    Consider a batched input tensor of shape :math:`(N, C, *)`,
    where :math:`N` is the batch dimension, :math:`C` is the channel dimension,
    and :math:`*` represent arbitrary spatial dimensions. This operation flattens
    each sliding `Kernel_size`- sized block within the spatial dimensions
    of `input` into a column (i.e., last dimension) of a 3-D output
    tensor of shape :math:`(N, C \times \prod(\text{kernel_size}), L)`, where
    :math:`C \times \prod(\text{kernel_size})` is the total number of values
    within each block (a block has :math:`\prod(\text{kernel_size})` spatial
    locations each containing a `C`-channeled vector), and :math:`L` is
    the total number of such blocks:
    
    .. math::
        L = \prod_d \left\lfloor\frac{\text{spatial_size}[d] + 2 \times \text{padding}[d] %
            - \text{dilation}[d] \times (\text{kernel_size}[d] - 1) - 1}{\text{stride}[d]} + 1\right\rfloor,
    
    where :math:`\text{spatial_size}` is formed by the spatial dimensions
    of `input` (:math:`*` above), and :math:`d` is over all spatial
    dimensions.
    
    Therefore, indexing `output` at the last dimension (column dimension)
    gives all values within a certain block.
    
    The `dilation`, `padding` and `stride` arguments specify
    how the sliding blocks are retrieved.
    
    .. warning::
        - Currently, batched(4D) image-like tensors are supported.
        - For Ascend, it is only supported on platforms above Atlas A2.
    
    Args:
        input (Tensor): 4-D Tensor.
        kernel_size (Union[int, tuple[int], list[int]]): The size of the kernel, should be two int
            for height and width. If type is int, it means that height equal with width. Must be specified.
        dilation (Union[int, tuple[int], list[int]], optional): The dilation of the window, should be two int
            for height and width. If type is int, it means that height equal with width. Default: ``1`` .
        padding (Union[int, tuple[int], list[int]], optional): The pad of the window, should be two int
            for height and width. If type is int, it means that height equal with width. Default: ``0`` .
        stride (Union[int, tuple[int], list[int]], optional): The stride of the window, should be two int
            for height and width. If type is int, it means that height equal with width. Default: ``1`` .
    
    Returns:
        A Tensor, with same type as `input` .
    
    Shape:
        - Input: :math:`(N, C, *)`
        - Output: :math:`(N, C \times \prod(\text{kernel_size}), L)`
    
    Raises:
        TypeError: If any data type of `kernel_size`, `stride`, `dilation`, `padding` is not int, tuple or list.
        ValueError: If `kernel_size`, `dilation`, `stride` value is not
            greater than zero or elements number more than `2`.
        ValueError: If `padding` value is less than zero.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> x = Tensor(np.random.rand(4, 4, 32, 32), mindspore.float32)
        >>> output = ops.auto_generate.unfold_ext(x, kernel_size=3, dilation=1, stride=1)
        >>> print(output.shape)
        (4, 36, 900)
    """
    return unfold_impl(input, converted_kernel_size, converted_dilation, converted_padding, converted_stride)


def index_select(input, dim, index):
    r"""
    Generates a new Tensor that accesses the values of `input` along the specified `dim` dimension
    using the indices specified in `index`. The new Tensor has the same number of dimensions as `input`,
    with the size of the `dim` dimension being equal to the length of `index`, and the size of all other
    dimensions will be unchanged from the original `input` Tensor.
    
    .. note::
        The value of index must be in the range of `[0, input.shape[dim])`, the result is undefined out of range.
    
    Args:
        input (Tensor): The input Tensor.
        dim (int): The dimension to be indexed.
        index (Tensor): A 1-D Tensor with the indices.
    
    Returns:
        Tensor, has the same dtype as input Tensor.
    
    Raises:
        TypeError: If `input` or `index` is not a Tensor.
        TypeError: If `dim` is not int number.
        ValueError: If the value of `dim` is out the range of `[-input.ndim, input.ndim - 1]`.
        ValueError: If the dimension of `index` is not equal to 1.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore
        >>> from mindspore import Tensor, ops
        >>> import numpy as np
        >>> input = Tensor(np.arange(16).astype(np.float32).reshape(2, 2, 4))
        >>> print(input)
        [[[ 0.  1.  2.  3.]
        [ 4.  5.  6.  7.]]
        [[ 8.  9. 10. 11.]
        [12. 13. 14. 15.]]]
        >>> index = Tensor([0,], mindspore.int32)
        >>> y = ops.auto_generate.index_select_ext(input, 1, index)
        >>> print(y)
        [[[ 0.  1.  2.  3.]]
        [[ 8.  9. 10. 11.]]]
    """
    return index_select_impl(input, dim, index)


def leaky_relu(input, negative_slope=0.01):
    r"""
    leaky_relu activation function. The element of `input` less than 0 times `negative_slope` .
    
    The activation function is defined as:
    
    .. math::
        \text{leaky_relu}(input) = \begin{cases}input, &\text{if } input \geq 0; \cr
        \text{negative_slope} * input, &\text{otherwise.}\end{cases}
    
    where :math:`negative\_slope` represents the `negative_slope` parameter.
    
    For more details, see `Rectifier Nonlinearities Improve Neural Network Acoustic Models
    <https://ai.stanford.edu/~amaas/papers/relu_hybrid_icml2013_final.pdf>`_.
    
    LeakyReLU Activation Function Graph:
    
    .. image:: ../images/LeakyReLU.png
        :align: center
    
    Args:
        input (Tensor): The input of leaky_relu is a Tensor of any dimension.
        negative_slope (Union[int, float]): Slope of the activation function when the element of `input` is less than 0.
          Default: ``0.01`` .
    
    Returns:
        Tensor, has the same type and shape as the `input`.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        TypeError: If `negative_slope` is not a float or an int.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> input = Tensor(np.array([[-1.0, 4.0, -8.0], [2.0, -5.0, 9.0]]), mindspore.float32)
        >>> print(ops.extend.leaky_relu_ext(input, negative_slope=0.2))
        [[-0.2  4.  -1.6]
         [ 2.  -1.   9. ]]
    """
    return leaky_relu_impl(input, negative_slope)


def matmul(input, mat2):
    r"""
    None
    """
    return matmul_impl(input, mat2)


def matrix_inverse(input):
    r"""
    Compute the inverse of the input matrix.
    
    Args:
        input (Tensor): A matrix to be calculated. Input `input` must be at least two dimensions, and the size of
            the last two dimensions must be the same size.
    
    Returns:
        Tensor, has the same type and shape as input`.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        ValueError: If the size of the last two dimensions of `input` is not the same.
        ValueError: If the dimension of `input` is 1.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> from mindspore import Tensor, ops
        >>> from mindspore import dtype as mstype
        >>> x = Tensor([[1., 2.], [3., 4.]], mstype.float32)
        >>> print(ops.matrix_inverse_ext(x))
        [[-2.   1. ]
         [ 1.5 -0.5]]
    """
    return matrix_inverse_impl(input)


def mean(input, axis=None, keep_dims=False, dtype=None):
    r"""
    Reduces all dimension of a tensor by averaging all elements in the dimension, by default.
    And reduce a dimension of `input` along the specified `axis`. `keep_dims`
    determines whether the dimensions of the output and input are the same.
    
    Note:
        The `axis` with tensor type is only used for compatibility with older versions and is not recommended.
    
    Args:
        input (Tensor[Number]): The input tensor. The dtype of the tensor to be reduced is number.
            :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
        axis (Union[int, tuple(int), list(int), Tensor]): The dimensions to reduce. Default: ``None`` ,
            reduce all dimensions. Only constant value is allowed. Assume the rank of `input` is r,
            and the value range is [-r,r).
        keep_dims (bool): If ``True`` , keep these reduced dimensions and the length is 1.
            If ``False`` , don't keep these dimensions. Default: ``False`` .
        dtype (:class:`mindspore.dtype`): The desired data type of returned Tensor. Default: ``None`` .
    
    Returns:
        Tensor, has the same data type as input tensor.
    
        - If `axis` is ``None`` , and `keep_dims` is ``False`` ,
          the output is a 0-D tensor representing the product of all elements in the input tensor.
        - If `axis` is int, set as 1, and `keep_dims` is ``False`` ,
          the shape of output is :math:`(x_0, x_2, ..., x_R)`.
        - If `axis` is tuple(int), set as (1, 2), and `keep_dims` is ``False`` ,
          the shape of output is :math:`(x_0, x_3, ..., x_R)`.
        - If `axis` is 1-D Tensor, set as [1, 2], and `keep_dims` is ``False`` ,
          the shape of output is :math:`(x_0, x_3, ..., x_R)`.
    
    Raises:
        TypeError: If `x` is not a Tensor.
        TypeError: If `axis` is not one of the following: int, tuple, list or Tensor.
        TypeError: If `keep_dims` is not a bool.
        ValueError: If `axis` is out of range.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> x = Tensor(np.random.randn(3, 4, 5, 6).astype(np.float32))
        >>> output = ops.mean(x, 1, keep_dims=True)
        >>> result = output.shape
        >>> print(result)
        (3, 1, 5, 6)
        >>> # case 1: Reduces a dimension by averaging all elements in the dimension.
        >>> x = Tensor(np.array([[[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]],
        ... [[4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5], [6, 6, 6, 6, 6, 6]],
        ... [[6, 6, 6, 6, 6, 6], [8, 8, 8, 8, 8, 8], [10, 10, 10, 10, 10, 10]]]),
        ... mindspore.float32)
        >>> output = ops.mean(x)
        >>> print(output)
        5.0
        >>> print(output.shape)
        ()
        >>> # case 2: Reduces a dimension along the axis 0
        >>> output = ops.mean(x, 0, True)
        >>> print(output)
        [[[4. 4. 4. 4. 4. 4.]
        [5. 5. 5. 5. 5. 5.]
        [6. 6. 6. 6. 6. 6.]]]
        >>> # case 3: Reduces a dimension along the axis 1
        >>> output = ops.mean(x, 1, True)
        >>> print(output)
        [[[2. 2. 2. 2. 2. 2.]]
        [[5. 5. 5. 5. 5. 5.]]
        [[8. 8. 8. 8. 8. 8.]]]
        >>> # case 4: Reduces a dimension along the axis 2
        >>> output = ops.mean(x, 2, True)
        >>> print(output)
        [[[ 2.]
        [ 2.]
        [ 2.]]
        [[ 4.]
        [ 5.]
        [ 6.]]
        [[ 6.]
        [ 8.]
        [10.]]]
    """
    return mean_impl(input, axis, keep_dims, dtype)


def prod(input, axis=None, keep_dims=False, dtype=None):
    r"""
    Reduces a dimension of a tensor by multiplying all elements in the dimension, by default. And also can
    reduce a dimension of `input` along the `axis`. Determine whether the dimensions of the output and input are the
    same by controlling `keep_dims`.
    
    Args:
        input (Tensor[Number]): The input tensor. The dtype of the tensor to be reduced is number.
            :math:`(N, *)` where :math:`*` means, any number of additional dimensions.
        axis (int): The dimensions to reduce. Default: ``None`` , reduce all dimensions.
            Only constant value is allowed. Assume the rank of `input` is r, and the value range is [-r,r).
        keep_dims (bool): If ``True`` , keep these reduced dimensions and the length is 1.
            If ``False`` , don't keep these dimensions. Default: ``False`` .
        dtype (:class:`mindspore.dtype`): The desired data type of returned Tensor. Default: ``None`` .
    
    Returns:
        Tensor, has the same data type as input tensor.
    
        - If `axis` is ``None`` , and `keep_dims` is  ``False`` ,
          the output is a 0-D tensor representing the product of all elements in the input tensor.
        - If `axis` is int, set as 1, and `keep_dims` is  ``False`` ,
          the shape of output is :math:`(input_0, input_2, ..., input_R)`.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        TypeError: If `axis` is not one of the following: int or None.
        TypeError: If `keep_dims` is not a bool.
        ValueError: If `axis` is out of range.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> x = Tensor(np.random.randn(3, 4, 5, 6).astype(np.float32))
        >>> output = ops.ProdExt()(x, 1, keep_dims=True)
        >>> result = output.shape
        >>> print(result)
        (3, 1, 5, 6)
        >>> # case 1: Reduces a dimension by multiplying all elements in the dimension.
        >>> x = Tensor(np.array([[[1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2], [3, 3, 3, 3, 3, 3]],
        ...                      [[4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5], [6, 6, 6, 6, 6, 6]],
        ...                      [[7, 7, 7, 7, 7, 7], [8, 8, 8, 8, 8, 8], [9, 9, 9, 9, 9, 9]]]), mindspore.float32)
        >>> output = ops.ProdExt()(x)
        >>> print(output)
        2.2833798e+33
        >>> print(output.shape)
        ()
        >>> # case 2: Reduces a dimension along axis 0.
        >>> output = ops.ProdExt()(x, 0, True)
        >>> print(output)
        [[[ 28.  28.  28.  28.  28.  28.]
        [ 80.  80.  80.  80.  80.  80.]
        [162. 162. 162. 162. 162. 162.]]]
        >>> # case 3: Reduces a dimension along axis 1.
        >>> output = ops.ProdExt()(x, 1, True)
        >>> print(output)
        [[[  6.   6.   6.   6.   6.   6.]]
        [[120. 120. 120. 120. 120. 120.]]
        [[504. 504. 504. 504. 504. 504.]]]
        >>> # case 4: Reduces a dimension along axis 2.
        >>> output = ops.ProdExt()(x, 2, True)
        >>> print(output)
        [[[1.00000e+00]
        [6.40000e+01]
        [7.29000e+02]]
        [[4.09600e+03]
        [1.56250e+04]
        [4.66560e+04]]
        [[1.17649e+05]
        [2.62144e+05]
        [5.31441e+05]]]
    """
    return prod_impl(input, axis, keep_dims, dtype)


def softplus(input, beta=1, threshold=20):
    r"""
    Applies softplus function to `input` element-wise.
    
    The softplus function is shown as follows, x is the element of `input` :
    
    .. math::
    
        \text{output} = \frac{1}{beta}\log(1 + \exp(\text{beta * x}))
    
    where :math:`input * beta > threshold`, the implementation converts to the linear function to ensure numerical stability.
    
    Args:
        input (Tensor): Tensor of any dimension. Supported dtypes: 
    
            - Ascend: float16, float32, bfloat16.
        beta (number.Number, optional): Scaling parameters in the softplus function. Default: ``1`` .
        threshold (number.Number, optional): For numerical stability, the softplus function is converted 
            to a threshold parameter of a linear function. Default: ``20`` .
    
    Returns:
        Tensor, with the same type and shape as the input.
    
    Raises:
        TypeError: If `input` is not a Tensor.
        TypeError: If dtype of `input` is not float16, float32, bfloat16.
    
    Supported Platforms:
        ``Ascend`` 
    
    Examples:
        >>> import mindspore
        >>> import numpy as np
        >>> from mindspore import Tensor, ops
        >>> input = Tensor(np.array([0.1, 0.2, 30, 25]), mindspore.float32)
        >>> output = ops.auto_generate.softplus_ext(input)
        >>> print(output)
        [0.74439657 0.7981388 30. 25.]
    """
    return softplus_impl(input, beta, threshold)


def sort(input, dim=-1, descending=False, stable=False):
    r"""
    None
    """
    return sort_impl(input, dim, descending, stable)


def stack(tensors, dim=0):
    r"""
    Stacks a list of tensors in specified dim.
    
    Stacks the list of input tensors with the same rank `R`, output is a tensor of rank `(R+1)`.
    
    Given input tensors of shape :math:`(x_1, x_2, ..., x_R)`. Set the number of input tensors as `N`.
    If :math:`dim \ge 0`, the shape of the output tensor is
    :math:`(x_1, x_2, ..., x_{dim}, N, x_{dim+1}, ..., x_R)`.
    
    Args:
        tensors (Union[tuple, list]): A Tuple or list of Tensor objects with the same shape and type.
        dim (int): Dimension to stack. The range is [-(R+1), R+1). Default: ``0`` .
    
    Returns:
        Tensor. A stacked Tensor with the same type as `tensors`.
    
    Raises:
        TypeError: If the data types of elements in `tensors` are not the same.
        ValueError: If `dim` is out of the range [-(R+1), R+1);
                    or if the shapes of elements in tensors are not the same.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore
        >>> from mindspore import Tensor, ops
        >>> import numpy as np
        >>> data1 = Tensor(np.array([0, 1]).astype(np.float32))
        >>> data2 = Tensor(np.array([2, 3]).astype(np.float32))
        >>> output = ops.auto_generate.stack_ext([data1, data2], 0)
        >>> print(output)
        [[0. 1.]
         [2. 3.]]
    """
    return stack_impl(tensors, dim)


def sub(input, other, alpha=1):
    r"""
    Subtracts scaled other value from input Tensor.
    
    .. math::
    
        out_{i} = input_{i} - alpha \times other_{i}
    
    Note:
        - When the two inputs have different shapes,
          they must be able to broadcast to a common shape.
        - The two inputs and alpha comply with the implicit type conversion rules to make the data types
          consistent.
    
    Args:
        input (Union[Tensor, number.Number, bool]): The first input is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        other (Union[Tensor, number.Number, bool]): The second input, is a number.Number or
            a bool or a tensor whose data type is
            `number <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_ or
            `bool_ <https://www.mindspore.cn/docs/en/master/api_python/mindspore.html#mindspore.dtype>`_.
        alpha (number.Number): A scaling factor applied to `other`, default 1.
    
    Returns:
        Tensor with a shape that is the same as the broadcasted shape of the input `input` and `other`,
        and the data type is the one with higher precision or higher digits among the two inputs and alpha.
    
    Raises:
        TypeError: If the type of `input`, `other`, or `alpha` is not one of the following: Tensor, number.Number, bool.
        TypeError: If `alpha` is of type float but `input` and `other` are not of type float.
        TypeError: If `alpha` is of type bool but `input` and `other` are not of type bool.
    
    Supported Platforms:
        ``Ascend`` ``GPU`` ``CPU``
    
    Examples:
        >>> import numpy as np
        >>> import mindspore
        >>> from mindspore import Tensor
        >>> from mindspore import ops
        >>> x = Tensor(np.array([4, 5, 6]).astype(np.float32))
        >>> y = Tensor(1, mindspore.int32)
        >>> alpha = 0.5
        >>> output = ops.auto_generate.sub_ext(x, y, alpha)
        >>> print(output)
        [3.5 4.5 5.5]
        >>> # the data type of x is float32, the data type of y is int32,
        >>> # alpha is a float, and the output is the data format of higher precision float32.
        >>> print(output.dtype)
        Float32
    """
    return sub_impl(input, other, alpha)


def topk(input, k, dim=-1, largest=True, sorted=True):
    r"""
    Finds values and indices of the `k` largest or smallest entries along a given dimension.
    
    .. warning::
        - If sorted is set to False, due to different memory layout and traversal methods on different platforms,
          the display order of calculation results may be inconsistent when `sorted` is False.
    
    If the `input` is a one-dimensional Tensor, finds the `k` largest  or smallest entries in the Tensor,
    and outputs its value and index as a Tensor. values[`k`] is the `k` largest item in `input`,
    and its index is indices [`k`].
    
    For a multi-dimensional matrix,
    calculates the first or last `k` entries in a given dimension, therefore:
    
    .. math::
    
        values.shape = indices.shape
    
    If the two compared elements are the same, the one with the smaller index value is returned first.
    
    Args:
        input (Tensor): Input to be computed.
        k (int): The number of top or bottom elements to be computed along the last dimension.
        dim (int, optional): The dimension to sort along. Default: ``-1`` .
        largest (bool, optional): If largest is ``False``  then the k smallest elements are returned.
            Default: ``True`` .
        sorted (bool, optional): If ``True`` , the obtained elements will be sorted by the values in descending
            order or ascending order according to `largest`. If ``False`` , the obtained elements will not be
            sorted. Default: ``True`` .
    
    Returns:
        A tuple consisting of `values` and `indices`.
    
        - values (Tensor) - The `k` largest or smallest elements in each slice of the given dimension.
        - indices (Tensor) - The indices of values within the last dimension of input.
    
    Raises:
        TypeError: If `sorted` is not a bool.
        TypeError: If `input` is not a Tensor.
        TypeError: If `k` is not an int.
    
    Supported Platforms:
        ``Ascend``
    
    Examples:
        >>> import mindspore as ms
        >>> from mindspore import ops
        >>> x = ms.Tensor([[0.5368, 0.2447, 0.4302, 0.9673],
        ...                [0.4388, 0.6525, 0.4685, 0.1868],
        ...                [0.3563, 0.5152, 0.9675, 0.8230]], dtype=ms.float32)
        >>> output = ops.topk_ext(x, 2, dim=1)
        >>> print(output)
        (Tensor(shape=[3, 2], dtype=Float32, value=
        [[ 9.67299998e-01,  5.36800027e-01],
         [ 6.52499974e-01,  4.68499988e-01],
         [ 9.67499971e-01,  8.23000014e-01]]), Tensor(shape=[3, 2], dtype=Int32, value=
        [[3, 0],
         [1, 2],
         [2, 3]]))
        >>> output2 = ops.topk_ext(x, 2, dim=1, largest=False)
        >>> print(output2)
        (Tensor(shape=[3, 2], dtype=Float32, value=
        [[ 2.44700000e-01,  4.30200011e-01],
         [ 1.86800003e-01,  4.38800007e-01],
         [ 3.56299996e-01,  5.15200019e-01]]), Tensor(shape=[3, 2], dtype=Int32, value=
        [[1, 2],
         [3, 0],
         [0, 1]]))
    """
    return topk_impl(input, k, dim, largest, sorted)

