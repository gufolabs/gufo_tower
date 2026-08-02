from collections import OrderedDict

import yaml
import yaml.constructor


class OrderedDictYAMLLoader(yaml.Loader):
    """A YAML loader that loads mappings into ordered dictionaries."""

    def __init__(self, *args, **kwargs):
        yaml.Loader.__init__(self, *args, **kwargs)

        self.add_constructor(
            "tag:yaml.org,2002:map", type(self).construct_yaml_map
        )
        self.add_constructor(
            "tag:yaml.org,2002:omap", type(self).construct_yaml_map
        )

    def construct_yaml_map(self, node):
        data = OrderedDict()
        yield data
        value = self.construct_mapping(node)
        data.update(value)

    def construct_mapping(self, node, deep=False):
        if isinstance(node, yaml.MappingNode):
            self.flatten_mapping(node)
        else:
            raise yaml.constructor.ConstructorError(
                None,
                None,
                f"expected a mapping node, but found {node.id}",
                node.start_mark,
            )

        mapping = OrderedDict()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            try:
                hash(key)
            except TypeError as exc:
                msg = "while constructing a mapping"
                raise yaml.constructor.ConstructorError(
                    msg,
                    node.start_mark,
                    f"found unacceptable key ({exc})",
                    key_node.start_mark,
                ) from exc
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping


def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """For Python 3.7+ only"""

    class OrderedLoader(Loader):
        pass

    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping
    )
    return yaml.load(stream, OrderedLoader)
