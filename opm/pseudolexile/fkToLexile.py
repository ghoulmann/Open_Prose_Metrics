def getLexile(fk):
    if fk >= 12.12:
        return "1185-1385"
    elif (fk > 10.35):
        return "1050-1335"
    elif (fk > 7.74):
        return "925-1185"
    elif (fk > 4.51):
        return "740-1010"
    elif (fk >= 1.98):
        return "420-820"
    elif (fk > 14.20):
        return "Past CCR (820+)"
    else:
        return "below 419"
