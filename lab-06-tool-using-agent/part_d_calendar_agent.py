"""Part D: agent with Google Calendar tools (create event, today's schedule), plus date/time and calculator."""
import datetime
from tools import calculator, get_date_time
from google_calendar_tools import create_calendar_event, get_todays_schedule
from agent_core import build_agent, run_agent, SYSTEM


def main():
    llm_with_tools, by_name = build_agent([get_date_time, get_todays_schedule, create_calendar_event, calculator])
    print("Calendar agent. Try: What is on my calendar today?   or   Add a meeting tomorrow at 3 pm")
    while True:
        q = input("\nYou (or exit): ").strip()
        if q.lower() in ("exit", "quit", ""):
            break
        today = datetime.date.today()
        system = (SYSTEM + f" Today's date is {today.isoformat()} ({today.strftime('%A')}). "
                  "Use it to work out dates such as 'tomorrow'. For calendar questions use the calendar tools.")
        print("Agent:", run_agent(llm_with_tools, by_name, q, system=system))


if __name__ == "__main__":
    main()
