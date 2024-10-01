from pypresence import Presence
import env
import time
import threading
import signal

start_time = int(time.time())
RPC = Presence(env.discord.client_id)
RPC.connect()

def update_t(**kwargs):
  def do_run():
    RPC.update(**kwargs)
  thread = threading.Thread(target=do_run)
  thread.start()