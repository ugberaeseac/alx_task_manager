import datetime

def parse_task_text(text: str) -> dict:
    """
    Abstracted adapter to parse task text into structured fields.
    This function will be replaced by an LLM call in the future.

    Args:
        text (str): The raw text input from the user.

    Returns:
        dict: A dictionary containing parsed task fields like 'title', 'description',
              'due_date' (ISO format string), and 'priority'.
              Returns an empty dictionary or default values if parsing fails or fields are not found.
    """
    # This is a stub implementation. In a real scenario, this would involve an LLM.
    # For now, we'll implement a very basic parsing logic or return dummy data.

    title = text
    description = ""
    due_date = None  # ISO format string, e.g., "2023-12-31T23:59:59"
    priority = "medium"

    # Basic keyword-based parsing for demonstration
    if "tomorrow" in text.lower():
        due_date = (datetime.date.today() + datetime.timedelta(days=1)).isoformat() + "T17:00:00"
        title = title.replace("tomorrow", "").strip()
    if "high priority" in text.lower():
        priority = "high"
        title = title.replace("high priority", "").strip()
    elif "low priority" in text.lower():
        priority = "low"
        title = title.replace("low priority", "").strip()

    return {
        "title": title.strip() if title.strip() else "New Task",
        "description": description,
        "due_date": due_date,
        "priority": priority,
    }