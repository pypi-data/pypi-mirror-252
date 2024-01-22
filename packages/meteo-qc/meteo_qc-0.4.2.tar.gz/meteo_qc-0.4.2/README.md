[![ci](https://github.com/jkittner/meteo-qc/actions/workflows/ci.yaml/badge.svg)](https://github.com/jkittner/meteo-qc/actions/workflows/ci.yaml)
[![docs](https://github.com/jkittner/meteo-qc/actions/workflows/docs.yaml/badge.svg)](https://github.com/jkittner/meteo-qc/actions/workflows/docs.yaml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jkittner/meteo-qc/main.svg)](https://results.pre-commit.ci/latest/github/jkittner/meteo-qc/main)

# meteo-qc

`meteo_qc` is a customizable framework for applying quality checks to meteorological
data. The framework can be easily extended by registering custom functions/plugins.

## Installation

To install **meteo-qc**, open an interactive shell and run

```console
pip install meteo-qc
```

## Getting started

Check out the [Documentation](https://jkittner.github.io/meteo-qc) for
detailed information.

Apply the quality control to this csv data called `test_data.csv`:

```
date,temp,pressure_reduced
2022-01-01 10:00:00,1,600
2022-01-01 10:10:00,2,1024
2022-01-01 10:20:00,3,1024
2022-01-01 10:30:00,4,1090
2022-01-01 10:50:00,4,
2022-01-01 11:00:00,,1024
2022-01-01 11:10:00,2,1024
2022-01-01 11:20:00,3,1024
2022-01-01 11:30:00,4,1090
2022-01-01 11:40:00,4,1090
```

1. Read in the data as a `pd.DataFrame`.
1. Create a [`meteo_qc.ColumnMapping`](https://jkittner.github.io/meteo-qc/meteo_qc.html#meteo_qc.ColumnMapping)
   object and use the column names as keys to use the method `add_group` to add
   the column to the group
   ([`temperature`](https://jkittner.github.io/meteo-qc/groups.html#temperature)
   or [`pressure`](https://jkittner.github.io/meteo-qc/groups.html#pressure)).
   This can be an existing group or a new group.
1. Call [`meteo_qc.apply_qc`](https://jkittner.github.io/meteo-qc/meteo_qc.html#meteo_qc.apply_qc)
   to apply the control to the DataFrame `data` using the `column_mapping` as a
   definition for the checks to be applied.

```python
import pandas as pd
import meteo_qc

# read in the data
data = pd.read_csv('test_data.csv', index_col=0, parse_dates=True)

# map the columns to groups
column_mapping = meteo_qc.ColumnMapping()
column_mapping['temp'].add_group('temperature')
column_mapping['pressure_reduced'].add_group('pressure')

# apply the quality control
result = meteo_qc.apply_qc(df=data, column_mapping=column_mapping)
print(result)
```

This will result in this object which can be used to display the result in a
nice way e.g. using an `html` template to render it.

```python
{
    'columns': defaultdict(<function apply_qc.<locals>.<lambda> at 0x7f9b0edd5480>, {
        'temp': {
            'results': {
                'missing_timestamps': Result(
                    function='missing_timestamps',
                    passed=False,
                    msg='missing 1 timestamps (assumed frequency: 10min)',
                    data=None,
                ),
                'null_values': Result(
                    function='null_values',
                    passed=False,
                    msg='found 1 values that are null',
                    data=[[1641034800000, None, True]],
                ),
                'range_check': Result(
                    function='range_check',
                    passed=True,
                    msg=None,
                    data=None,
                ),
                'spike_dip_check': Result(
                    function='spike_dip_check',
                    passed=True,
                    msg=None,
                    data=None,
                ),
                'persistence_check': Result(
                    function='persistence_check',
                    passed=True,
                    msg=None,
                    data=None,
                )
            },
            'passed': False,
        },
        'pressure_reduced': {
            'results': {
                'missing_timestamps': Result(
                    function='missing_timestamps',
                    passed=False,
                    msg='missing 1 timestamps (assumed frequency: 10min)',
                    data=None,
                ),
                'null_values': Result(
                    function='null_values',
                    passed=False,
                    msg='found 1 values that are null',
                    data=[[1641034200000, None, True]],
                ),
                'range_check': Result(
                    function='range_check',
                    passed=False,
                    msg='out of allowed range of [860 - 1055]',
                    data=[[1641031200000, 600.0, True], [1641033000000, 1090.0, True], [1641036600000, 1090.0, True], [1641037200000, 1090.0, True]],
                ),
                'spike_dip_check': Result(
                    function='spike_dip_check',
                    passed=False,
                    msg='spikes or dips detected. Exceeded allowed delta of 0.3 / min',
                    data=[[1641031800000, 1024.0, True], [1641033000000, 1090.0, True], [1641034200000, None, True], [1641036600000, 1090.0, True]],
                ),
                'persistence_check': Result(
                    function='persistence_check',
                    passed=True,
                    msg=None,
                    data=None,
                )
            },
            'passed': False
        }
    }),
    'passed': False,
    'data_start_date': 1641031200000,
    'data_end_date': 1641037200000,
}
```

It is also possible to write and register your own functions if they are not
already in the predefined [Groups](https://jkittner.github.io/meteo-qc/groups.html).
Please check out the [Docs](https://jkittner.github.io/meteo-qc) for
more information.
