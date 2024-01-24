import sys
import threading
import time
import numba, numpy
import torch
import torch.utils.cpp_extension
import numba.cuda
import numpy
from torch.utils._python_dispatch import TorchDispatchMode

cuda_src = """
__device__ __inline__ std::pair<uint32_t, uint32_t> device_apply_round(uint32_t v0, uint32_t v1, const uint32_t rot) {
  v0 = v0 + v1;
  v1 = (v1 << rot) + (v1 >> (32 - rot));
  v1 = v0 ^ v1;
  return std::make_pair(v0, v1);
}

__device__ __inline__ std::pair<uint32_t, uint32_t> device_threefry2x32(uint32_t key0, uint32_t key1, uint32_t x0, uint32_t x1) {
  uint32_t key2 = key0 ^key1 ^ 0x1BD11BDA;
  x0 = x0 + key0;
  x1 = x1 + key1;
  inline static constexpr const uint32_t[] r0 {13, 15, 26, 6};
  inline static constexpr const uint32_t[] r1 {17, 29, 16, 24};
  foreach (const uint32_t r: r0) {
    auto[x0, x1] = apply_round(x0, x1, r);
  }
  x0 = x0 + key1;
  x1 = x1 + key2 + 1;
  foreach (const uint32_t r: r1) {
    auto[x0, x1] = apply_round(x0, x1, r);
  }
  x0 = x0 + key2;
  x1 = x1 + key0 + 2;
  foreach (const uint32_t r: r0) {
    auto[x0, x1] = apply_round(x0, x1, r);
  }
  x0 = x0 + key0;
  x1 = x1 + key1 + 3;
  foreach (const uint32_t r: r1) {
    auto[x0, x1] = apply_round(x0, x1, r);
  }
  x0 = x0 + key1;
  x1 = x1 + key2 + 4;
  foreach (const uint32_t r: r0) {
    auto[x0, x1] = apply_round(x0, x1, r);
  }
  x0 = x0 + key2;
  x1 = x1 + key0 + 5;
  return std::make_pair(x0, x1);
}

__global__ void threefry2x32_kernel(uint32_t key0, uint32_t key1, TensorInfo inp0, TensorInfo inp1, TensorInfo out1, TensorInfo out2) {
  
}
def threefry2x32_kernel(key0: numba.uint32, key1: numba.uint32, inp1, inp2, out1, out2):
    idx = numba.cuda.grid(1)
        
    x0 = inp1[idx]
    x1 = inp2[idx]
    
    x0, x1 = cu_threefry2x32(key0, key1, x0, x1)
    
    out1[idx] = x0
    out2[idx] = x1




"""

csrc = """

struct MyGeneratorImpl : public at::GeneratorImpl {
   
   MyGeneratorImpl(uint64_t seed_in = 0): c10::GeneratorImpl{c10::Device(c10::DeviceType::CPU), c10::DispatchKeySet(c10::DispatchKey::CPU)} {}
   void set_current_seed(uint64_t _) override {}
   void set_offset(uint64_t _) override {}
   uint64_t get_offset() const override { return 0; }
   uint64_t current_seed() const override { return 0; }
   uint64_t seed() override { return 0; }
   void set_state(const c10::TensorImpl& new_state) override {}
   c10::intrusive_ptr<c10::TensorImpl> get_state() const override {
     auto t = torch::Tensor();
     return t.getIntrusivePtr();
   }
  MyGeneratorImpl* clone_impl() const {
    auto gen = new MyGeneratorImpl();
    return gen;
  }
};

at::Generator my_op_impl() {
    return at::make_generator<MyGeneratorImpl>(0);
}


TORCH_LIBRARY(torchrandom, m) {
    m.def("my_op() -> Generator?", my_op_impl);
}

"""
if False:
    torch.utils.cpp_extension.load_inline(
        name="torchrandom",
        cpp_sources=csrc,
        # extra_ldflags=["-lopencv_core", "-lopencv_imgproc"],
        is_python_module=False,
        verbose=True,
    )


# used for CPU
def arr_threefry2x32(key0, key1, x0, x1):
    key0 = key0.astype(dtype=numpy.uint32, copy=False)
    key1 = key1.astype(dtype=numpy.uint32, copy=False)
    key2 = key0.copy()
    key2 ^= key1
    key2 ^= numpy.uint32(0x1BD11BDA)
    x0 = x0.astype(numpy.uint32)  # This makes a copy!
    x1 = x1.astype(numpy.uint32)  # This makes a copy!
    r0 = numpy.array((13, 15, 26, 6), dtype=numpy.uint32)
    r1 = numpy.array((17, 29, 16, 24), dtype=numpy.uint32)

    x0 += key0
    x1 += key1
    for r in r0:
        x0 += x1
        x1[:] = (x1 << r) + (x1 >> (32 - r))
        x1 ^= x0

    x0 += key1
    x1 += key2
    x1 += numpy.uint32(1)

    for r in r1:
        x0 += x1
        x1[:] = (x1 << r) + (x1 >> (32 - r))
        x1 ^= x0

    x0 += key2
    x1 += key0
    x1 += numpy.uint32(2)

    for r in r0:
        x0 += x1
        x1[:] = (x1 << r) + (x1 >> (32 - r))
        x1 ^= x0

    x0 += key0
    x1 += key1
    x1 += numpy.uint32(3)

    for r in r1:
        x0 += x1
        x1[:] = (x1 << r) + (x1 >> (32 - r))
        x1 ^= x0
    x0 += key1
    x1 += key2
    x1 += numpy.uint32(4)

    for r in r0:
        x0 += x1
        x1[:] = (x1 << r) + (x1 >> (32 - r))
        x1 ^= x0
    x0 += key2
    x1 += key0
    x1 += numpy.uint32(5)

    return x0, x1


@numba.cuda.jit(device=True)
def cu_apply_round(
    v0: numba.uint32, v1: numba.uint32, rot: numba.uint32
) -> tuple[numba.uint32, numba.uint32]:
    v0 = numba.uint32(v0 + v1)
    v1 = numba.uint32(numba.uint32(v1 << rot) + numba.uint32(v1 >> (32 - rot)))
    v1 = numba.uint32(v0 ^ v1)
    return v0, v1


@numba.cuda.jit(device=True)
def cu_threefry2x32(
    key0: numba.uint32, key1: numba.uint32, x0: numba.uint32, x1: numba.uint32
) -> tuple[numba.uint32, numba.uint32]:
    key2 = numba.uint32(key0 ^ key1 ^ numba.uint32(0x1BD11BDA))

    x0 = x0 + key0
    x1 = x1 + key1
    r0 = (13, 15, 26, 6)
    r1 = (17, 29, 16, 24)
    for r in r0:
        x0, x1 = cu_apply_round(x0, x1, r)

    x0 = numba.uint32(x0 + key1)
    x1 = numba.uint32(x1 + key2 + numba.uint32(1))

    for r in r1:
        x0, x1 = cu_apply_round(x0, x1, r)
    x0 = numba.uint32(x0 + key2)
    x1 = numba.uint32(x1 + key0 + numba.uint32(2))
    for r in r0:
        x0, x1 = cu_apply_round(x0, x1, r)
    x0 = numba.uint32(x0 + key0)
    x1 = numba.uint32(x1 + key1 + numba.uint32(3))

    for r in r1:
        x0, x1 = cu_apply_round(x0, x1, r)
    x0 = numba.uint32(x0 + key1)
    x1 = numba.uint32(x1 + key2 + numba.uint32(4))

    for r in r0:
        x0, x1 = cu_apply_round(x0, x1, r)
    x0 = numba.uint32(x0 + key2)
    x1 = numba.uint32(x1 + key0 + numba.uint32(5))

    return x0, x1


@numba.cuda.jit
def threefry2x32_kernel(key0: numba.uint32, key1: numba.uint32, inp1, inp2, out1, out2):
    idx = numba.cuda.grid(1)

    x0 = inp1[idx]
    x1 = inp2[idx]

    x0, x1 = cu_threefry2x32(key0, key1, x0, x1)

    out1[idx] = x0
    out2[idx] = x1


@numba.cuda.jit
def cu_random_array_kernel(key0: numba.uint32, key1: numba.uint32, shape, out0, out1):
    thread_idx = numba.cuda.grid(1)
    num_threads = numba.cuda.gridsize(1)

    for item_idx in range(thread_idx, out0.size, num_threads):
        idx = item_idx
        # this assumes that the last dim is the fastest moving
        for d in range(shape.size - 1, -1, -1):
            n = shape[d]
            idx_in_d = idx % n
            idx //= n
            if idx_in_d > 0:
                key0, key1 = cu_threefry2x32(
                    key0, key1, numba.uint32(idx_in_d), numba.uint32(shape.size - 1 - d)
                )

        out0[item_idx] = key0
        out1[item_idx] = key1


def cu_random_array(key0, key1, shape):
    key0 = numpy.array(key0, dtype=numpy.uint32)
    key1 = numpy.array(key1, dtype=numpy.uint32)
    inp0 = numpy.array((20342,), dtype=numpy.uint32)
    inp1 = numpy.array((134345,), dtype=numpy.uint32)

    print(numpy.prod(shape))
    shape_d = numba.cuda.to_device(numpy.array(shape, dtype=numpy.uint32))
    out0_d = numba.cuda.device_array(shape, dtype=numpy.uint32)
    out1_d = numba.cuda.device_array(shape, dtype=numpy.uint32)

    nkey0, nkey1 = arr_threefry2x32(key0, key1, inp0, inp1)
    nkey0 = numpy.uint32(int(nkey0))
    nkey1 = numpy.uint32(int(nkey1))
    print(nkey0, type(nkey0))
    threadsperblock = (256,)
    blockspergrid = (256,)
    if len(shape) > 1:  # bug in numba?
        out0_d_arg = out0_d.ravel()
        out1_d_arg = out1_d.ravel()
    else:
        out0_d_arg = out0_d
        out1_d_arg = out1_d
    cu_random_array_kernel[blockspergrid, threadsperblock](
        nkey0, nkey1, shape_d, out0_d_arg, out1_d_arg
    )

    return out0_d, out1_d


# This would benefit greatly from an implementation in C++. Unfortunately, it seems harder to compose
# pointwise functions efficiently in Numba
def random_array(key0, key1, shape):
    key0 = numpy.array(key0, dtype=numpy.uint32)
    key1 = numpy.array(key1, dtype=numpy.uint32)
    inp0 = numpy.array((20342,), dtype=numpy.uint32)
    inp1 = numpy.array((134345,), dtype=numpy.uint32)
    nkey0, nkey1 = arr_threefry2x32(key0, key1, inp0, inp1)
    out0 = numpy.zeros(shape, dtype=numpy.uint32)
    out1 = numpy.zeros(shape, dtype=numpy.uint32)
    idx = [0 for _ in shape]
    out0[tuple(idx)] = nkey0
    out1[tuple(idx)] = nkey1
    for d, n in list(enumerate(shape))[::-1]:
        # what if the range does not fit?
        inp0 = numpy.arange(1, n, dtype=numpy.uint32)[
            (...,) + tuple(None for _ in shape[d + 1 :])
        ]
        inp0 = numpy.broadcast_to(inp0, (n - 1, *shape[d + 1 :])).copy()
        inp1 = numpy.full_like(inp0, len(shape) - 1 - d)
        key0 = out0[tuple(idx)]  # [None]
        key1 = out1[tuple(idx)]  # [None]
        idx[d] = slice(1, None)
        # print(idx)
        tmp0, tmp1 = arr_threefry2x32(key0, key1, inp0, inp1)
        out0[tuple(idx)], out1[tuple(idx)] = tmp0, tmp1
        idx[d] = slice(None)
    return out0, out1


@numba.jit(parallel=True)
def bit_length(inp):
    r = ((inp > 0xFFFFFFFF) << 5).astype(numpy.uint64)
    v = inp >> r
    shift = ((v > 0xFFFF) << 4).astype(numpy.uint64)
    v >>= shift
    r |= shift
    shift = ((v > 0xFF) << 3).astype(numpy.uint64)
    v >>= shift
    r |= shift
    shift = ((v > 0xF) << 2).astype(numpy.uint64)
    v >>= shift
    r |= shift
    shift = ((v > 0x3) << 1).astype(numpy.uint64)
    v >>= shift
    r |= shift
    return (r | (v >> numpy.uint64(1))) + (inp > 0).astype(numpy.uint64)


@numba.jit(parallel=True)
def int32x2_to_fp64_uniform(i0, i1):
    np_int_type = numpy.uint64
    i64 = (i0.astype(np_int_type) << np_int_type(32)) + i1.astype(np_int_type)
    f_exp_bits = np_int_type(11)
    f_frac_bits = np_int_type(52)
    i_width = f_exp_bits + f_frac_bits + 1
    f_exp_offset = 2 ** (f_exp_bits - 1) - 1
    bl = bit_length(i64)
    i = i64 << (i_width - bl).astype(np_int_type)
    i = i >> np_int_type(f_exp_bits)
    i = i & np_int_type(2**f_frac_bits - 1)
    fpbits = (
        (f_exp_offset - i_width + bl - 1).astype(np_int_type)
        * (i64 > 0).astype(np_int_type)
    ) << f_frac_bits | i
    return fpbits


@numba.jit(parallel=True)
def int32_to_fp32_uniform(i0):
    np_int_type = numpy.uint32
    inp = i0.astype(np_int_type)
    f_exp_bits = np_int_type(8)
    f_frac_bits = np_int_type(23)
    i_width = f_exp_bits + f_frac_bits + 1
    f_exp_offset = 2 ** (f_exp_bits - 1) - 1
    bl = bit_length(inp)
    i = inp << (i_width - bl).astype(np_int_type)
    i = i >> np_int_type(f_exp_bits)
    i = i & np_int_type(2**f_frac_bits - 1)
    fpbits = (
        (f_exp_offset - i_width + bl - 1).astype(np_int_type)
        * (inp > 0).astype(np_int_type)
        << f_frac_bits
    ) | i
    return fpbits


@numba.jit(parallel=True)
def int32_to_fp16_uniform(i0):
    np_int_type = numpy.uint16
    inp = (i0 >> numpy.uint32(16)).astype(np_int_type)
    f_exp_bits = np_int_type(5)
    f_frac_bits = np_int_type(10)
    i_width = f_exp_bits + f_frac_bits + 1
    f_exp_offset = 2 ** (f_exp_bits - 1) - 1
    bl = bit_length(inp)
    i = inp << (i_width - bl).astype(np_int_type)
    i = i >> np_int_type(f_exp_bits)
    i = i & np_int_type(2**f_frac_bits - 1)
    fpbits = (
        (f_exp_offset - i_width + bl - 1).astype(np_int_type)
        * (inp > 0).astype(np_int_type)
        << f_frac_bits
    ) | i
    return fpbits


@numba.jit(parallel=True)
def int32_to_bf16_uniform(i0):
    np_int_type = numpy.uint16
    inp = (i0 >> numpy.uint32(16)).astype(np_int_type)
    f_exp_bits = np_int_type(8)
    f_frac_bits = np_int_type(7)
    i_width = f_exp_bits + f_frac_bits + 1
    f_exp_offset = 2 ** (f_exp_bits - 1) - 1
    bl = bit_length(inp)
    i = inp << (i_width - bl).astype(np_int_type)
    i = i >> np_int_type(f_exp_bits)
    i = i & np_int_type(2**f_frac_bits - 1)
    fpbits = (
        (f_exp_offset - i_width + bl - 1).astype(np_int_type)
        * (inp > 0).astype(np_int_type)
        << f_frac_bits
    ) | i
    return fpbits


def int_to_unif01_float(i, dtype):
    dtype = torch.float32

    f_exp_bits, f_frac_bits, np_int_type = float_info[dtype]
    i_width = f_exp_bits + f_frac_bits + 1

    i = np_int_type((2**60) >> 32)

    f_exp_offset = 2 ** (f_exp_bits - 1) - 1
    if i > 0:
        bl = bit_length(i)

        if bl < i_width:
            i = i << np_int_type(i_width - i)
        i = i >> np_int_type(11)
        i = i & np_int_type(2**f_frac_bits - 1)
        fpbits = np_int_type((f_exp_offset - i_width + bl - 1) << f_frac_bits) | i
    else:
        fpbits = np_int_type(0)

    torch.frombuffer(np_int_type(fpbits).tobytes(), dtype=dtype)


@numba.cuda.jit(device=True)
def cu_random_entry(key0: numba.uint32, key1: numba.uint32, idx: numba.uint64, shape):
    # this assumes that the last dim is the fastest moving
    for d in range(shape.size - 1, -1, -1):
        n = shape[d]
        idx_in_d = idx % n
        idx //= n
        if idx_in_d > 0:
            key0, key1 = cu_threefry2x32(
                key0, key1, numba.uint32(idx_in_d), numba.uint32(shape.size - 1 - d)
            )
    return key0, key1


def bit_length(inp):
    r = ((inp > 0xFFFFFFFF) << 5).astype(numpy.uint64)
    v = inp >> r
    shift = ((v > 0xFFFF) << 4).astype(numpy.uint64)
    v >>= shift
    r |= shift
    shift = ((v > 0xFF) << 3).astype(numpy.uint64)
    v >>= shift
    r |= shift
    shift = ((v > 0xF) << 2).astype(numpy.uint64)
    v >>= shift
    r |= shift
    shift = ((v > 0x3) << 1).astype(numpy.uint64)
    v >>= shift
    r |= shift
    return (r | (v >> numpy.uint64(1))) + (inp > 0).astype(numpy.uint64)


# todo: cuda has clz
@numba.cuda.jit(device=True)
def cu_bit_length(i):
    return 64 - numba.cuda.clz(numba.uint64(i))


def make_rand(dtype, device):
    # (f_exp_bits, f_frac_bits, unsigned numpy dtype of bitlen, int32x2toint<foo>)
    def uint32x2_to_uint64(r0: numba.uint32, r1: numba.uint32) -> numba.uint64:
        return (numba.uint64(r0) << numba.uint64(32)) + numba.uint64(r1)

    def uint32x2_to_uint32(r0: numba.uint32, r1: numba.uint32) -> numba.uint32:
        return numba.uint32(r0)

    def uint32x2_to_uint16(r0: numba.uint32, r1: numba.uint32) -> numba.uint16:
        return numba.uint16(r0 >> 16)

    float_info = {
        torch.float64: (11, 52, numpy.uint64, torch.uint64, uint32x2_to_uint64),
        torch.float32: (8, 23, numpy.uint32, torch.uint32, uint32x2_to_uint32),
        torch.float16: (5, 10, numpy.uint16, torch.uint32, uint32x2_to_uint16),
        torch.bfloat16: (8, 7, numpy.uint16, torch.uint32, uint32x2_to_uint16),
    }
    f_exp_bits, f_frac_bits, np_int_type, torch_int_type, int32x2topbits = float_info[
        dtype
    ]

    if device == "cuda":
        bit_length_fn = cu_bit_length
        jit = numba.cuda.jit(device=True)
    else:
        bit_length_fn = bit_length
        jit = numba.jit(parallel=True)

    int32x2topbits = jit(int32x2topbits)

    @jit
    def int32x2_to_unif01_float(x0: numba.uint32, x1: numba.uint32) -> np_int_type:
        inp = np_int_type(int32x2topbits(x0, x1))
        i_width = f_exp_bits + f_frac_bits + 1
        f_exp_offset = 2 ** (f_exp_bits - 1) - 1
        bl = bit_length_fn(np_int_type(inp))
        i = inp << np_int_type(i_width - bl)
        i = i >> np_int_type(f_exp_bits)
        i = i & np_int_type(2**f_frac_bits - 1)
        fpbits = (
            np_int_type(f_exp_offset - i_width + bl - 1) * np_int_type(inp > 0)
            << f_frac_bits
        ) | i
        return np_int_type(fpbits)

    if device == "cuda":

        @numba.cuda.jit
        def cu_rand_kernel(key0: numba.uint32, key1: numba.uint32, shape, out):
            thread_idx = numba.cuda.grid(1)
            num_threads = numba.cuda.gridsize(1)

            for item_idx in range(thread_idx, out.size, num_threads):
                r0, r1 = cu_random_entry(key0, key1, item_idx, shape)
                out[item_idx] = int32x2_to_unif01_float(r0, r1)

        def cu_rand(key0, key1, out_d):
            # stream?
            # key0 = numpy.array(key0, dtype=numpy.uint32)
            # key1 = numpy.array(key1, dtype=numpy.uint32)
            # inp0 = numpy.array((20342,), dtype=numpy.uint32)
            # inp1 = numpy.array((134345,), dtype=numpy.uint32)
            # nkey0, nkey1 = arr_threefry2x32(key0, key1, inp0, inp1)
            shape = out_d.shape
            shape_d = numba.cuda.to_device(numpy.array(shape, dtype=numpy.uint32))

            nkey0 = numpy.uint32(int(key0))
            nkey1 = numpy.uint32(int(key1))
            threadsperblock = (256,)
            blockspergrid = (256,)
            out_d_arg = out_d.view(torch_int_type).ravel()
            cu_rand_kernel[blockspergrid, threadsperblock](
                nkey0, nkey1, shape_d, out_d_arg
            )
            return out_d

        return cu_rand
    elif device == "cpu":

        def rand(key0, key1, out):
            r0, r1 = random_array(key0, key1, out.shape)
            out[:] = torch.from_numpy(int32x2_to_unif01_float(r0, r1)).view(out.dtype)

        return rand

    # torch.frombuffer(np_int_type(fpbits).tobytes(), dtype=dtype)


# TODO: what's faster, a nested lookup or a lookup of a tuple?
rand_dispatch_dict = {
    "cuda": {k: make_rand(k, "cuda") for k in (torch.float64, torch.float32)},
    "cpu": {k: make_rand(k, "cpu") for k in (torch.float64, torch.float32)},
}


def split(key0, key1):
    key0 = numpy.array(key0, dtype=numpy.uint32)
    key1 = numpy.array(key1, dtype=numpy.uint32)
    out0, out1 = random_array(key0, key1, shape=(2,))
    inp0 = numpy.array((3, 4), dtype=numpy.uint32)
    inp1 = numpy.array((5, 6), dtype=numpy.uint32)
    nkey0, nkey1 = arr_threefry2x32(key0, key1, inp0, inp1)
    return tuple(nkey0), tuple(nkey1)


class RandomGenerator:
    def __init__(self, seed: int | None = None):
        self.lock = threading.Lock()
        if seed is None:
            seed = time.time_ns()
        self.seed(seed)

    def seed(self, seed: int):
        """seeds the RNG with up to 64 bits from int seed"""
        with self.lock:
            key1 = numpy.uint32((seed & (2**32 - 1)))
            key0 = numpy.uint32((seed >> 32) & (2**32 - 1))
            (self.key0, self.key1), _ = split(key0, key1)

    def branch(self):
        with self.lock:
            (self.key0, self.key1), (b0, b1) = split(self.key0, self.key1)
        return b0, b1


default_rng = RandomGenerator()

rand_ops = set()
rand_ops_overloads = set()
for opname in dir(torch.ops.aten):
    op = getattr(torch.ops.aten, opname)
    if isinstance(op, torch._ops.OpOverloadPacket):
        overload_names = op.overloads()
        for oname in overload_names:
            overload = getattr(op, oname)
            for arg in overload._schema.arguments:
                if (
                    "Generator" in arg.type.annotation_str
                ):  # Optional[Generator] or Generator mostly?
                    rand_ops.add(op)
                    rand_ops_overloads.add(overload)

rand_ops_overloads_all = set()
for op in rand_ops:
    for ovn in op.overloads():
        overload = getattr(op, ovn)
        # print(f"torch.ops.{overload}")
        rand_ops_overloads_all.add(overload)

# print('\n'.join(sorted([f'  torch.ops.{str(o)}: not_implemented_overload(torch.ops.{str(o)}),' for o in rand_ops_overloads_all])))


def not_implemented_overload(overload):
    def fn(*args, **kwargs):
        raise NotImplementedError(
            f"not implemented: random function {overload._schema}, called with {args=}, {kwargs=}"
        )

    return fn


def randn_default(*args, **kwargs):
    res = torch.empty(*args, **kwargs)
    normal_(res)
    return res


def normal_(
    self: torch.Tensor,
    mean: float = 0.0,
    std: float = 1.0,
    *,
    generator: torch.Generator | None = None,
):
    if self.device.type == "cpu":
        print("CPU")
    elif self.device.type == "cuda":
        print("CUDA")
    else:
        raise NotImplementedError(f"normal_ not implemented for Tensor on {device=}")


# size is symint...
# TODO: it might be much more pleasant to use an "out" kernel as default
def rand(
    size: list[int],
    *,
    dtype: torch.dtype | None = None,
    layout: torch.layout | None = None,
    device: torch.device | None = None,
    pin_memory: bool | None = None,
):
    # if device is None:

    out = torch.empty(
        size, dtype=dtype, device=device, pin_memory=pin_memory, layout=layout
    )
    fn = rand_dispatch_dict.get(out.device.type, {}).get(out.dtype)
    if fn is None:
        raise NotImplementedError(f"rand with {device=} {dtype=}")
    k0, k1 = default_rng.branch()
    fn(k0, k1, out)
    return out


def uniform(
    self: torch.Tensor,
    _from: float = 0.0,
    to: float = 1.0,
    *,
    generator: torch.Generator | None = None,
    out: torch.Tensor = None,
):
    if out is None:
        out = self.empty_like()
    elif out.shape != self.shape:
        out.resize_as_(self)
    rnd_dtype = (
        torch.float64
        if (out.dtype.itemsize > 4 * (1 if not out.dtype.is_complex else 2))
        else torch.float32
    )
    # todo: do integated kernel instead of copy_, complex uses real and imag both from from...to ...
    rnd = rand(out.shape, dtype=rnd_dtype, device=out.device)
    out.copy_(rnd * (to - _from) + _from)
    if out.dtype.is_complex:
        out += rnd * ((to - _from) * 1j) + (_from * 1j)
    return out


def uniform_(
    self: torch.Tensor,
    _from: float = 0,
    to: float = 1,
    *,
    generator: torch.Generator | None = None,
):
    return uniform(self, _from, to, generator=generator, out=self)
    # TODO: do an out kernel


rand_ops_overrides = {
    torch.ops.aten._fused_dropout.default: not_implemented_overload(
        torch.ops.aten._fused_dropout.default
    ),
    torch.ops.aten._fused_dropout.out: not_implemented_overload(
        torch.ops.aten._fused_dropout.out
    ),
    torch.ops.aten.bernoulli.Tensor: not_implemented_overload(
        torch.ops.aten.bernoulli.Tensor
    ),
    torch.ops.aten.bernoulli.Tensor_out: not_implemented_overload(
        torch.ops.aten.bernoulli.Tensor_out
    ),
    torch.ops.aten.bernoulli.default: not_implemented_overload(
        torch.ops.aten.bernoulli.default
    ),
    torch.ops.aten.bernoulli.float_out: not_implemented_overload(
        torch.ops.aten.bernoulli.float_out
    ),
    torch.ops.aten.bernoulli.out: not_implemented_overload(
        torch.ops.aten.bernoulli.out
    ),
    torch.ops.aten.bernoulli.p: not_implemented_overload(torch.ops.aten.bernoulli.p),
    torch.ops.aten.bernoulli_.Tensor: not_implemented_overload(
        torch.ops.aten.bernoulli_.Tensor
    ),
    torch.ops.aten.bernoulli_.float: not_implemented_overload(
        torch.ops.aten.bernoulli_.float
    ),
    torch.ops.aten.cauchy.default: not_implemented_overload(
        torch.ops.aten.cauchy.default
    ),
    torch.ops.aten.cauchy.out: not_implemented_overload(torch.ops.aten.cauchy.out),
    torch.ops.aten.cauchy_.default: not_implemented_overload(
        torch.ops.aten.cauchy_.default
    ),
    torch.ops.aten.exponential.default: not_implemented_overload(
        torch.ops.aten.exponential.default
    ),
    torch.ops.aten.exponential.out: not_implemented_overload(
        torch.ops.aten.exponential.out
    ),
    torch.ops.aten.exponential_.default: not_implemented_overload(
        torch.ops.aten.exponential_.default
    ),
    torch.ops.aten.geometric.default: not_implemented_overload(
        torch.ops.aten.geometric.default
    ),
    torch.ops.aten.geometric.out: not_implemented_overload(
        torch.ops.aten.geometric.out
    ),
    torch.ops.aten.geometric_.default: not_implemented_overload(
        torch.ops.aten.geometric_.default
    ),
    torch.ops.aten.log_normal.default: not_implemented_overload(
        torch.ops.aten.log_normal.default
    ),
    torch.ops.aten.log_normal.out: not_implemented_overload(
        torch.ops.aten.log_normal.out
    ),
    torch.ops.aten.log_normal_.default: not_implemented_overload(
        torch.ops.aten.log_normal_.default
    ),
    torch.ops.aten.multinomial.default: not_implemented_overload(
        torch.ops.aten.multinomial.default
    ),
    torch.ops.aten.multinomial.out: not_implemented_overload(
        torch.ops.aten.multinomial.out
    ),
    torch.ops.aten.normal.Tensor_Tensor: not_implemented_overload(
        torch.ops.aten.normal.Tensor_Tensor
    ),
    torch.ops.aten.normal.Tensor_Tensor_out: not_implemented_overload(
        torch.ops.aten.normal.Tensor_Tensor_out
    ),
    torch.ops.aten.normal.Tensor_float: not_implemented_overload(
        torch.ops.aten.normal.Tensor_float
    ),
    torch.ops.aten.normal.Tensor_float_out: not_implemented_overload(
        torch.ops.aten.normal.Tensor_float_out
    ),
    torch.ops.aten.normal.float_Tensor: not_implemented_overload(
        torch.ops.aten.normal.float_Tensor
    ),
    torch.ops.aten.normal.float_Tensor_out: not_implemented_overload(
        torch.ops.aten.normal.float_Tensor_out
    ),
    torch.ops.aten.normal.float_float: not_implemented_overload(
        torch.ops.aten.normal.float_float
    ),
    torch.ops.aten.normal.float_float_out: not_implemented_overload(
        torch.ops.aten.normal.float_float_out
    ),
    torch.ops.aten.normal.out: not_implemented_overload(torch.ops.aten.normal.out),
    torch.ops.aten.normal_.default: not_implemented_overload(
        torch.ops.aten.normal_.default
    ),
    torch.ops.aten.rand.default: not_implemented_overload(torch.ops.aten.rand.default),
    torch.ops.aten.rand.generator: not_implemented_overload(
        torch.ops.aten.rand.generator
    ),
    torch.ops.aten.rand.generator_out: not_implemented_overload(
        torch.ops.aten.rand.generator_out
    ),
    torch.ops.aten.rand.generator_with_names: not_implemented_overload(
        torch.ops.aten.rand.generator_with_names
    ),
    torch.ops.aten.rand.generator_with_names_out: not_implemented_overload(
        torch.ops.aten.rand.generator_with_names_out
    ),
    torch.ops.aten.rand.names: not_implemented_overload(torch.ops.aten.rand.names),
    torch.ops.aten.rand.names_out: not_implemented_overload(
        torch.ops.aten.rand.names_out
    ),
    torch.ops.aten.rand.out: not_implemented_overload(torch.ops.aten.rand.out),
    torch.ops.aten.randint.default: not_implemented_overload(
        torch.ops.aten.randint.default
    ),
    torch.ops.aten.randint.generator: not_implemented_overload(
        torch.ops.aten.randint.generator
    ),
    torch.ops.aten.randint.generator_out: not_implemented_overload(
        torch.ops.aten.randint.generator_out
    ),
    torch.ops.aten.randint.low: not_implemented_overload(torch.ops.aten.randint.low),
    torch.ops.aten.randint.low_generator: not_implemented_overload(
        torch.ops.aten.randint.low_generator
    ),
    torch.ops.aten.randint.low_generator_out: not_implemented_overload(
        torch.ops.aten.randint.low_generator_out
    ),
    torch.ops.aten.randint.low_out: not_implemented_overload(
        torch.ops.aten.randint.low_out
    ),
    torch.ops.aten.randint.out: not_implemented_overload(torch.ops.aten.randint.out),
    torch.ops.aten.randn.default: not_implemented_overload(
        torch.ops.aten.randn.default
    ),
    torch.ops.aten.randn.generator: not_implemented_overload(
        torch.ops.aten.randn.generator
    ),
    torch.ops.aten.randn.generator_out: not_implemented_overload(
        torch.ops.aten.randn.generator_out
    ),
    torch.ops.aten.randn.generator_with_names: not_implemented_overload(
        torch.ops.aten.randn.generator_with_names
    ),
    torch.ops.aten.randn.generator_with_names_out: not_implemented_overload(
        torch.ops.aten.randn.generator_with_names_out
    ),
    torch.ops.aten.randn.names: not_implemented_overload(torch.ops.aten.randn.names),
    torch.ops.aten.randn.names_out: not_implemented_overload(
        torch.ops.aten.randn.names_out
    ),
    torch.ops.aten.randn.out: not_implemented_overload(torch.ops.aten.randn.out),
    torch.ops.aten.randperm.default: not_implemented_overload(
        torch.ops.aten.randperm.default
    ),
    torch.ops.aten.randperm.generator: not_implemented_overload(
        torch.ops.aten.randperm.generator
    ),
    torch.ops.aten.randperm.generator_out: not_implemented_overload(
        torch.ops.aten.randperm.generator_out
    ),
    torch.ops.aten.randperm.out: not_implemented_overload(torch.ops.aten.randperm.out),
    torch.ops.aten.rrelu_with_noise.default: not_implemented_overload(
        torch.ops.aten.rrelu_with_noise.default
    ),
    torch.ops.aten.rrelu_with_noise.out: not_implemented_overload(
        torch.ops.aten.rrelu_with_noise.out
    ),
    torch.ops.aten.rrelu_with_noise_.default: not_implemented_overload(
        torch.ops.aten.rrelu_with_noise_.default
    ),
    torch.ops.aten.uniform.default: not_implemented_overload(
        torch.ops.aten.uniform.default
    ),
    torch.ops.aten.uniform.out: not_implemented_overload(torch.ops.aten.uniform.out),
    torch.ops.aten.uniform_.default: uniform_,
}


class AlternativeRandom(TorchDispatchMode):
    def __torch_dispatch__(
        self,
        func,
        types,
        args=(),
        kwargs=None,
    ):
        if kwargs is None:
            kwargs = {}
        override = rand_ops_overrides.get(func)
        if override is not None:
            return override(*args, **kwargs)
        return func(*args, **kwargs)


if 0:
    while True:
        k0, k1 = default_rng.branch()
        x0, x1 = random_array(k0, k1, (16, 16, 16, 16, 16))
        sys.stdout.buffer.write(x0.tobytes())
        sys.stdout.buffer.write(x1.tobytes())


if 0:
    x1 = rand32(0, 10, (10, 10))
    x2 = rand32(0, 10, (1024, 1024))
    x2_64 = rand64(0, 10, (1024, 1024))
    x2_16 = rand16(0, 10, (1024, 1024))

if 0:
    x0, x1 = random_array(0, 10, (16, 16, 64, 64, 128))
    x0.tofile("my0.bin")
    x1.tofile("my1.bin")
    # del x0, x1

    # x0, x1 = random_array(3912842007, 31661381, (128 * 1024 * 1024,))
    # x0.tofile('my2.bin')
    # x1.tofile('my3.bin')
