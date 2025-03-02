def format_receiver_tow(pr_data=None):
    if pr_data is None:
        return
    else:
        receiver_tow = pr_data["DF004"]
        return receiver_tow/1000
