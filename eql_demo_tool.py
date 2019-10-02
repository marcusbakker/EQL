import datetime
import json
import sys
from pprint import pprint
import eql
import yaml


class EQLSearch:
    def _create_events(self, data, data_type, event_type, timestamp_key):
        """
        Create EQL Events from the provided data.
        :param data: list of dictionaries to be transformed to EQL Events
        :param data_type: if 'yaml', serialize all 'Datetime.date' key-value pairs
        :param event_type: the value to be used as event_type for the provided data
        :param timestamp_key: name of the key-value pair to be used as timestamp
        :return: EQL Events or data
        """
        eql_events = []

        if data_type == 'yaml':
            data = self._serialize_date(data)

        # this result in EQL trying the derive the event_type and timestamp from the contents of 'data'
        if not event_type:
            return data

        # create EQL Events from 'data'
        for item in data:
            eql_events.append(eql.Event(event_type, timestamp_key, item))

        return eql_events

    def _execute_eql_query(self, events, query):
        """
        Execute an EQL query on the provided events.
        :param events: events
        :param query: EQL query
        :return: the result of the query as a list of dictionaries or None when the query did not match the schema
        """
        schema = eql.Schema.learn(events)

        query_result = []

        # this function is used to store the result of the query to 'query_result'
        def store_result(result):
            for event in result.events:
                query_result.append(event.data)

        engine = eql.PythonEngine()
        with schema:
            try:
                eql_query = eql.parse_query(query, implied_any=True, implied_base=True)
                engine.add_query(eql_query)
            except eql.EqlError as e:
                print(e, file=sys.stderr)
                print('\nTake into account the following schema:')
                pprint(schema.schema)
                return None
            engine.add_output_hook(store_result)

        # execute the query
        engine.stream_events(events)

        return query_result

    def search(self, data, query, data_type='json', event_type=None, timestamp_key=0):
        """
        Perform a EQL search on the provided JSON or YAML data.
        :param data: list of dictionaries
        :param query: EQL search query
        :param data_type: 'json' or 'yaml'
        :param event_type: name of the event type to use for the EQL schema. Leave empty if you want to derive the
        event type from the data itself (i.e. the key-value pair named 'event_type' or 'event_type_full').
        :param timestamp_key: name of the key-value pair to be used as timestamp
        :return: the result of the search query as a list of dictionaries
        """
        # check for a valid data_type
        if data_type != 'json' and data_type != 'yaml':
            raise ValueError("date_type should be 'json' or 'yaml'")

        # transform data into a list of EQL Event objects
        eql_events = self._create_events(data, data_type, event_type, timestamp_key)

        # execute the EQL query on the provided data
        search_result = self._execute_eql_query(eql_events, query)

        return search_result

    def _traverse_dict(self, obj, callback=None):
        """
        Traverse all items in a dictionary
        :param obj: dictionary, list or value
        :param callback: the function that will be called to modify a value
        :return: value or call callback function
        """
        if isinstance(obj, dict):
            value = {k: self._traverse_dict(v, callback)
                     for k, v in obj.items()}
        elif isinstance(obj, list):
            value = [self._traverse_dict(elem, callback)
                     for elem in obj]
        else:
            value = obj

        # if a callback is provided, call it to get the new value
        if callback is None:
            return value
        else:
            return callback(value)

    def _serialize_date(self, obj):
        """
        Serialize a datetime.date object
        :param obj: dictionary
        :return: function call
        """

        # this gets called for every value in the dictionary
        def _transformer(value):
            if isinstance(value, datetime.date):
                return str(value)
            else:
                return value

        return self._traverse_dict(obj, callback=_transformer)


if __name__ == "__main__":
    eql_search = EQLSearch()

    # example.json = https://github.com/marcusbakker/EQL/blob/master/example.json
    with open('example.json', 'r') as json_data:
        data = json.load(json_data)

    query = 'process where pid == 424'
    result = eql_search.search(data, query)
    if result:
        print('Query:  ' + query + '\nResult: ' + str(len(result)) + ' event(s) ↓\n')
        pprint(result)

    print('\n' + '-' * 80 + '\n')

    # data-sources-endpoints.yaml = https://github.com/marcusbakker/EQL/blob/master/data-sources-endpoints.yaml
    with open('data-sources-endpoints.yaml', 'r') as yaml_data:
        data = yaml.safe_load(yaml_data)['data_sources']

    query = 'data_sources where date_connected >= "2019-01-01"'
    result = eql_search.search(data, query, data_type='yaml', event_type='data_sources', timestamp_key=0)
    if result:
        print('Query:  ' + query + '\nResult: ' + str(len(result)) + ' event(s) ↓\n')
        pprint(result)
