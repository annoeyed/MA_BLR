"""
Integration test for the basic backdoor loop scenario.
"""
import pytest
from experiments.scenarios.basic_backdoor_loop import main as run_scenario

@pytest.mark.asyncio
async def test_backdoor_loop_execution():
    """
    Tests that the basic backdoor loop scenario runs without errors
    and returns a results dictionary.
    """
    print("Running integration test for basic backdoor loop...")
    
    # Execute the scenario
    results = await run_scenario()
    
    # Check for a basic indicator of success.
    # The exact results will depend on the final implementation of the scenario.
    # For now, let's just check that it returns a dictionary.
    assert isinstance(results, dict), "Scenario should return a dictionary of results."
    
    # A more specific test could be:
    # assert "total_alerts" in results, "Results should contain total_alerts count."
    # assert results["total_alerts"] > 0, "There should be at least one alert in this scenario."
    
    print("Integration test completed successfully.")
