import time
from is_wire.core import Logger

from opencensus.trace.tracer import Tracer
from opencensus.trace.span_context import SpanContext
from opencensus.trace.exporters.zipkin_exporter import ZipkinExporter

import opencensus.trace.exporters.transports.background_thread
from opencensus.trace.exporters.transports.background_thread import BackgroundThreadTransport

log = Logger(name='ZipkinExporter')

exporter1 = ZipkinExporter(
  service_name='Service1',
  host_name='localhost',
  port=9412,
  transport=BackgroundThreadTransport(max_batch_size=100)
)

exporter2 = ZipkinExporter(
    service_name='Service2',
    host_name='localhost',
    port=9412,
    transport=BackgroundThreadTransport(max_batch_size=100)
)

exporter3 = ZipkinExporter(
    service_name='Service3',
    host_name='localhost',
    port=9412,
    transport=BackgroundThreadTransport(max_batch_size=100)
)


for i in range(10):
  tracer1 = Tracer(exporter=exporter1)
  name = 'task_{}'.format(i)
  with tracer1.span(name=name) as span1:
    time.sleep(0.1)
    context = SpanContext(trace_id=tracer1.tracer.trace_id,
                          span_id=span1.context_tracer.trace_id)
    tracer2 = Tracer(exporter=exporter2, span_context=context)
    for j in range(2):
      inner_name = 'task_{}_{}'.format(i, j)
      with tracer2.span(name=inner_name) as span2:
        span2.add_attribute('Value', j)
        span2.add_attribute('SquareValue', j*j)
        time.sleep(j*0.025)
      inner_name = 'other_task_{}_{}'.format(i, j)
      with tracer2.span(name=inner_name) as span2:
        span2.add_attribute('MinusValue', -j)
        span2.add_attribute('DoubleValue', 2*j)
        time.sleep(j*j*0.01)
    
        tracer3 = Tracer(exporter=exporter3, span_context=context)
        inner_name = 'task_{}_{}'.format(i, j)
        with tracer3.span(name=inner_name) as span3:
            time.sleep(j*j*0.05)
    
    time.sleep(0.1)
    log.info('{}', name)
