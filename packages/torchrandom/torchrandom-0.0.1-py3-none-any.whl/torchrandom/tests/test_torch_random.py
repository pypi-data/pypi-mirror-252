# This is taken form PyTorch (~2.2)
# (c) by the PyTorch contributors, see
# https://github.com/pytorch/pytorch/blob/main/LICENSE
# for the license
import torch
import torch.utils.data
import numpy as np
from random_hacks import AlternativeRandom

import contextlib
import gc
import io
import inspect
import itertools
import math
import random
import re
import copy
import os
import tempfile
import unittest
import warnings
import types
import pickle
import textwrap
import subprocess
import weakref
import sys
from torch import inf, nan
from itertools import product, combinations, permutations
from functools import partial
from torch import multiprocessing as mp
from torch.testing import make_tensor

from torch.testing._internal.common_utils import (  # type: ignore[attr-defined]
    TEST_WITH_TORCHINDUCTOR,
    TestCase,
    TEST_WITH_ROCM,
    run_tests,
    IS_JETSON,
    IS_WINDOWS,
    IS_FILESYSTEM_UTF8_ENCODING,
    NO_MULTIPROCESSING_SPAWN,
    IS_SANDCASTLE,
    IS_FBCODE,
    IS_REMOTE_GPU,
    skipIfTorchInductor,
    load_tests,
    slowTest,
    slowTestIf,
    TEST_WITH_CROSSREF,
    skipIfTorchDynamo,
    skipRocmIfTorchInductor,
    set_default_dtype,
    skipCUDAMemoryLeakCheckIf,
    BytesIOContext,
    skipIfRocm,
    skipIfNoSciPy,
    TemporaryFileName,
    TemporaryDirectoryName,
    wrapDeterministicFlagAPITest,
    DeterministicGuard,
    CudaSyncGuard,
    skipIfNotRegistered,
    bytes_to_scalar,
    parametrize,
    skipIfMps,
    noncontiguous_like,
    AlwaysWarnTypedStorageRemoval,
)
from multiprocessing.reduction import ForkingPickler
from torch.testing._internal.common_device_type import (
    expectedFailureMeta,
    expectedFailureXLA,
    instantiate_device_type_tests,
    onlyCUDA,
    onlyCPU,
    dtypes,
    dtypesIfCUDA,
    dtypesIfCPU,
    deviceCountAtLeast,
    skipMeta,
    PYTORCH_CUDA_MEMCHECK,
    largeTensorTest,
    onlyNativeDeviceTypes,
    get_all_device_types,
    skipXLA,
)
from typing import Tuple
import torch.backends.quantized
import torch.testing._internal.data
from torch.testing._internal.common_cuda import (
    tf32_on_and_off,
    tf32_is_not_fp32,
    TEST_CUDNN,
)
from torch.testing._internal.common_dtype import (
    floating_types_and,
    get_all_math_dtypes,
    all_types_and_complex_and,
    complex_types,
    all_types_and,
    floating_types,
    floating_and_complex_types,
    integral_types_and,
    get_all_qint_dtypes,
)

ar = AlternativeRandom()
ar.__enter__()


# and tests/distributions
class TestRandom(TestCase):
    @dtypes(*floating_types_and(torch.half, torch.bfloat16))
    @skipIfMps
    def test_log_normal(self, device, dtype):
        a = torch.tensor([10], dtype=dtype, device=device).log_normal_()
        self.assertEqual(a.dtype, dtype)
        self.assertEqual(a.size(), torch.Size([1]))

    @dtypes(*all_types_and(torch.half, torch.bfloat16))
    @skipIfMps
    def test_geometric(self, device, dtype):
        a = torch.tensor([10], dtype=dtype, device=device).geometric_(0.5)
        self.assertEqual(a.dtype, dtype)
        self.assertEqual(a.size(), torch.Size([1]))

    @dtypes(*floating_types())
    @dtypesIfCPU(*floating_types_and(torch.bfloat16, torch.half))
    @dtypesIfCUDA(*floating_types_and(torch.half))
    def test_bernoulli_p(self, device, dtype):
        for trivial_p in ([0, 1], [1, 0, 1, 1, 0, 1]):
            x = torch.tensor(trivial_p, dtype=dtype, device=device)
            self.assertEqual(x.bernoulli().tolist(), trivial_p)

        def isBinary(t):
            return torch.ne(t, 0).mul_(torch.ne(t, 1)).sum().item() == 0

        p = torch.rand(5, 5, dtype=dtype, device=device)
        self.assertTrue(isBinary(p.bernoulli()))

        p = torch.rand(5, dtype=dtype, device=device).expand(5, 5)
        self.assertTrue(isBinary(p.bernoulli()))

        p = torch.rand(5, 5, dtype=dtype, device=device)
        torch.bernoulli(torch.rand_like(p), out=p)
        self.assertTrue(isBinary(p))

    # RngUniform not implemented for Integral type in XLA test
    @dtypes(*floating_types())
    @dtypesIfCPU(*all_types_and(torch.bool, torch.half))
    @dtypesIfCUDA(*all_types_and(torch.bool, torch.half))
    def test_bernoulli_self(self, device, dtype):
        def isBinary(t):
            return torch.ne(t, 0).mul_(torch.ne(t, 1)).sum().item() == 0

        t = torch.empty(10, 10, dtype=dtype, device=device)

        t.fill_(2)
        t.bernoulli_(0.5)
        self.assertTrue(isBinary(t))

        for p_dtype in floating_types_and(
            *[torch.half] if device.startswith("cuda") else []
        ):
            p = torch.rand(10, dtype=p_dtype, device=device).expand(10, 10)
            t.fill_(2)
            t.bernoulli_(p)
            self.assertTrue(isBinary(t))

            t.fill_(2)
            torch.bernoulli(torch.rand_like(t, dtype=p_dtype), out=t)
            self.assertTrue(isBinary(t))

            t.fill_(2)
            t.bernoulli_(torch.rand_like(t, dtype=p_dtype))
            self.assertTrue(isBinary(t))

    @slowTest
    @dtypes(*floating_types_and(torch.half))
    @dtypesIfCUDA(*floating_types_and(torch.half))
    def test_bernoulli_edge_cases(self, device, dtype):
        # Need to draw a lot of samples to cover every random floating point number.
        a = torch.zeros(
            10000, 10000, dtype=dtype, device=device
        )  # probability of drawing "1" is 0
        num_ones = (torch.bernoulli(a) == 1).sum()
        self.assertEqual(num_ones, 0)

        b = torch.ones(
            10000, 10000, dtype=dtype, device=device
        )  # probability of drawing "1" is 1
        num_zeros = (torch.bernoulli(b) == 0).sum()
        self.assertEqual(num_zeros, 0)

    @dtypes(*floating_types_and(torch.half, torch.bfloat16))
    @skipIfMps
    def test_exponential(self, device, dtype):
        a = torch.tensor([10], dtype=dtype, device=device).exponential_(0.5)
        self.assertEqual(a.dtype, dtype)
        self.assertEqual(a.size(), torch.Size([1]))

        # Tests extremal behavior
        t = torch.empty((1,), device=device, dtype=dtype).exponential_(float("inf"))
        self.assertTrue(t.item() == 0)

        # Tests that negative lambda fails
        with self.assertRaises(RuntimeError):
            torch.empty((1,), device=device, dtype=dtype).exponential_(-0.5)

    @onlyCUDA
    @dtypes(torch.half, torch.float)
    def test_exponential_no_zero(self, device, dtype):
        # naively, 0 in exponential can be generated with probability 2^-24
        # so we need more samples to check if it's not generated
        # instead of doing one
        # don't test CPU, that would be a long test
        x = torch.empty(50000000, device=device, dtype=dtype).exponential_()
        self.assertTrue(x.min() > 0)

    @skipIfNoSciPy
    @dtypes(*floating_types_and(torch.half, torch.bfloat16))
    def test_uniform_kstest(self, device, dtype):
        from scipy import stats

        size = 1000
        for from_ in [-42, 0, 4.2]:
            for to_ in [-4.2, 0, 42]:
                if to_ > from_:
                    t = torch.empty(size, dtype=dtype, device=device).uniform_(
                        from_, to_
                    )
                    res = stats.kstest(
                        t.cpu().to(torch.double), "uniform", args=(from_, (to_ - from_))
                    )
                    self.assertTrue(res.statistic < 0.1)

    @skipIfNoSciPy
    @dtypes(*floating_types_and(torch.half))
    @dtypesIfCUDA(*floating_types_and(torch.half, torch.bfloat16))
    def test_normal_kstest(self, device, dtype):
        from scipy import stats

        size = 1000
        for mean in [-10, 0, 50]:
            for std in [1, 5, 10]:
                t = torch.empty(size, dtype=dtype, device=device).normal_(
                    mean=mean, std=std
                )
                res = stats.kstest(t.cpu().to(torch.double), "norm", args=(mean, std))
                self.assertTrue(res.statistic < 0.1)

    @skipIfMps
    @skipIfNoSciPy
    @skipRocmIfTorchInductor
    @dtypes(*floating_types_and(torch.half, torch.bfloat16))
    def test_lognormal_kstest(self, device, dtype):
        from scipy import stats

        size = 1000
        for mean in [-3, 0, 7]:
            for std in [1, 5, 7]:
                t = torch.empty(size, dtype=dtype, device=device).log_normal_(
                    mean=mean, std=std
                )
                res = stats.kstest(
                    t.cpu().to(torch.double), "lognorm", args=(std, 0, math.exp(mean))
                )
                if dtype == torch.half:
                    self.assertTrue(res.statistic < 0.3)
                else:
                    self.assertTrue(res.statistic < 0.1)

    @skipIfMps
    @skipIfNoSciPy
    @dtypes(*floating_types_and(torch.half, torch.bfloat16))
    def test_exponential_kstest(self, device, dtype):
        from scipy import stats

        size = 1000
        for lambd in [0.5, 1.0, 5.0]:
            t = torch.empty(size, dtype=dtype, device=device).exponential_(lambd=lambd)
            res = stats.kstest(
                t.cpu().to(torch.double),
                "expon",
                args=(
                    0,
                    1 / lambd,
                ),
            )
            self.assertTrue(res.statistic < 0.1)

    @skipIfMps
    @skipIfNoSciPy
    @skipRocmIfTorchInductor
    @dtypes(*floating_types_and(torch.half, torch.bfloat16))
    def test_cauchy_kstest(self, device, dtype):
        from scipy import stats

        size = 1000
        for median in [-10, 0, 50]:
            for sigma in [0.5, 1.0, 10.0]:
                t = torch.empty(size, dtype=dtype, device=device).cauchy_(
                    median=median, sigma=sigma
                )
                res = stats.kstest(
                    t.cpu().to(torch.double), "cauchy", args=(median, sigma)
                )
                self.assertTrue(res.statistic < 0.1)

    @slowTest
    @onlyCUDA
    @dtypes(torch.bfloat16, torch.float32)
    def test_cauchy_no_inf(self, device, dtype):
        # torch.float16 will have `inf` because of its smaller range.
        for _ in range((2**16) * 2):
            x = torch.empty((2**16), dtype=dtype, device=device)
            x.cauchy_()
            self.assertFalse(x.isinf().sum())

    @dtypes(*floating_types_and(torch.half, torch.bfloat16))
    def test_cauchy(self, device, dtype):
        a = torch.tensor([10], dtype=dtype, device=device).cauchy_(0.0, 0.5)
        self.assertEqual(a.dtype, dtype)
        self.assertEqual(a.size(), torch.Size([1]))

        # Tests extremal behavior
        t = torch.empty((1,), device=device, dtype=dtype).cauchy_(float("inf"), 0.5)
        self.assertTrue(t.item() == float("inf"))

        # Tests non-positive rate fails
        with self.assertRaises(RuntimeError):
            torch.empty((1,), device=device, dtype=dtype).cauchy_(0.0, 0.0)

    @skipIfMps
    @skipIfNoSciPy
    @skipRocmIfTorchInductor
    @dtypes(*all_types_and(torch.half, torch.bfloat16))
    def test_geometric_kstest(self, device, dtype):
        from scipy import stats

        size = 1000
        for p in [0.2, 0.5, 0.8]:
            t = torch.empty(size, dtype=dtype, device=device).geometric_(p=p)
            actual = np.histogram(t.cpu().to(torch.double), np.arange(1, 100))[0]
            expected = stats.geom(p).pmf(np.arange(1, 99)) * size
            res = stats.chisquare(actual, expected)
            self.assertEqual(res.pvalue, 1.0, atol=0.1, rtol=0)

    # FIXME: move to test distributions
    @onlyCUDA
    def test_multinomial_device_constrain(self, device):
        x = torch.empty(3, device="cpu")
        y = torch.empty(3, device=device)
        self.assertRaisesRegex(
            RuntimeError,
            "Expected all tensors to be on the same device",
            lambda: torch.multinomial(x, 2, out=y),
        )

    # FIXME: move to test distributions
    @deviceCountAtLeast(2)
    @onlyCUDA
    def test_multinomial_gpu_device_constrain(self, devices):
        x = torch.empty(3, device=devices[0])
        y = torch.empty(3, device=devices[1])
        self.assertRaisesRegex(
            RuntimeError,
            "Expected all tensors to be on the same device",
            lambda: torch.multinomial(x, 2, out=y),
        )

    # FIXME: move to test distributions
    @skipIfMps
    @dtypesIfCUDA(torch.float, torch.double, torch.half)
    @dtypes(torch.float, torch.double, torch.half)
    def test_multinomial(self, device, dtype):
        def make_prob_dist(shape, is_contiguous):
            if is_contiguous:
                if dtype == torch.half:
                    return (
                        torch.zeros(shape, device=device)
                        .uniform_()
                        .to(dtype=torch.half)
                    )
                return torch.zeros(shape, device=device, dtype=dtype).uniform_()
            elif len(shape) == 1:
                if dtype == torch.half:
                    return (
                        torch.zeros((shape + [5]), device=device)
                        .uniform_()
                        .to(dtype=torch.half)[:, 2]
                    )
                return torch.zeros(
                    (shape + [5]), device=device, dtype=dtype
                ).uniform_()[:, 2]
            else:
                # num dim = 2
                new_shape = [2, shape[1], 7, 1, shape[0], 1, 10]
                if dtype == torch.half:
                    prob_dist = (
                        torch.zeros(new_shape, device=device)
                        .uniform_()
                        .to(dtype=torch.half)
                    )
                else:
                    prob_dist = torch.zeros(
                        new_shape, device=device, dtype=dtype
                    ).uniform_()
                prob_dist = prob_dist.transpose(1, 4)
                prob_dist = prob_dist[1, :, 5, 0, :, 0, 4]
                assert not prob_dist.is_contiguous()  # sanity check
                return prob_dist

        for is_contiguous in (True, False):
            # with replacement
            n_row = 3
            for n_col in range(4, 5 + 1):
                prob_dist = make_prob_dist([n_row, n_col], is_contiguous)
                # indices that shouldn't be sampled (<0 means none)
                zero_prob_indices = torch.LongTensor(n_row).random_(-2, n_col).tolist()
                for i, j in enumerate(zero_prob_indices):
                    if j >= 0:
                        prob_dist[i, j] = 0
                n_sample = n_col * 3
                sample_indices = torch.multinomial(prob_dist, n_sample, True)
                self.assertEqual(prob_dist.dim(), 2)
                self.assertEqual(sample_indices.size(1), n_sample)
                for i in range(n_row):
                    zero_prob_idx = zero_prob_indices[i]
                    if zero_prob_idx < 0:
                        continue
                    for j in range(n_sample):
                        self.assertNotEqual(
                            sample_indices[i, j],
                            zero_prob_idx,
                            msg="sampled an index with zero probability",
                        )

            # without replacement
            n_row = 3
            for n_col in range(2, 10 + 1, 2):
                prob_dist = make_prob_dist([n_row, n_col], is_contiguous)
                # indices that shouldn't be sampled (<0 means none)
                zero_prob_indices = torch.LongTensor(n_row).random_(-1, n_col).tolist()
                for i, j in enumerate(zero_prob_indices):
                    if j >= 0:
                        prob_dist[i, j] = 0
                n_sample = max(1, n_col - 2)
                sample_indices = torch.multinomial(prob_dist, n_sample, False)
                self.assertEqual(prob_dist.dim(), 2)
                self.assertEqual(sample_indices.size(1), n_sample)
                for i in range(n_row):
                    row_samples = {}
                    zero_prob_idx = zero_prob_indices[i]
                    for j in range(n_sample):
                        sample_idx = sample_indices[i, j]
                        if zero_prob_idx >= 0:
                            self.assertNotEqual(
                                sample_idx,
                                zero_prob_idx,
                                msg="sampled an index with zero probability",
                            )
                        self.assertNotIn(
                            sample_idx, row_samples, "sampled an index twice"
                        )
                        row_samples[sample_idx] = True

            # vector
            n_col = 4
            prob_dist = make_prob_dist([n_col], is_contiguous).fill_(1)
            zero_prob_idx = 1  # index that shouldn't be sampled
            prob_dist[zero_prob_idx] = 0
            n_sample = 20
            sample_indices = torch.multinomial(prob_dist, n_sample, True)
            for sample_index in sample_indices:
                self.assertNotEqual(
                    sample_index,
                    zero_prob_idx,
                    msg="sampled an index with zero probability",
                )
            s_dim = sample_indices.dim()
            self.assertEqual(sample_indices.dim(), 1, msg="wrong number of dimensions")
            self.assertEqual(
                prob_dist.dim(), 1, msg="wrong number of prob_dist dimensions"
            )
            self.assertEqual(
                sample_indices.size(0), n_sample, msg="wrong number of samples"
            )

        # CUDA misalignment issue (#46702)
        n_row, n_col = 2, 3
        prob_dist = make_prob_dist([n_row, n_col], True)
        n_sample = 1
        sample_indices = torch.multinomial(prob_dist, n_sample, True)
        self.assertEqual(sample_indices.dim(), 2, msg="wrong number of dimensions")
        self.assertEqual(
            sample_indices.size(1), n_sample, msg="wrong number of samples"
        )

    # FIXME: move to test distributions
    @onlyCUDA
    @dtypes(torch.float, torch.double, torch.half)
    def test_multinomial_deterministic(self, device, dtype):
        gen = torch.Generator(device=device)

        trials = 5
        seed = 0
        prob_dist = torch.rand(10000, 1000, device=device, dtype=dtype)
        n_sample = 1

        for i in range(trials):
            gen.manual_seed(seed)
            samples_1 = torch.multinomial(prob_dist, n_sample, True, generator=gen)

            gen.manual_seed(seed)
            samples_2 = torch.multinomial(prob_dist, n_sample, True, generator=gen)

            self.assertEqual(samples_1, samples_2)
            self.assertEqual(samples_1.dim(), 2, msg="wrong number of dimensions")
            self.assertEqual(samples_1.size(1), n_sample, msg="wrong number of samples")

    # FIXME: move to test distributions
    @slowTest
    @dtypes(torch.float)
    def test_multinomial_rng_state_advance(self, device, dtype):
        corpus_size = 100000
        freqs = torch.ones(corpus_size, dtype=torch.float, device=device)
        n_sample = 100
        samples1 = torch.multinomial(freqs, n_sample, replacement=True)
        samples2 = torch.multinomial(freqs, n_sample, replacement=True)
        samples = torch.cat([samples1, samples2])
        # expect no more than 1 repeating elements generated in 2 attempts
        # the probability of at least element being repeated is surprisingly large, 18%
        self.assertLessEqual(2 * n_sample - samples.unique().size(0), 2)
        samples1 = torch.multinomial(freqs, n_sample, replacement=False)
        samples2 = torch.multinomial(freqs, n_sample, replacement=False)
        samples = torch.cat([samples1, samples2])
        # expect no more than 1 repeating elements generated in 2 attempts
        self.assertLessEqual(2 * n_sample - samples.unique().size(0), 1)

    # FIXME: move to test distributions
    def _test_multinomial_empty(self, device, replacement, num_samples):
        probs = torch.ones(0, 3, device=device)
        expected = torch.empty(0, num_samples, dtype=torch.int64)
        out = torch.multinomial(probs, num_samples=num_samples, replacement=replacement)
        self.assertEqual(out, expected)

    # FIXME: move to test distributions
    def test_multinomial_empty_w_replacement(self, device):
        self._test_multinomial_empty(device, True, 1)
        self._test_multinomial_empty(device, True, 2)

    # FIXME: move to test distributions
    def test_multinomial_empty_wo_replacement(self, device):
        self._test_multinomial_empty(device, False, 1)
        self._test_multinomial_empty(device, False, 2)

    @dtypesIfCUDA(torch.float, torch.double, torch.half)
    @dtypesIfCPU(torch.float, torch.double, torch.bfloat16, torch.half)
    @dtypes(torch.float, torch.double)
    def test_multinomial_cpu(self, device, dtype):
        def make_prob_dist(shape, is_contiguous):
            if is_contiguous:
                if dtype == torch.half or dtype == torch.bfloat16:
                    return torch.zeros(shape, device=device).uniform_().to(dtype=dtype)
                return torch.zeros(shape, device=device, dtype=dtype).uniform_()
            elif len(shape) == 1:
                if dtype == torch.half or dtype == torch.bfloat16:
                    return (
                        torch.zeros((shape + [5]), device=device)
                        .uniform_()
                        .to(dtype=dtype)[:, 2]
                    )
                return torch.zeros(
                    (shape + [5]), device=device, dtype=dtype
                ).uniform_()[:, 2]
            else:
                # num dim = 2
                new_shape = [2, shape[1], 7, 1, shape[0], 1, 10]
                if dtype == torch.half or dtype == torch.bfloat16:
                    prob_dist = (
                        torch.zeros(new_shape, device=device).uniform_().to(dtype=dtype)
                    )
                else:
                    prob_dist = torch.zeros(
                        new_shape, device=device, dtype=dtype
                    ).uniform_()
                prob_dist = prob_dist.transpose(1, 4)
                prob_dist = prob_dist[1, :, 5, 0, :, 0, 4]
                assert not prob_dist.is_contiguous()  # sanity check
                return prob_dist

    def test_generator_cpu(self):
        # test default generators are equal
        self.assertEqual(torch.default_generator, torch.default_generator)

        # tests Generator API
        # manual_seed, seed, initial_seed, get_state, set_state
        g1 = torch.Generator()
        g2 = torch.Generator()
        g1.manual_seed(12345)
        g2.manual_seed(12345)
        self.assertEqual(g1.initial_seed(), g2.initial_seed())

        g1.seed()
        g2.seed()
        self.assertNotEqual(g1.initial_seed(), g2.initial_seed())

        g1 = torch.Generator()
        g2_state = g2.get_state()
        g2_randn = torch.randn(1, generator=g2)
        g1.set_state(g2_state)
        g1_randn = torch.randn(1, generator=g1)
        self.assertEqual(g1_randn, g2_randn)

        default_state = torch.default_generator.get_state()
        q = torch.empty(100)
        g1_normal = q.normal_()
        g2 = torch.Generator()
        g2.set_state(default_state)
        g2_normal = q.normal_(generator=g2)
        self.assertEqual(g1_normal, g2_normal)

    def test_invalid_generator_raises(self):
        self.assertRaises(RuntimeError, lambda: torch.Generator("opengl"))

    # FIXME: Put the following random tests into their own test class or test suite
    @skipIfTorchDynamo("requires https://github.com/pytorch/torchdynamo/pull/1098")
    def test_RNGState(self):
        state = torch.get_rng_state()
        stateCloned = state.clone()
        before = torch.rand(1000)

        self.assertEqual(state.ne(stateCloned).long().sum(), 0, atol=0, rtol=0)

        torch.set_rng_state(state)
        after = torch.rand(1000)
        self.assertEqual(before, after, atol=0, rtol=0)

    @skipIfTorchDynamo("requires https://github.com/pytorch/torchdynamo/pull/1098")
    def test_RNGStateAliasing(self):
        # Fork the random number stream at this point
        gen = torch.Generator()
        gen.set_state(torch.get_rng_state())
        self.assertEqual(gen.get_state(), torch.get_rng_state())

        target_value = torch.rand(1000)
        # Dramatically alter the internal state of the main generator
        _ = torch.rand(100000)
        forked_value = torch.rand(1000, generator=gen)
        self.assertEqual(
            target_value,
            forked_value,
            atol=0,
            rtol=0,
            msg="RNG has not forked correctly.",
        )

    @skipIfTorchDynamo("requires https://github.com/pytorch/torchdynamo/pull/1098")
    def test_RNG_after_pickle(self):
        torch.random.manual_seed(100)
        before = torch.rand(10)

        torch.random.manual_seed(100)
        buf = io.BytesIO()
        tensor = torch.tensor([1, 2, 3])
        ForkingPickler(buf, pickle.HIGHEST_PROTOCOL).dump(tensor)
        after = torch.rand(10)

        self.assertEqual(before, after, atol=0, rtol=0)

    @skipIfTorchDynamo("requires https://github.com/pytorch/torchdynamo/pull/1098")
    def test_boxMullerState(self):
        torch.manual_seed(123)
        odd_number = 101
        seeded = torch.randn(odd_number)
        state = torch.get_rng_state()
        midstream = torch.randn(odd_number)
        torch.set_rng_state(state)
        repeat_midstream = torch.randn(odd_number)
        torch.manual_seed(123)
        reseeded = torch.randn(odd_number)
        self.assertEqual(
            midstream,
            repeat_midstream,
            atol=0,
            rtol=0,
            msg="get_rng_state/set_rng_state not generating same sequence of normally distributed numbers",
        )
        self.assertEqual(
            seeded,
            reseeded,
            atol=0,
            rtol=0,
            msg="repeated calls to manual_seed not generating same sequence of normally distributed numbers",
        )

    @skipIfTorchDynamo("requires https://github.com/pytorch/torchdynamo/pull/1098")
    def test_manual_seed(self):
        rng_state = torch.get_rng_state()
        torch.manual_seed(2)
        x = torch.randn(100)
        self.assertEqual(torch.initial_seed(), 2)
        torch.manual_seed(2)
        y = torch.randn(100)
        self.assertEqual(x, y)

        max_int64 = 0x7FFF_FFFF_FFFF_FFFF
        min_int64 = -max_int64 - 1
        max_uint64 = 0xFFFF_FFFF_FFFF_FFFF
        # Check all boundary cases of valid seed value inputs
        test_cases = [
            # (seed, expected_initial_seed)
            # Positive seeds should be unchanged
            (max_int64, max_int64),
            (max_int64 + 1, max_int64 + 1),
            (max_uint64, max_uint64),
            (0, 0),
            # Negative seeds wrap around starting from the largest seed value
            (-1, max_uint64),
            (min_int64, max_int64 + 1),
        ]
        for seed, expected_initial_seed in test_cases:
            torch.manual_seed(seed)
            actual_initial_seed = torch.initial_seed()
            msg = "expected initial_seed() = {:x} after calling manual_seed({:x}), but got {:x} instead".format(
                expected_initial_seed, seed, actual_initial_seed
            )
            self.assertEqual(expected_initial_seed, actual_initial_seed, msg=msg)
        for invalid_seed in [min_int64 - 1, max_uint64 + 1]:
            with self.assertRaisesRegex(RuntimeError, r"Overflow when unpacking long"):
                torch.manual_seed(invalid_seed)

        torch.set_rng_state(rng_state)


instantiate_device_type_tests(TestRandom, globals())

if __name__ == "__main__":
    TestCase._default_dtype_check_enabled = True
    run_tests()
