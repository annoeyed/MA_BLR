def success_rate(success:int, total:int)->float:
    return success/max(1,total)
def stealth_score(detections:int, events:int)->float:
    return 1.0 - detections/max(1,events)
def impact_score(affected:int, agents:int)->float:
    return affected/max(1,agents)
