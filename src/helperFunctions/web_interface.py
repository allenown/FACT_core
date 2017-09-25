import colorsys
import json
from itertools import chain


def _get_rgba(hue, saturation):
    return "rgba({}, {}, {}, {})".format(*[int(i * 255) for i in colorsys.hsv_to_rgb(hue, 0.8, 0.75)], saturation)


def get_js_list_of_n_uniques_colors(n, saturation=0.7, shuffle=True):
    result = [_get_rgba(i / n, saturation) for i in range(1, n + 1)]
    if shuffle:
        result = list(chain(*[result[i::2] for i in range(2)]))
    return result


def get_color_list(n, limit=10):
    compliant_colors = ['#2b669a', '#cce0dc', '#2b669a', '#cce0dc', '#2b669a', '#cce0dc', '#2b669a', '#cce0dc', '#2b669a', '#cce0dc', '#2b669a', '#cce0dc']
    if n > limit:
        n = limit
    return compliant_colors[:n]


def overwrite_default_plugins(intercom, checked_plugin_list):
    result = intercom.get_available_analysis_plugins()
    for item in result.keys():
        tmp = list(result[item])
        if item in checked_plugin_list:
            tmp[2] = True
        else:
            tmp[2] = False
        result[item] = tuple(tmp)
    return result


def apply_filters_to_query(request, query):
    query_dict = json.loads(query)
    for key in ["device_class", "vendor"]:
        if request.args.get(key):
            if key not in query_dict.keys():
                query_dict[key] = request.args.get(key)
            else:  # key was in the previous search query
                query_dict["$and"] = [{key: query_dict[key]}, {key: request.args.get(key)}]
                query_dict.pop(key)
    return query_dict


class ConnectTo:
    def __init__(self, connected_interface, config):
        self.interface = connected_interface
        self.config = config

    def __enter__(self):
        self.connection = self.interface(self.config)
        return self.connection

    def __exit__(self, *args):
        self.connection.shutdown()