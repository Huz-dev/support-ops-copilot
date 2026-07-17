from pathlib import Path
from datetime import datetime
import json


class LoggerService:

    def __init__(self):

        self.path = Path("logs/sessions")

        self.path.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(
        self,
        ticket,
        plan,
        classification,
        extraction,
        tool_results,
        email,
    ):

        timestamp = datetime.now()

        session_id = timestamp.strftime(
            "%Y%m%d_%H%M%S"
        )

        data = {
            "session_id": session_id,
            "timestamp": str(timestamp),
            "ticket": ticket,
            "plan": plan,
            "classification": classification,
            "extraction": extraction,
            "tool_results": tool_results,
            "email": email,
        }

        with open(
            self.path / f"{session_id}.json",
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )