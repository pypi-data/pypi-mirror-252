from pathlib import Path

from k8s_collector import config
from k8s_collector.config.models import CollectorConfig, AggregatedResource
from k8s_collector.config.parsers import YamlCollectorConfigParser
from k8s_collector.config.parsers.sinks.factory import SinkConfigParserFactory, BasicSinkConfigParserFactory
from k8s_collector.config.validators import CollectorConfigValidator, JsonSchemaCollectorConfigValidator
from k8s_collector.filterers import JmesPathEventFilterer, EventFilterer
from k8s_collector.handlers import BasicEventHandler, EventHandler
from k8s_collector.listeners import ThreadedMultiResourceListener, BasicResourceListener, MultiResourceListener, \
    ResourceListener
from k8s_collector.processors import JmesPathEventProcessor, EventProcessor
from k8s_collector.sinks.factory import SharedSinkFactory, SinkFactory
from k8s_collector.utils.resources import get_aggregated_resources


class K8SCollector:
    def __init__(self, collector_config: Path, namespace: str | None):
        self._namespace: str | None = namespace
        collector_config_schema: Path = Path(config.__file__).parent / 'collector_config.schema.json'
        self._collector_config_validator: CollectorConfigValidator = JsonSchemaCollectorConfigValidator(collector_config_schema)
        self._sink_config_parser_factory: SinkConfigParserFactory = BasicSinkConfigParserFactory()
        self._collector_config_parser = YamlCollectorConfigParser(self._collector_config_validator, self._sink_config_parser_factory)
        self._collector_config: CollectorConfig = self._collector_config_parser.parse_file(collector_config)
        self._aggregated_resources: list[AggregatedResource] = get_aggregated_resources(self._collector_config)

        self._sink_factory: SinkFactory = SharedSinkFactory()
        self._event_filterer: EventFilterer = JmesPathEventFilterer()
        self._event_processor: EventProcessor = JmesPathEventProcessor()
        self._event_handler: EventHandler = BasicEventHandler(self._event_filterer, self._event_processor, self._sink_factory)
        self._event_listener: ResourceListener = BasicResourceListener(self._event_handler)
        self._multi_resource_event_listener: MultiResourceListener = ThreadedMultiResourceListener(self._event_listener)

    def collect(self):
        self._multi_resource_event_listener.listen(self._aggregated_resources, self._namespace)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--namespace", type=str,
                        help="namespace to listen for resources, if not provided listen cluster-wide")
    parser.add_argument("-c", "--config", type=Path, required=True,
                        help="CollectorConfig Configuration file path")
    args = parser.parse_args()

    collector = K8SCollector(collector_config=args.config, namespace=args.namespace)
    collector.collect()
