"""
Small JSON logger using keyworded varargs

@param msg logger status message
@param **kwargs keyworded logger values
"""
def log(msg, **kwargs):
  log_obj = {}
  for key in kwargs:
    log_obj[key] = kwargs[key]
  log_obj['msg'] = msg
  print(f"{log_obj}")
