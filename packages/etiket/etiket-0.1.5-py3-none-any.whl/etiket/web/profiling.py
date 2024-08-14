from fastapi import FastAPI
# Profiling
from pyinstrument import Profiler
from etiket.settings import settings

from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
import os
import sqltap


def register_profiling(app: FastAPI):
    profiling_interval=1e-3


    @app.middleware("http")
    async def profile_request(request: Request, call_next):
        profiler = Profiler(interval=profiling_interval, async_mode="enabled")
        profiler_sqltap = sqltap.start()
        profiler.start()
        response = await call_next(request)
        profiler.stop()
        profiler_sqltap.stop()
        statistics = profiler_sqltap.collect()
        sqltap.report(statistics, "sqltap_profile_report.html")
        # Save HTML to file
        with open("profiler_output.html", "w") as f:
            f.write(profiler.output_html())
        
        # Here, you could add logic to open this HTML file in a web browser, or you could manually navigate to it
        # os.system("open profiler_output.html") #macOS
        os.system('start profiler_output.html') #Windows
        print('profiled request saved.')
        # return HTMLResponse(profiler.output_html())
        return response

