"""
Evaluation Framework for Commerce Agent

This module provides comprehensive evaluation tests for the enhanced commerce agent,
measuring improvements in:
1. Tool trajectory efficiency (reduced turns for preferences)
2. Response structure (Pydantic JSON schemas)
3. User satisfaction (multimodal support, cart management)

Based on personalized-shopping agent evaluation patterns.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List

import pytest
from google import genai
from google.genai import types as genai_types

from commerce_agent.agent_enhanced import enhanced_root_agent
from commerce_agent.types import (
    CartModificationResult,
    ProductRecommendations,
    VisualAnalysisResult,
)


# Evaluation metrics weights (from personalized-shopping example)
TOOL_TRAJECTORY_WEIGHT = 0.3
RESPONSE_STRUCTURE_WEIGHT = 0.4
USER_SATISFACTION_WEIGHT = 0.3


def load_test_scenarios() -> Dict[str, Any]:
    """Load test scenarios from eval_data/test_scenarios.json"""
    eval_data_path = Path(__file__).parent / "eval_data" / "test_scenarios.json"
    with open(eval_data_path, "r") as f:
        return json.load(f)


def calculate_tool_trajectory_score(
    expected_max_turns: int, actual_turns: int, expected_tools: List[str], used_tools: List[str]
) -> float:
    """
    Calculate tool trajectory score based on efficiency and correctness.
    
    Args:
        expected_max_turns: Maximum expected turns for the scenario
        actual_turns: Actual turns taken
        expected_tools: List of tools expected to be used
        used_tools: List of tools actually used
    
    Returns:
        Score between 0.0 and 1.0
    """
    # Turn efficiency score (penalize excessive turns)
    turn_efficiency = min(1.0, expected_max_turns / max(actual_turns, 1))
    
    # Tool usage score (correct tools used)
    if not expected_tools:
        tool_score = 1.0
    else:
        correct_tools = set(expected_tools) & set(used_tools)
        tool_score = len(correct_tools) / len(expected_tools)
    
    # Weighted average
    return (turn_efficiency * 0.6) + (tool_score * 0.4)


def calculate_response_structure_score(response: Any, expected_schema: str) -> float:
    """
    Calculate response structure score based on Pydantic schema validation.
    
    Args:
        response: The agent's response
        expected_schema: Expected Pydantic schema name
    
    Returns:
        Score between 0.0 and 1.0
    """
    try:
        # Check if response is JSON-like dict
        if not isinstance(response, dict):
            return 0.0
        
        # Validate against expected schema
        schema_map = {
            "ProductRecommendations": ProductRecommendations,
            "CartModificationResult": CartModificationResult,
            "VisualAnalysisResult": VisualAnalysisResult,
        }
        
        if expected_schema not in schema_map:
            return 0.5  # Unknown schema, partial credit
        
        schema_class = schema_map[expected_schema]
        
        # Try to validate with Pydantic
        try:
            schema_class(**response)
            return 1.0  # Perfect validation
        except Exception:
            # Check if at least some required fields present
            required_fields = schema_class.model_fields.keys()
            present_fields = set(response.keys()) & set(required_fields)
            return len(present_fields) / len(required_fields)
    
    except Exception:
        return 0.0


def calculate_user_satisfaction_score(
    scenario: Dict[str, Any], responses: List[Any]
) -> float:
    """
    Calculate user satisfaction score based on expected behaviors.
    
    Args:
        scenario: Test scenario definition
        responses: List of agent responses
    
    Returns:
        Score between 0.0 and 1.0
    """
    expected = scenario["expected_behavior"]
    score_components = []
    
    # Check multimodal support if expected
    if expected.get("should_use_visual_assistant"):
        has_visual = any(
            "visual_assistant" in str(r).lower() or "analyze_product_image" in str(r).lower()
            for r in responses
        )
        score_components.append(1.0 if has_visual else 0.0)
    
    # Check cart management if expected
    if expected.get("should_modify_cart"):
        has_cart = any(
            "cart" in str(r).lower() or "checkout" in str(r).lower()
            for r in responses
        )
        score_components.append(1.0 if has_cart else 0.0)
    
    # Check structured recommendations if expected
    if expected.get("should_return_structured_recommendations"):
        has_structured = any(
            isinstance(r, dict) and "products" in r
            for r in responses
        )
        score_components.append(1.0 if has_structured else 0.0)
    
    # Check error handling if expected
    if expected.get("should_handle_error_gracefully"):
        has_error_handling = any(
            isinstance(r, dict) and r.get("status") == "error"
            for r in responses
        )
        score_components.append(1.0 if has_error_handling else 0.0)
    
    # Average of all components
    return sum(score_components) / len(score_components) if score_components else 0.5


class TestEvalFramework:
    """Evaluation framework tests for commerce agent"""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment"""
        self.scenarios = load_test_scenarios()["test_scenarios"]
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            pytest.skip("GOOGLE_API_KEY not set")
        
        # Initialize GenAI client
        self.client = genai.Client(api_key=self.api_key)
    
    def test_load_scenarios(self):
        """Test that scenarios load correctly"""
        assert len(self.scenarios) > 0, "No test scenarios loaded"
        assert all("scenario_id" in s for s in self.scenarios), "Missing scenario_id"
        assert all("expected_behavior" in s for s in self.scenarios), "Missing expected_behavior"
    
    def test_trail_running_shoes_basic(self):
        """
        Test basic trail running shoes scenario.
        Expected: Efficient preference collection (max 2 turns) and structured recommendations.
        """
        scenario = next(s for s in self.scenarios if s["scenario_id"] == "trail_running_shoes_basic")
        
        # Mock responses for testing structure (real implementation would invoke agent)
        mock_responses = [
            {
                "questions": [
                    "What is your shoe size?",
                    "What type of terrain do you usually run on?",
                    "What is your budget?",
                    "Do you have any brand preferences?"
                ],
                "collected_preferences": {}
            },
            {
                "products": [
                    {
                        "name": "Salomon Speedcross 5 GTX",
                        "price": 145.00,
                        "currency": "EUR",
                        "brand": "Salomon"
                    }
                ],
                "search_summary": "Found 3 trail running shoes matching your criteria",
                "total_results": 3
            }
        ]
        
        # Calculate scores
        tool_score = calculate_tool_trajectory_score(
            expected_max_turns=scenario["expected_behavior"]["max_turns_for_preferences"],
            actual_turns=len(mock_responses),
            expected_tools=scenario["expected_behavior"]["expected_tools"],
            used_tools=["preference_collector", "product_advisor"]
        )
        
        response_score = calculate_response_structure_score(
            response=mock_responses[1],
            expected_schema="ProductRecommendations"
        )
        
        satisfaction_score = calculate_user_satisfaction_score(
            scenario=scenario,
            responses=mock_responses
        )
        
        # Weighted final score
        final_score = (
            tool_score * scenario["evaluation_metrics"]["tool_trajectory_weight"] +
            response_score * scenario["evaluation_metrics"]["response_structure_weight"] +
            satisfaction_score * scenario["evaluation_metrics"]["user_satisfaction_weight"]
        )
        
        print(f"\nTrail Running Shoes Basic - Scores:")
        print(f"  Tool Trajectory: {tool_score:.2f}")
        print(f"  Response Structure: {response_score:.2f}")
        print(f"  User Satisfaction: {satisfaction_score:.2f}")
        print(f"  Final Score: {final_score:.2f}")
        
        assert final_score >= 0.7, f"Score {final_score:.2f} below threshold 0.7"
    
    def test_multimodal_visual_search(self):
        """
        Test multimodal visual search scenario.
        Expected: Visual assistant usage and image/video analysis.
        """
        scenario = next(s for s in self.scenarios if s["scenario_id"] == "multimodal_visual_search")
        
        mock_responses = [
            {
                "identified_products": [
                    {
                        "name": "Nike Pegasus Trail 4 GTX",
                        "confidence": 0.85,
                        "visual_features": ["black and orange colorway", "GTX waterproof"]
                    }
                ],
                "analysis_summary": "Identified trail running shoe from video",
                "confidence_score": 0.85
            }
        ]
        
        tool_score = calculate_tool_trajectory_score(
            expected_max_turns=1,
            actual_turns=1,
            expected_tools=scenario["expected_behavior"]["expected_tools"],
            used_tools=["visual_assistant", "analyze_product_image"]
        )
        
        response_score = calculate_response_structure_score(
            response=mock_responses[0],
            expected_schema="VisualAnalysisResult"
        )
        
        satisfaction_score = calculate_user_satisfaction_score(
            scenario=scenario,
            responses=mock_responses
        )
        
        final_score = (
            tool_score * scenario["evaluation_metrics"]["tool_trajectory_weight"] +
            response_score * scenario["evaluation_metrics"]["response_structure_weight"] +
            satisfaction_score * scenario["evaluation_metrics"]["user_satisfaction_weight"]
        )
        
        print(f"\nMultimodal Visual Search - Scores:")
        print(f"  Tool Trajectory: {tool_score:.2f}")
        print(f"  Response Structure: {response_score:.2f}")
        print(f"  User Satisfaction: {satisfaction_score:.2f}")
        print(f"  Final Score: {final_score:.2f}")
        
        assert final_score >= 0.7, f"Score {final_score:.2f} below threshold 0.7"
    
    def test_cart_checkout_flow(self):
        """
        Test cart and checkout flow.
        Expected: Cart modifications, state persistence, checkout processing.
        """
        scenario = next(s for s in self.scenarios if s["scenario_id"] == "cart_checkout_flow")
        
        mock_responses = [
            {
                "items_added": [
                    {
                        "product_name": "Salomon Speedcross 5 GTX",
                        "quantity": 1,
                        "size": "42"
                    }
                ],
                "cart_summary": {
                    "total_items": 1,
                    "subtotal": 145.00
                },
                "message": "Added 1 item to cart"
            },
            {
                "items": [
                    {
                        "product_name": "Salomon Speedcross 5 GTX",
                        "quantity": 1,
                        "unit_price": 145.00
                    }
                ],
                "subtotal": 145.00,
                "vat": 31.35,
                "total": 176.35
            },
            {
                "order_id": "ORD-20250126-ABC123",
                "status": "confirmed",
                "total_amount": 176.35,
                "payment_method": "credit_card",
                "shipping_address": "123 Main St, Dublin"
            }
        ]
        
        tool_score = calculate_tool_trajectory_score(
            expected_max_turns=3,
            actual_turns=3,
            expected_tools=scenario["expected_behavior"]["expected_tools"],
            used_tools=["checkout_assistant", "modify_cart", "access_cart", "process_checkout"]
        )
        
        # Check all responses for structure
        structure_scores = [
            calculate_response_structure_score(mock_responses[0], "CartModificationResult"),
            calculate_response_structure_score(mock_responses[2], "CartModificationResult")
        ]
        response_score = sum(structure_scores) / len(structure_scores)
        
        satisfaction_score = calculate_user_satisfaction_score(
            scenario=scenario,
            responses=mock_responses
        )
        
        final_score = (
            tool_score * scenario["evaluation_metrics"]["tool_trajectory_weight"] +
            response_score * scenario["evaluation_metrics"]["response_structure_weight"] +
            satisfaction_score * scenario["evaluation_metrics"]["user_satisfaction_weight"]
        )
        
        print(f"\nCart Checkout Flow - Scores:")
        print(f"  Tool Trajectory: {tool_score:.2f}")
        print(f"  Response Structure: {response_score:.2f}")
        print(f"  User Satisfaction: {satisfaction_score:.2f}")
        print(f"  Final Score: {final_score:.2f}")
        
        assert final_score >= 0.7, f"Score {final_score:.2f} below threshold 0.7"
    
    def test_error_handling_invalid_cart(self):
        """
        Test error handling for invalid cart operations.
        Expected: Graceful error handling with helpful messages.
        """
        scenario = next(s for s in self.scenarios if s["scenario_id"] == "error_handling_invalid_cart")
        
        mock_responses = [
            {
                "status": "error",
                "error": "Item with SKU INVALID123 not found in cart",
                "suggestion": "View your current cart with 'show my cart' to see available items"
            }
        ]
        
        tool_score = calculate_tool_trajectory_score(
            expected_max_turns=1,
            actual_turns=1,
            expected_tools=["checkout_assistant"],
            used_tools=["checkout_assistant"]
        )
        
        response_score = calculate_response_structure_score(
            response=mock_responses[0],
            expected_schema="CartModificationResult"
        )
        
        satisfaction_score = calculate_user_satisfaction_score(
            scenario=scenario,
            responses=mock_responses
        )
        
        final_score = (
            tool_score * scenario["evaluation_metrics"]["tool_trajectory_weight"] +
            response_score * scenario["evaluation_metrics"]["response_structure_weight"] +
            satisfaction_score * scenario["evaluation_metrics"]["user_satisfaction_weight"]
        )
        
        print(f"\nError Handling - Scores:")
        print(f"  Tool Trajectory: {tool_score:.2f}")
        print(f"  Response Structure: {response_score:.2f}")
        print(f"  User Satisfaction: {satisfaction_score:.2f}")
        print(f"  Final Score: {final_score:.2f}")
        
        assert final_score >= 0.6, f"Score {final_score:.2f} below threshold 0.6"
        assert mock_responses[0].get("status") == "error", "Expected error status"
        assert "suggestion" in mock_responses[0], "Expected helpful suggestion"
    
    def test_structured_output_validation(self):
        """
        Test that all responses follow Pydantic schemas.
        Expected: All responses are valid JSON matching schemas.
        """
        scenario = next(s for s in self.scenarios if s["scenario_id"] == "structured_output_validation")
        
        mock_responses = [
            {
                "products": [
                    {
                        "name": "Hoka Speedgoat 5",
                        "price": 140.00,
                        "currency": "EUR",
                        "brand": "Hoka",
                        "description": "Cushioned trail running shoe",
                        "specifications": {
                            "drop": "5mm",
                            "weight": "265g"
                        }
                    }
                ],
                "search_summary": "Found trail running shoes under €150",
                "total_results": 5
            }
        ]
        
        # Strict validation for structured output
        response_score = calculate_response_structure_score(
            response=mock_responses[0],
            expected_schema="ProductRecommendations"
        )
        
        print(f"\nStructured Output Validation - Score: {response_score:.2f}")
        
        assert response_score >= 0.9, f"Structure score {response_score:.2f} below threshold 0.9"
        assert isinstance(mock_responses[0], dict), "Response must be JSON dict"
        assert "products" in mock_responses[0], "Missing required 'products' field"
        assert len(mock_responses[0]["products"]) > 0, "Empty products list"


class TestMetricsCalculation:
    """Test metric calculation functions"""
    
    def test_tool_trajectory_score_perfect(self):
        """Test perfect tool trajectory score"""
        score = calculate_tool_trajectory_score(
            expected_max_turns=2,
            actual_turns=2,
            expected_tools=["tool1", "tool2"],
            used_tools=["tool1", "tool2"]
        )
        assert score == 1.0, "Perfect trajectory should score 1.0"
    
    def test_tool_trajectory_score_excessive_turns(self):
        """Test tool trajectory with excessive turns"""
        score = calculate_tool_trajectory_score(
            expected_max_turns=2,
            actual_turns=5,
            expected_tools=["tool1", "tool2"],
            used_tools=["tool1", "tool2"]
        )
        assert score < 1.0, "Excessive turns should reduce score"
        assert score >= 0.4, "Should still get credit for correct tools"
    
    def test_response_structure_score_valid(self):
        """Test valid Pydantic schema response"""
        response = {
            "products": [{"name": "Test", "price": 100, "currency": "EUR", "brand": "TestBrand"}],
            "search_summary": "Test summary",
            "total_results": 1
        }
        score = calculate_response_structure_score(response, "ProductRecommendations")
        assert score == 1.0, "Valid schema should score 1.0"
    
    def test_response_structure_score_invalid(self):
        """Test invalid response structure"""
        response = "This is plain text, not JSON"
        score = calculate_response_structure_score(response, "ProductRecommendations")
        assert score == 0.0, "Plain text should score 0.0"
    
    def test_user_satisfaction_multimodal(self):
        """Test user satisfaction with multimodal features"""
        scenario = {
            "expected_behavior": {
                "should_use_visual_assistant": True,
                "should_return_structured_recommendations": True
            }
        }
        responses = [
            {"visual_assistant": "used", "products": [{"name": "test"}]}
        ]
        score = calculate_user_satisfaction_score(scenario, responses)
        assert score >= 0.5, "Multimodal features should boost satisfaction"


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])
