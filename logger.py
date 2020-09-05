class Logger:
  """
  @param msg logger status message
  @param **kwargs keyworded logger values
  """
  @staticmethod
  def info(msg, **kwargs):
    log_obj = Logger._log(msg, kwargs)
    print(f"[INFO] {log_obj}")

  """
  @param msg logger status message
  @param **kwargs keyworded logger values
  """
  @staticmethod
  def error(msg, **kwargs):
    log_obj = Logger._log(msg, kwargs)
    print(f"[ERROR] {log_obj}")

  def warn(msg, **kwargs):
    log_obj = Logger._log(msg, kwargs)
    print(f"[WARN] {log_obj}")

  @staticmethod
  def _log(msg, kwargs):
    log_obj = {}
    for key in kwargs:
      log_obj[key] = kwargs[key]
    log_obj['msg'] = msg
    return log_obj