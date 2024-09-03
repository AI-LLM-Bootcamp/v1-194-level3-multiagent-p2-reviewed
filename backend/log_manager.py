from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from threading import Lock

@dataclass
class Event:
    timestamp: datetime
    data: str


@dataclass
class Output:
    status: str
    events: List[Event]
    result: str

outputs_lock = Lock()
outputs: Dict[str, "Output"] = {}

def append_event(input_id: str, event_data: str):
    with outputs_lock:
        if input_id not in outputs:
            print(f"Start output {input_id}")
            outputs[input_id] = Output(
                status='STARTED',
                events=[],
                result='')
        else:
            print("Appending event for output")
            
        outputs[input_id].events.append(
            Event(timestamp=datetime.now(), data=event_data))