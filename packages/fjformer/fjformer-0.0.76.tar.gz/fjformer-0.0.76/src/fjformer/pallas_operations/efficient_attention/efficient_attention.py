import functools
from typing import NamedTuple
import jax
import jax.lax as lax
import jax.numpy as jnp
from einops import rearrange
import chex


class Carry(NamedTuple):
    numerator: chex.Array
    denominator: chex.Array
    max_so_far: chex.Array


def efficient_attention(
        query: chex.Array,
        key: chex.Array,
        value: chex.Array,
        bias: chex.Array = None,
        deterministic: bool = True,
        dropout_rng: chex.PRNGKey = None,
        attention_drop_rate: float = 0.0,
        causal: bool = True,
        query_chunk_size: int = 1024,
        key_chunk_size: int = 1024,
        dtype: chex.ArrayDType = jnp.float32,
        policy=jax.checkpoint_policies.nothing_saveable(),
        precision=None,
        float32_logits: bool = True,
        prevent_cse: bool = True,
):
    """

    :param query: Array Shape [batch,Q Sequence length,num attention heads, head dims]
    :param key: Array Shape [batch,KV Sequence length,num KV attention heads, head dims]
    :param value: Array Shape [batch,KV Sequence length,num KV attention heads, head dims]
    :param bias: Bias To be added
    :param deterministic: bool (whenever use dropout or no)
    :param dropout_rng: RNG Dropout
    :param attention_drop_rate:
    :param causal: Is Decoder or Causal
    :param query_chunk_size: Chunk size used for query
    :param key_chunk_size: Chunk size used for key
    :param dtype: DataType
    :param policy: Gradient Checkpoint Policy
    :param precision: PrecisionLike
    :param float32_logits:
    :param prevent_cse:
    :return:
    """
    query = query / jnp.sqrt(query.shape[-1]).astype(dtype)
    if float32_logits:
        query = query.astype(jnp.float32)
        key = key.astype(jnp.float32)

    batch, q_len, num_heads, dim_per_head = query.shape
    batch, kv_len, kv_heads, dim_per_head = key.shape
    batch, kv_len, kv_heads, dim_per_head = value.shape

    num_q = q_len // query_chunk_size
    num_kv = kv_len // key_chunk_size
    query = query.reshape((batch, num_q, query_chunk_size, num_heads, dim_per_head))
    key = key.reshape((batch, num_kv, key_chunk_size, kv_heads, dim_per_head))
    value = value.reshape((batch, num_kv, key_chunk_size, kv_heads, dim_per_head))

    query = jnp.moveaxis(query, 1, 0)
    key = jnp.moveaxis(key, 1, 0)
    value = jnp.moveaxis(value, 1, 0)

    if bias is not None:
        for bias_dim, broadcast_dim in zip(bias.shape, (batch, num_heads, q_len, kv_len)):
            assert bias_dim == 1 or bias_dim == broadcast_dim
    if not deterministic and attention_drop_rate > 0.0:
        attn_dropout_rng, dropout_rng = jax.random.split(dropout_rng)
        attn_dropout = jax.random.bernoulli(attn_dropout_rng, attention_drop_rate, (batch, num_heads, q_len, kv_len))
    else:
        attn_dropout = None

    _chunk_bias_fn = functools.partial(
        _chunk_attention_bias,
        query_chunk_size, key_chunk_size, bias, deterministic,
        attn_dropout, attention_drop_rate, causal, dtype)

    def scan_attention(args):
        query_chunk, query_chunk_idx = args

        @functools.partial(jax.checkpoint, prevent_cse=prevent_cse, policy=policy)
        def scan_kv_block(carry, args):
            key_chunk, value_chunk, key_chunk_idx = args
            (numerator, denominator, prev_max_score) = carry
            attn_weights = jnp.einsum('bqhd,bkhd->bqhk', query_chunk, key_chunk, precision=precision)
            bias_chunk = _chunk_bias_fn(query_chunk_idx, key_chunk_idx)
            bias_chunk = jnp.moveaxis(bias_chunk, 1, 2)
            attn_weights = attn_weights + bias_chunk

            max_score = jnp.max(attn_weights, axis=-1, keepdims=True)
            max_score = jnp.maximum(prev_max_score, max_score)
            max_score = jax.lax.stop_gradient(max_score)
            exp_weights = jnp.exp(attn_weights - max_score)
            exp_values = jnp.einsum(
                'bqhv,bvhd->bqhd', exp_weights, value_chunk, precision=precision
            )
            correction = jnp.exp(prev_max_score - max_score)
            numerator = numerator * correction + exp_values
            denominator = denominator * correction + exp_weights.sum(axis=-1, keepdims=True)
            return Carry(numerator, denominator, max_score), None

        def skip_upper_half(carry, args):
            key_chunk, value_chunk, key_chunk_idx = args
            skip_block = jnp.array(False)
            if causal:
                skip_block = query_chunk_idx < key_chunk_idx
            return jax.lax.cond(
                skip_block,
                lambda carry, args: (carry, None),
                scan_kv_block,
                carry,
                args,
            )

        init_carry = Carry(
            jnp.zeros((batch, query_chunk_size, num_heads, dim_per_head), dtype=query.dtype),
            jnp.zeros((batch, query_chunk_size, num_heads, dim_per_head), dtype=query.dtype),
            (-jnp.inf) * jnp.ones((batch, query_chunk_size, num_heads, 1), dtype=query.dtype),
        )
        (numerator, denominator, max_score), _ = lax.scan(
            skip_upper_half, init_carry, xs=(key, value, jnp.arange(0, num_kv))
        )
        outputs = (numerator / denominator).astype(dtype)
        return outputs

    _, res = lax.scan(
        lambda _, x: ((), scan_attention(x)),
        (), xs=(query, jnp.arange(0, num_q))
    )
    res = rearrange(res, 'n b c h d -> b (n c) h d')
    return res


def _chunk_attention_bias(
        query_chunk_size: int,
        key_chunk_size: int,
        bias: chex.Array,
        deterministic: bool,
        attn_dropout: chex.Array,
        attention_drop_rate: float,
        causal: bool,
        dtype: chex.ArrayDType,
        query_chunk_idx: int,
        key_chunk_idx: int
):
    """
    The _chunk_attention_bias function is used to compute the attention bias for a single chunk of
    the query and key tensors. The function takes in the following arguments:

    :param query_chunk_size: int: Determine the size of the query chunk
    :param key_chunk_size: int: Determine the size of the key_chunk
    :param bias: chex.Array: Mask out the attention weights
    :param deterministic: bool: Determine whether to use dropout or not
    :param attn_dropout: chex.Array: Drop out attention weights
    :param attention_drop_rate: float: Determine the dropout rate for attention
    :param causal: bool: Determine if the attention is causal or not
    :param dtype: chex.ArrayDType: Specify the data type of the array
    :param query_chunk_idx: int: Select the query chunk
    :param key_chunk_idx: int: Determine the key_offset
    :return: A chunk of the attention bias
    
    """
    query_offset = query_chunk_idx * query_chunk_size
    key_offset = key_chunk_idx * key_chunk_size
    chunk_bias = jnp.zeros((1, 1, 1, 1), dtype=dtype)
    if bias is not None:
        chunk_bias = lax.dynamic_slice(
            bias,
            start_indices=(0, 0, query_offset, key_offset),
            slice_sizes=(*bias.shape[:2], min(bias.shape[-2], query_chunk_size), min(bias.shape[-1], key_chunk_size)),
        )

    if causal:
        query_idx = lax.broadcasted_iota(dtype=jnp.int32, shape=(query_chunk_size, 1), dimension=0)
        key_idx = lax.broadcasted_iota(dtype=jnp.int32, shape=(1, key_chunk_size), dimension=1)
        offset = query_offset - key_offset
        query_idx += offset
        causal_mask_value = (query_idx < key_idx) * jnp.finfo(dtype).min
        chunk_bias += causal_mask_value.reshape(1, 1, *causal_mask_value.shape)

    if not deterministic and attention_drop_rate > 0.0:
        attn_dropout_slice = lax.dynamic_slice(
            attn_dropout,
            start_indices=(0, 0, query_offset, key_offset),
            slice_sizes=(
                *attn_dropout.shape[:2],
                min(attn_dropout.shape[-2], query_chunk_size),
                min(attn_dropout.shape[-1], key_chunk_size),
            ),
        )
        chunk_bias += attn_dropout_slice * jnp.finfo(dtype).min
    return chunk_bias.astype(dtype)
