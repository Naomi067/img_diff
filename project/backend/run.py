# -*- coding: utf-8 -*-
import settings
from qaweb import create_app, config

if __name__ in ("__main__", "run"):
    app = create_app()
    if app.is_main_worker:
        ## do something you need
        pass
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=config.PORT, debug=True, use_debugger=True)
