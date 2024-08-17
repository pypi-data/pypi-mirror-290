from hgraph import graph, TS_SCHEMA, TSB, record, TIME_SERIES_TYPE, SCALAR, TSD

__all__ = ("record_to_dataframe_tsb", "record_to_dataframe_tsd")


@graph(overloads=record)
def record_to_dataframe_tsb(ts: TSB[TS_SCHEMA]):
    """
    If the tsb is flat, then we record into a single data-frame, if not, we split the time-series into it's elements
    and then attempt to record the components into individual files. The file-name will take the form of
    {recordable_id}:{key}
    """


@graph(overloads=record)
def record_to_dataframe_tsd(ts: TSD[SCALAR, TIME_SERIES_TYPE]):
    """
    Records the components into a data-frame of key - > flattening of the time-series-type
    """
