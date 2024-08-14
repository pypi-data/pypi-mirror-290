

def affine_quantize(w: array, /, scales: array, biases: array, group_size: int = 64, bits: int = 4, *, stream: Union[None, Stream, Device] = None) -> array:
    r"""
    Quantize the matrix ``w`` using the provided ``scales`` and
    ``biases`` and the ``group_size`` and ``bits`` configuration.

    Formally, given the notation in :func:`quantize`, we compute
    :math:`w_i` from :math:`\hat{w_i}` and corresponding :math:`s` and
    :math:`\beta` as follows

    .. math::

      w_i = s (\hat{w_i} + \beta)

    Args:
      w (array): Matrix to be quantize
      scales (array): The scales to use per ``group_size`` elements of ``w``
      biases (array): The biases to use per ``group_size`` elements of ``w``
      group_size (int, optional): The size of the group in ``w`` that shares a
        scale and bias. (default: ``64``)
      bits (int, optional): The number of bits occupied by each element in
        ``w``. (default: ``4``)

    Returns:
      array: The quantized version of ``w``
    """

def layer_norm(x: array, weight: Optional[array], bias: Optional[array], eps: float, *, stream: Union[None, Stream, Device] = None) -> array:
    """
    Layer normalization.

    The normalization is with respect to the last axis of the input ``x``.

    Args:
        x (array): Input array.
        weight (array, optional): A multiplicative weight to scale the result by.
          The ``weight`` should be one-dimensional with the same size
          as the last axis of ``x``. If set to ``None`` then no scaling happens.
        bias (array, optional): An additive offset to be added to the result.
          The ``bias`` should be one-dimensional with the same size
          as the last axis of ``x``. If set to ``None`` then no translation happens.
        eps (float): A small additive constant for numerical stability.

    Returns:
        array: The output array.
    """

def rms_norm(x: array, weight: array, eps: float, *, stream: Union[None, Stream, Device] = None) -> array:
    """
    Root Mean Square normalization (RMS norm).

    The normalization is with respect to the last axis of the input ``x``.

    Args:
        x (array): Input array.
        weight (array): A multiplicative weight to scale the result by.
          The ``weight`` should be one-dimensional with the same size
          as the last axis of ``x``.
        eps (float): A small additive constant for numerical stability.

    Returns:
        array: The output array.
    """

def rope(a: array, dims: int, *, traditional: bool, base: float, scale: float, offset: int, stream: Union[None, Stream, Device] = None) -> array:
    """
    Apply rotary positional encoding to the input.

    Args:
        a (array): Input array.
        dims (int): The feature dimensions to be rotated. If the input feature
            is larger than dims then the rest is left unchanged.
        traditional (bool): If set to ``True`` choose the traditional
            implementation which rotates consecutive dimensions.
        base (float): The base used to compute angular frequency for
            each dimension in the positional encodings.
        scale (float): The scale used to scale the positions.
        offset (int): The position offset to start at.

    Returns:
        array: The output array.
    """

def scaled_dot_product_attention(q: array, k: array, v: array, *, scale: float,  mask: Union[None, array] = None, stream: Union[None, Stream, Device] = None) -> array:
    """
    A fast implementation of multi-head attention: ``O = softmax(Q @ K.T, dim=-1) @ V``.

    Supports:

    * `Multi-Head Attention <https://arxiv.org/abs/1706.03762>`_
    * `Grouped Query Attention <https://arxiv.org/abs/2305.13245>`_
    * `Multi-Query Attention <https://arxiv.org/abs/1911.02150>`_

    Note: The softmax operation is performed in ``float32`` regardless of
    the input precision.

    Note: For Grouped Query Attention and Multi-Query Attention, the ``k``
    and ``v`` inputs should not be pre-tiled to match ``q``.

    Args:
        q (array): Input query array.
        k (array): Input keys array.
        v (array): Input values array.
        scale (float): Scale for queries (typically ``1.0 / sqrt(q.shape(-1)``)
        mask (array, optional): An additive mask to apply to the query-key scores.
    Returns:
        array: The output array.
    """
