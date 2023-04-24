import p2p
reciever = p2p.p2p_obj('localhost',19123)
online_df = reciever.get_online_df()