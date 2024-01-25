import requests
import math


class Analyser:
    def __init__(self, base_url):
        self.base_url = base_url

    def _get(self, endpoint, params=None):
        response = requests.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def _get_signal_ids(self, params=None):
        """
        Retrieve the list of IDs of signals in the database.
        E.g.: [0, 1, 2, 10, 255]
        """
        return self._get("signals", params=params)

    def _get_signal_info(self, id, params=None):
        """
        Retrieve information for the given signal ID (integer).
        E.g.:
        {
            "name": "sig1",
            "group": ["section", "subsection"],
        }
        """
        return self._get("signals/" + str(id), params=params)

    def _get_signal_values(self, id, params=None):
        """
        Retrieve a list of signal values between two timestamps
        start and end.
        E.g.:
        [
            {
                "timestamp": "2023-07-10T08:00:21.123Z",
                "value": 123.456
            },
            {
                "timestamp": "2023-07-10T08:12:01.532Z",
                "value": 789.0
            },
        ]
        """
        return self._get(f"signals/{id}/values", params=params)

    def _get_signal_id_from_name(self, name, params=None):
        """
        Retrieve the id of a signal given a name.
        """
        signal_ids = self._get_signal_ids(params=params)

        for signal_id in signal_ids:
            signal_info = self._get_signal_info(signal_id)
            if signal_info["name"] == name:
                return signal_id

    def _filter_signals_by_group(self, signals, group):
        """
        Filter signals based on the specified group and subgroups.
        """
        if group is not None:
            filtered_signals = []
            for signal in signals:
                signal_info = self._get_signal_info(signal)
                signal_groups = signal_info.get("group", [])
                if signal_groups is None:
                    continue
                if any(g == group for g in signal_groups):
                    filtered_signals.append(signal)
            return filtered_signals
        else:
            return signals

    def mean(self, start, end, group=None):
        """
        Returns the mean for each signal name
        """
        signal_ids = self._get_signal_ids()
        result = []

        filtered_signal_ids = self._filter_signals_by_group(signal_ids, group)

        for signal_id in filtered_signal_ids:
            signal_info = self._get_signal_info(signal_id)
            signal_values = self._get_signal_values(
                signal_id, params={"start": start, "end": end}
            )

            values = [entry["value"] for entry in signal_values]
            mean_value = sum(values) / len(values) if values else None

            result.append({"name": signal_info["name"], "mean": mean_value})
        return result

    def std(self, start, end, group=None):
        """
        Returns the standard deviation for each signal name
        """
        signal_ids = self._get_signal_ids()
        result = []

        filtered_signal_ids = self._filter_signals_by_group(signal_ids, group)

        for signal_id in filtered_signal_ids:
            signal_info = self._get_signal_info(signal_id)
            signal_values = self._get_signal_values(
                signal_id, params={"start": start, "end": end}
            )

            values = [entry["value"] for entry in signal_values]
            mean_value = sum(values) / len(values) if values else None

            if mean_value is not None:
                std_value = math.sqrt(
                    sum((x - mean_value) ** 2 for x in values) / len(values)
                )
            else:
                std_value = None

            result.append({"name": signal_info["name"], "std": std_value})

        return result

    def stats(self, start, end, group=None):
        """
        Returns both the mean and standard deviation for each signal name
        """
        signal_ids = self._get_signal_ids()
        result = []

        filtered_signal_ids = self._filter_signals_by_group(signal_ids, group)

        for signal_id in filtered_signal_ids:
            signal_info = self._get_signal_info(signal_id)
            signal_values = self._get_signal_values(
                signal_id, params={"start": start, "end": end}
            )

            values = [entry["value"] for entry in signal_values]
            mean_value = sum(values) / len(values) if values else None

            if mean_value is not None:
                std_value = math.sqrt(
                    sum((x - mean_value) ** 2 for x in values) / len(values)
                )
            else:
                std_value = None

            result.append(
                {"name": signal_info["name"], "mean": mean_value, "std": std_value}
            )

        return result

    def raw(self, start, end, name, batch_size=1000, params=None):
        """
        Returns the timestamps and values of the signal in batches specified by batch_size
        The user should iterate through the batches, e.g.:
            for batch in raw(...):
                # Do something to batch
        Return an iterator that returns one batch of data at a time.
        """
        id = self._get_signal_id_from_name(name)
        offset = 0

        while True:
            signal_values = self._get_signal_values(
                id,
                params={
                    "start": start,
                    "end": end,
                    "page_size": batch_size,
                    "offset": offset,
                },
            )

            if not signal_values:
                break

            yield signal_values
            offset += batch_size
