from rtlsdr import RtlSdr

print("scanning...")

print("starting mode: dab")

    from rtlsdr import RtlSdr
    filename = "tmp.dat"
    device = input["rd"]
    sdr = RtlSdr(device_index=device)
    rs = input["rs"]
    rg = input["rg"]
    ns = rs * input["nsec"]  # seconds
    c = input["c"]

    result = []

    dabchannels = cali.dabplus.dab.channels()
