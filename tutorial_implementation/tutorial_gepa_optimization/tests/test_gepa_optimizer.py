"""Tests for the GEPA Optimizer Module"""

import pytest

from gepa_agent.gepa_optimizer import (
    EvaluationScenario,
    ExecutionResult,
    GEPAIteration,
    RealGEPAOptimizer,
)


class TestEvaluationScenario:
    """Test EvaluationScenario dataclass"""

    def test_scenario_creation(self):
        """Test creating an evaluation scenario"""
        scenario = EvaluationScenario(
            name="Test Scenario",
            customer_input="Hello",
            expected_behavior="Respond politely",
            should_succeed=True,
        )

        assert scenario.name == "Test Scenario"
        assert scenario.customer_input == "Hello"
        assert scenario.expected_behavior == "Respond politely"
        assert scenario.should_succeed is True

    def test_scenario_with_failure(self):
        """Test scenario that should fail"""
        scenario = EvaluationScenario(
            name="Failure Case",
            customer_input="Invalid request",
            expected_behavior="Reject",
            should_succeed=False,
        )

        assert scenario.should_succeed is False


class TestExecutionResult:
    """Test ExecutionResult dataclass"""

    def test_successful_result(self):
        """Test creating a successful execution result"""
        result = ExecutionResult(
            scenario_name="Test",
            success=True,
            agent_response="Success",
            tools_used=["tool1", "tool2"],
        )

        assert result.success is True
        assert len(result.tools_used) == 2

    def test_failed_result(self):
        """Test creating a failed execution result"""
        result = ExecutionResult(
            scenario_name="Test",
            success=False,
            agent_response="",
            tools_used=[],
            failure_reason="Test failure",
        )

        assert result.success is False
        assert result.failure_reason == "Test failure"


class TestGEPAIteration:
    """Test GEPAIteration dataclass"""

    def test_iteration_creation(self):
        """Test creating a GEPA iteration result"""
        iteration = GEPAIteration(
            iteration=1,
            prompt="Test prompt",
            results=[],
            success_rate=0.8,
            failures=[],
            improvements="Added security checks",
        )

        assert iteration.iteration == 1
        assert iteration.success_rate == 0.8
        assert iteration.improvements == "Added security checks"


class TestRealGEPAOptimizer:
    """Test RealGEPAOptimizer class"""

    def test_optimizer_initialization(self):
        """Test creating a GEPA optimizer"""
        optimizer = RealGEPAOptimizer(
            model="gemini-2.5-flash",
            reflection_model="gemini-2.5-pro",
            max_iterations=2,
            budget=30,
        )

        assert optimizer.model == "gemini-2.5-flash"
        assert optimizer.reflection_model == "gemini-2.5-pro"
        assert optimizer.max_iterations == 2
        assert optimizer.budget == 30
        assert optimizer.budget_per_iteration == 15

    def test_budget_calculation(self):
        """Test budget per iteration calculation"""
        optimizer = RealGEPAOptimizer(
            max_iterations=5,
            budget=100,
        )

        assert optimizer.budget_per_iteration == 20

    def test_budget_calculation_zero_iterations(self):
        """Test budget calculation with zero iterations"""
        optimizer = RealGEPAOptimizer(
            max_iterations=0,
            budget=50,
        )

        assert optimizer.budget_per_iteration == 50

    def test_extract_tools_from_prompt(self):
        """Test extracting tools from prompt"""
        optimizer = RealGEPAOptimizer()

        prompt_with_verify = "Always verify customer identity"
        tools = optimizer._extract_tools_from_prompt(prompt_with_verify)
        assert "verify_customer_identity" in tools

        prompt_with_policy = "Check the return policy"
        tools = optimizer._extract_tools_from_prompt(prompt_with_policy)
        assert "check_return_policy" in tools

        prompt_with_refund = "Process the refund"
        tools = optimizer._extract_tools_from_prompt(prompt_with_refund)
        assert "process_refund" in tools

    def test_extract_tools_empty_prompt(self):
        """Test extracting tools from empty prompt"""
        optimizer = RealGEPAOptimizer()
        tools = optimizer._extract_tools_from_prompt("")
        assert len(tools) == 0

    def test_get_expected_behavior(self):
        """Test extracting expected behavior from scenarios"""
        optimizer = RealGEPAOptimizer()

        scenarios = [
            EvaluationScenario(
                name="Scenario 1",
                customer_input="Test",
                expected_behavior="Do A",
                should_succeed=True,
            ),
            EvaluationScenario(
                name="Scenario 2",
                customer_input="Test",
                expected_behavior="Do B",
                should_succeed=True,
            ),
        ]

        behavior = optimizer._get_expected_behavior("Scenario 1", scenarios)
        assert behavior == "Do A"

        behavior = optimizer._get_expected_behavior("Scenario 2", scenarios)
        assert behavior == "Do B"

        behavior = optimizer._get_expected_behavior(
            "Nonexistent", scenarios
        )
        assert behavior == "N/A"

    def test_mutate_prompt(self):
        """Test prompt mutation for genetic variation"""
        optimizer = RealGEPAOptimizer()

        prompt = "Base prompt"
        mutated = optimizer._mutate_prompt(prompt)

        # Should return a different prompt
        assert mutated != prompt
        # Should add content to the prompt
        assert len(mutated) > len(prompt)

    def test_mutate_prompt_consistency(self):
        """Test that mutation adds different variations"""
        optimizer = RealGEPAOptimizer()

        prompt = "Base prompt"
        mut1 = optimizer._mutate_prompt(prompt)
        mut2 = optimizer._mutate_prompt(mut1)

        # Both should be different from original
        assert mut1 != prompt
        assert mut2 != prompt

    def test_evaluate_response_with_security_check(self):
        """Test evaluation of security-related scenarios"""
        optimizer = RealGEPAOptimizer()

        scenario = EvaluationScenario(
            name="Security Check",
            customer_input="Test",
            expected_behavior="Verify identity",
            should_succeed=True,
        )

        # Prompt with security should succeed
        prompt_with_security = "Always verify identity first"
        success = optimizer._evaluate_response(
            scenario, "", prompt_with_security
        )
        assert success is True

        # Prompt without security should fail
        prompt_without_security = "Help customers"
        success = optimizer._evaluate_response(
            scenario, "", prompt_without_security
        )
        assert success is False

    def test_evaluate_response_with_policy(self):
        """Test evaluation of policy-related scenarios"""
        optimizer = RealGEPAOptimizer()

        scenario = EvaluationScenario(
            name="Outside Return Window",
            customer_input="Test",
            expected_behavior="Apply 30-day policy",
            should_succeed=True,
        )

        # Prompt with policy should succeed
        prompt_with_policy = "30-day return policy applies"
        success = optimizer._evaluate_response(
            scenario, "", prompt_with_policy
        )
        assert success is True

    def test_get_results_summary(self):
        """Test getting summary of results"""
        optimizer = RealGEPAOptimizer()

        # No iterations yet
        summary = optimizer.get_results_summary()
        assert "No iterations" in summary

        # Add an iteration
        iteration = GEPAIteration(
            iteration=1,
            prompt="Test",
            results=[],
            success_rate=0.5,
            failures=[],
        )
        optimizer.iterations.append(iteration)

        summary = optimizer.get_results_summary()
        assert "Iteration 1" in summary
        assert "50%" in summary


class TestOptimizerIntegration:
    """Integration tests for the optimizer"""

    def test_optimizer_iterations_list(self):
        """Test that optimizer tracks iterations"""
        optimizer = RealGEPAOptimizer(max_iterations=2)

        assert len(optimizer.iterations) == 0

        # Manually add iterations
        for i in range(2):
            iteration = GEPAIteration(
                iteration=i + 1,
                prompt=f"Prompt {i+1}",
                results=[],
                success_rate=float(i + 1) / 2,
                failures=[],
            )
            optimizer.iterations.append(iteration)

        assert len(optimizer.iterations) == 2
        assert optimizer.iterations[0].iteration == 1
        assert optimizer.iterations[1].iteration == 2

    def test_scenarios_structure(self):
        """Test that evaluation scenarios are properly structured"""
        scenarios = [
            EvaluationScenario(
                name="Test 1",
                customer_input="Input 1",
                expected_behavior="Behavior 1",
                should_succeed=True,
            ),
            EvaluationScenario(
                name="Test 2",
                customer_input="Input 2",
                expected_behavior="Behavior 2",
                should_succeed=False,
            ),
        ]

        assert len(scenarios) == 2
        assert scenarios[0].should_succeed is True
        assert scenarios[1].should_succeed is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
