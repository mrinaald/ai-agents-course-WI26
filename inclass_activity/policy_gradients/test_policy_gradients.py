"""
Unit tests for Policy Gradients implementation.
"""

import torch
import traceback

def _describe_tensor(t):
    if t is None:
        return "None"
    if not isinstance(t, torch.Tensor):
        return f"<{type(t).__name__}> (not a tensor)"
    return f"shape {tuple(t.shape)}, dtype {t.dtype}"


def assert_tensors_close(actual, expected, msg="", atol=1e-6, rtol=1e-5):
    if actual is None:
        raise AssertionError(
            f"{msg}\n  Your result: None (did you return a value?)\n  Expected: {_describe_tensor(expected)}"
        )
    if expected is None:
        raise AssertionError(f"{msg}\n  Expected is None (bug in test).")
    if not isinstance(actual, torch.Tensor):
        raise AssertionError(
            f"{msg}\n  Your result: {type(actual).__name__} (expected a tensor)\n  Expected: {_describe_tensor(expected)}"
        )
    if not isinstance(expected, torch.Tensor):
        raise AssertionError(
            f"{msg}\n  Your result: {_describe_tensor(actual)}\n  Expected: not a tensor (bug in test)"
        )
    if actual.shape != expected.shape:
        raise AssertionError(
            f"{msg}\n  Your result shape: {actual.shape}\n  Expected shape:   {expected.shape}"
        )
    if not torch.allclose(actual, expected, atol=atol, rtol=rtol):
        diff = (actual.float() - expected.float())
        abs_diff = diff.abs()
        total_elements = actual.numel()
        err_lines = [
            msg,
            "",
            "  Comparison (your result vs expected):",
            f"  Your result: {_describe_tensor(actual)}",
            f"  Expected:    {_describe_tensor(expected)}",
        ]
        if total_elements <= 16:
            err_lines.append(f"  Your values:    {actual.tolist()}")
            err_lines.append(f"  Expected values: {expected.tolist()}")
        
        raise AssertionError("\n".join(err_lines))


def test_compute_probability_ratio(func):
    """Test probability ratio computation."""
    print("Testing compute_probability_ratio...")

    try:
        new_logps = torch.tensor([[0.0]])
        old_logps = torch.tensor([[-0.693147]])
        ratio = func(new_logps, old_logps)
        assert_tensors_close(ratio, torch.tensor([[2.0]]), "Ratio should be 2.0", atol=1e-4)

        print("✓ Test passed for compute_probability_ratio")
        return True
    except AssertionError as e:
        print(f"✗ compute_probability_ratio failed:\n{e}")
        return False
    except Exception as e:
        print(f"Error in test_compute_probability_ratio: {e}")
        print(traceback.format_exc())
        return False


def test_compute_policy_gradient_loss(func):
    """Test basic policy gradient loss."""
    print("Testing compute_policy_gradient_loss...")

    try:
        advantages = torch.tensor([[1.0]])
        ratio = torch.tensor([[2.0]])
        loss = func(advantages, ratio)
        if loss is None:
            raise AssertionError(
                "compute_policy_gradient_loss returned None.\n  Did you implement the function and return the loss tensor?"
            )
        assert_tensors_close(loss, torch.tensor([[-2.0]]), "loss should be -advantages*ratio = -2.0")

        print("✓ Test passed for compute_policy_gradient_loss")
        return True
    except AssertionError as e:
        print(f"✗ compute_policy_gradient_loss failed:\n{e}")
        return False
    except Exception as e:
        print(f"Error in test_compute_policy_gradient_loss: {e}")
        print(traceback.format_exc())
        return False


def test_compute_rloo_advantages(func):
    """Test RLOO advantage computation."""
    print("Testing compute_rloo_advantages...")

    try:
        rewards = torch.tensor([1.0, 3.0])
        advantages = func(rewards, rloo_k=2)
        if advantages is None:
            raise AssertionError(
                "compute_rloo_advantages returned None.\n  Did you implement the function and return the advantages tensor?"
            )
        expected = torch.tensor([-2.0, 2.0])
        assert_tensors_close(
            advantages, expected, "RLOO K=2: expected advantages should be [-2, 2]", atol=1e-6,
        )

        print("✓ Test passed for compute_rloo_advantages")
        return True
    except AssertionError as e:
        print(f"✗ compute_rloo_advantages failed:\n{e}")
        return False
    except Exception as e:
        print(f"Error in test_compute_rloo_advantages: {e}")
        print(traceback.format_exc())
        return False


def test_compute_grpo_advantages(func):
    """Test GRPO advantage computation."""
    print("Testing compute_grpo_advantages...")

    try:
        rewards = torch.tensor([1.0, 2.0, 3.0, 10.0, 20.0, 30.0])
        advantages = func(rewards, num_generations=3)
        reshaped = advantages.view(2, 3)
        means = reshaped.mean(dim=1)
        assert_tensors_close(
            means, torch.zeros_like(means),
            "GRPO — mean of advantages per group should be ~0",
            atol=1e-5,
        )
        print("✓ Test passed for compute_grpo_advantages")
        return True
    except AssertionError as e:
        print(f"✗ compute_grpo_advantages failed:\n{e}")
        return False
    except Exception as e:
        print(f"Error in test_compute_grpo_advantages: {e}")
        print(traceback.format_exc())
        return False


def test_compute_returns_monte_carlo(func):
    """Test Monte Carlo returns computation."""
    print("Testing compute_returns_monte_carlo...")

    try:
        rewards = torch.tensor([[1.0, 2.0, 3.0]])
        done_mask = torch.tensor([[0.0, 0.0, 1.0]])
        returns = func(rewards, gamma=1.0, done_mask=done_mask)
        if returns is None:
            raise AssertionError(
                "compute_returns_monte_carlo returned None.\n  Did you implement the function and return the returns tensor?"
            )
        expected = torch.tensor([[6.0, 5.0, 3.0]])
        assert_tensors_close(
            returns, expected,
            "Monte Carlo returns with gamma=1 (sum of future rewards from each step)",
            atol=1e-6,
        )
        
        print("✓ Test passed for compute_returns_monte_carlo")
        return True
    except AssertionError as e:
        print(f"✗ compute_returns_monte_carlo failed:\n{e}")
        return False
    except Exception as e:
        print(f"Error in test_compute_returns_monte_carlo: {e}")
        print(traceback.format_exc())
        return False


def run_all_tests(ratio_fn, loss_fn, rloo_fn, grpo_fn, mc_fn):
    """Run all unit tests."""
    print("=" * 60)
    print("Running Policy Gradients Unit Tests")
    print("=" * 60)
    print()

    tests = [
        (test_compute_probability_ratio, ratio_fn),
        (test_compute_policy_gradient_loss, loss_fn),
        (test_compute_rloo_advantages, rloo_fn),
        (test_compute_grpo_advantages, grpo_fn),
        (test_compute_returns_monte_carlo, mc_fn),
    ]

    passed_count = 0
    total_tests = len(tests)

    for test_func, impl_func in tests:
        if test_func(impl_func):
            passed_count += 1
        print()

    print("=" * 60)
    print(f"Results: {passed_count}/{total_tests} tests passed")
    print("=" * 60)

    return passed_count == total_tests
