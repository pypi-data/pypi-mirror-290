from typing import Dict, Any
from chat_llm_cli.prompt.prompt import console
from litellm import BudgetManager
from rich.panel import Panel
from rich.table import Table


class SessionBudgetManager:
    def __init__(self, budget_manager: BudgetManager):
        self.budget_manager = budget_manager
        self.session_costs = {}

    def add_cost(self, user: str, model: str, cost: float):
        if user not in self.session_costs:
            self.session_costs[user] = {}
        if model not in self.session_costs[user]:
            self.session_costs[user][model] = 0
        self.session_costs[user][model] += cost

    def get_session_cost(self, user: str) -> float:
        return sum(self.session_costs.get(user, {}).values())

    def get_session_model_costs(self, user: str) -> Dict[str, float]:
        return self.session_costs.get(user, {})


def display_expense(
    config: Dict[str, Any],
    user: str,
    budget_manager: BudgetManager,
    session_budget_manager: SessionBudgetManager,
) -> None:
    """
    Displays the current cost, total budget, and remaining budget for the user.

    Args:
        config: The configuration dictionary.
        user: The user's name.
        budget_manager: The budget manager.
        session_budget_manager: The session budget manager.
    """
    # Get the current cost and total budget for the user
    current_cost = budget_manager.get_current_cost(user)
    session_cost = session_budget_manager.get_session_cost(user)
    total_cost = current_cost + session_cost
    total_budget = budget_manager.get_total_budget(user)

    # Calculate remaining budget
    remaining_budget = total_budget - total_cost

    # Create a table for expense information
    table = Table(
        show_header=False, expand=True, border_style="#89dceb"
    )  # Catppuccin Sky
    table.add_column("Item", style="bold #f5e0dc")  # Catppuccin Rosewater
    table.add_column("Value", style="#cba6f7")  # Catppuccin Mauve

    table.add_row("Previous total cost", f"${current_cost:.6f}")
    table.add_row("Current session cost", f"${session_cost:.6f}")
    table.add_row("New total cost", f"${total_cost:.6f}")
    table.add_row("Total budget", f"${total_budget:.2f}")
    table.add_row("Remaining budget", f"${remaining_budget:.6f}")

    # If you want to display model-specific costs
    model_costs = budget_manager.get_model_cost(user)
    session_model_costs = session_budget_manager.get_session_model_costs(user)
    if model_costs or session_model_costs:
        table.add_row("Cost breakdown by model", "")
        for model in set(list(model_costs.keys()) + list(session_model_costs.keys())):
            previous_cost = model_costs.get(model, 0)
            session_cost = session_model_costs.get(model, 0)
            total_cost = previous_cost + session_cost
            table.add_row(
                f"  {model}",
                f"${total_cost:.6f} (${previous_cost:.6f} + ${session_cost:.6f})",
            )

    # Create a panel to contain the table
    panel = Panel(
        table,
        title="Expense Information",
        expand=False,
        border_style="#89dceb",  # Catppuccin Sky
        title_align="left",
    )

    console.print(panel)


def calculate_expense(
    prompt_tokens: int,
    completion_tokens: int,
    prompt_pricing: float,
    completion_pricing: float,
) -> float:
    """
    Calculates the expense based on the number of tokens and pricing rates.

    Args:
        prompt_tokens: The number of tokens in the prompt.
        completion_tokens: The number of tokens in the completion.
        prompt_pricing: The pricing rate per 1000 tokens for the prompt.
        completion_pricing: The pricing rate per 1000 tokens for the completion.

    Returns:
        The calculated expense.
    """
    expense = ((prompt_tokens / 1000) * prompt_pricing) + (
        (completion_tokens / 1000) * completion_pricing
    )

    # Format to display in decimal notation rounded to 6 decimals
    expense = round(expense, 6)

    return expense
