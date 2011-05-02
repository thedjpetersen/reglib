def time_conflict(time, time1):
    if (time[0] >= time1[0] and time[0] <= time1[1]) or (time[1] >= time1[0] and time[1] <= time1[1]):
        return True
    return False
