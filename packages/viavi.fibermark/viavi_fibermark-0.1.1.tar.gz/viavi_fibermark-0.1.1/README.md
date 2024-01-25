# Curve Measure Notation CLI
This is a command-line interface (CLI) for the Curve Measure Notation tool. It provides various commands to perform operations related to curves, algorithms, and notes.
Commands are grouped in the following pattern :

```
Usage: cli.py [OPTIONS] COMMAND [ARGS]...

  Curve Measure Notation CLI

Options:
  --help  Show this message and exit.

Commands:
  add      Add command group.
  compare  Compare command group.
  note     Note command group.
  remote   Make command group.
  show     Show command group.
```

# Run from Dockerfile (Easiest way):

To run the FiberMark CI/CD App in a Docker container, follow these steps:

1. **Clone the Repository:**
   Clone this repository to your local machine:
   
   ```bash
   git clone https://github.com/your-username/fibermark_ci_cd.git
   ```
2. **Install Docker**

  Go here: https://www.docker.com/ 
  And follow the steps corresponding to your OS.

  For debian 12, one can follow: https://computingforgeeks.com/how-to-install-docker-on-debian-12-bookworm/?expand_article=1

3. **Build the Docker Image:**
   Open a terminal in the cloned repository directory and execute the following command to build the Docker image:
   
   ```bash
   docker build -t fibermark_ci_cd .
   ```

   This will create a Docker image named "fibermark_ci_cd".

4. **Run the Docker Container:**
   After building the Docker image, you can run a container from it using the following command:
   
   ```bash
   docker run -it -v path/to/your/fibermark:/code fibermark_ci_cd
   ```
   (-v flag mounts directory from local system where fibermark is to where fibermark is on Dockerfile, to facilitate you getting the generated excel report).
   This will start a container and provide you with an interactive terminal session in the working environment.

# Main tooling:

## Evaluating an FO version:

An FO evaluation can be done to monitor updates in FO on reference curves. This can be done on a local FO or a remote base FO.

(It is advised to do it on a local FO as it will be way faster due to all file transfers)

Examples:

`fibermark remote eval-fo --ip=localhost --user=aboussejra --passwd="users123"`

`fibermark remote eval-fo --ip="base-1000-77981" --user=root --passwd=1m0t0s0`

### Filter Configuration JSON

The `--use_filters` option may be used for `eval-fo`. It expects a JSON file that defines the filter configurations. The JSON file should have the following structure:

json

{
  "pulse_ns": [],
  "eval_category": ["Non-Regression"],
  "files_to_skip": [], # list of files to skip
  "eval_only_file": [] # if not empty, eval only on those files
}

It will filter files for faster evaluation.

## Make detailed reports:

A primary tool is to generate detailed reports of what changed between two FO version. Thus we have the compare algos with the `--detailed` flag. (all algo marks and evaluations are done only on `Non-Regression` category reference curves)

Example Command:

`fibermark compare algos --alg-1=22.64 --alg-2=23.22 --detailed`

This outputs a excel report which is a file of the form:

`FO: 23.22 comparison to FO: 22.64.xlsx`

Which contains 3 sheets. A summary of stats between algorithms. A sheet of events in FO 22.64 and not in FO 23.22, and a sheet of events in FO 23.22 and not in FO 22.64.

If needed, one can compare an algo to references in details:

`fibermark compare algo-to-ref --alg=22.64`

This ouputs an excel which is `FO: 22.64 comparison to reference.xlsx` which contains, a summary of algorithm stats and a sheet containing the detailed info on events measured (TP,FP,FN)


## Additional Information

- The `Dockerfile` in this repository defines the build process for the Docker image.
- You can customize the app or modify the `Dockerfile` to suit your needs.
- Remember to replace "your-username" with your actual GitHub username in the repository URL.

Feel free to explore, modify, and use this repository as a starting point for your CI/CD projects using Docker.

Happy coding!
```

Make sure to replace "your-username" with your actual GitHub username in the repository URL and adjust any other parts as needed to match your project's specifics.

# Installing package

Run `make install`to install package if you cloned the repo. Users reading this from bitbucket could do a simple 
`pip install git+https://cosgit1.ds.jdsu.net/scm/tfosw/fibermark.git` or a `poetry add git+https://cosgit1.ds.jdsu.net/scm/tfosw/fibermark.git` to install the project (or another command from their favorite python package manager).

# Old documentation detailed notes of other marginal commands (not meant for all users) 

# Adding measures/references from local files

```
Usage: cli.py add [OPTIONS] COMMAND [ARGS]...

  Add command group. (Adds Ref/Measure to DB from local files)

Options:
  --help  Show this message and exit.

Commands:
  measure    Add measure, who will be noted by comparing to reference...
  reference  Add a reference curve, if --ref-id is specified, upsert the...
```

## Adding a reference:

We can add a reference from a file_path. Please try always inputting a category
that makes sense for your reference curve.
```
Usage: cli.py add reference [OPTIONS]

  Add a reference curve, if --ref-id is specified, upsert the reference if a reference 
  with this id already exists either from the .sor file at `file_path`.
  (If it detects that this file already exist in the db i.e: same md5, does not do anything)

Options:
  --ref-id INTEGER  An integer ID
  --file-path PATH  File path of the form "foo.sor", please input either ip of
                    file_path  [required]
  --category TEXT   category column of the reference Table for easy filtering
                    of data
  --help            Show this message and exit.
```

Example:

`fibermark add reference --file-path=path/to/test.sor --category="Dummy Cat"`

One can specify a `--ref-id`, for exemple, imagine you want to overwrite reference at ref-id=24 because you deem it wrong and you corrected it. One can do:

`fibermark add reference --ref-id=24 --file-path=path/to/test.sor --category="Dummy Cat"`

## Adding a measure:

We can add a measure from a filepath. Consider you just measured a curve with FO: 23.27 and you would like to add this measure to db to compare it to older measures later. 

A measure must be compared to a reference. Thus `--ref-id` is needed in all cases when adding a measure. As the info on the FO version for the measure is not in the .sor file on must input the name of the algorithm the measure is for.

```
Usage: cli.py add measure [OPTIONS]

  Add measure of alg --alg, who will be noted by comparing to reference `--ref-id` from a
  local filepath

Options:
  --ref-id INTEGER  An integer ID  [required]
  --file-path PATH  File path of the form "foo.sor"  [required]
  --alg TEXT        [required]
  --help            Show this message and exit.
```

Example:

`fibermark add measure --ref-id=1 --file-path=path/to/test.sor  --alg="FO: 23.27"`

# Adding measures/references from a remote base:

```
Usage: cli.py remote [OPTIONS] COMMAND [ARGS]...

  Remote command group. (Upserts to DB from remote)

Options:
  --help  Show this message and exit.

Commands:
  eval-fo    Evaluates FO, from all curves in reference of connected DB
  measure    Add measure, who will be noted by comparing to reference...
  reference  Add a reference curve, if --ref-id is specified, upsert the...
```

## Adding a reference from remote:

One may want to add a reference from a remote base. The program gets the remote file/measure state and upserts it as reference.

```
Usage: cli.py remote reference [OPTIONS]

  Add a reference curve, if --ref-id is specified, upsert the reference either
  from the file_path (using local state of the file) or from a base whose IP
  is inputted (if ip inputted, needs user and password for base) (replace if
  it exists already and iff no file with this md5 exist in DB)

Options:
  --ref-id INTEGER  An integer ID
  --ip TEXT         IP address of a base like "10.33.17.123", please input
                    either ip of file_path  [required]
  --user TEXT       ftp_user to connect to IP  [required]
  --passwd TEXT     ftp_passwd to connect to IP  [required]
  --category TEXT   category column of the reference Table for easy filtering
                    of data
  --help            Show this message and exit.
```

Example:

`fibermark remote reference --ip=base-4000-ng-00488 --user="root" --passwd="4m0t0s0"`

As for `add reference` one can specify an optional `--ref-id` to overwrite an existing reference.

## Adding a measure from remote:

One may want to add a measure from a remote base. The program gets the algorithm by asking FO and upserts the measure.

```
Usage: cli.py remote measure [OPTIONS]

  Add measure, who will be noted by comparing to reference `--ref-id` from an
  ip address

Options:
  --ref-id INTEGER  An integer ID  [required]
  --ip TEXT         IP address of a base like "10.33.17.123", please input
                    either ip of file_path  [required]
  --user TEXT       ftp_user to connect to IP  [required]
  --passwd TEXT     ftp_passwd to connect to IP  [required]
  --help            Show this message and exit.
```

Example:

`fibermark remote measure --ref-id=1 --ip=localhost --user="aboussejra" --passwd="users123"`

# Inspecting info on curves, marks, algo-marks:
All those commands outputs in a tabular format the data stored in the DB:

```
Usage: cli.py show [OPTIONS] COMMAND [ARGS]...

  Show command group.

Options:
  --help  Show this message and exit.

Commands:
  algo       Output a tabular format of all info on algo and their...
  algo-mark  Show mark of an algorithm on all curve
  mark       Show mark of an algorithm on given curve
  measure    Output a tabular format of info for a measure on a curve...
  reference  Outputs a tabular format of all info on curves
```

## Seeing algo list:

Straightforwardly looking at algo list in DB.

Example:
`fibermark show algo`

```
  id  name
----  ---------
  70  dummy
  68  FO: 22.64
  69  FO: 23.22
   1  reference
```
## Seeing mark on an algorithm:

We may look at an algorithm mark on all existing measures from this algorithm. We may mark measures/algo on different metrics (corresponding to configurations in FO)
We currently have All/Auto (meaning we evaluate on all Events, or we filter Events with Auto FO config).

```
Usage: cli.py show algo-mark [OPTIONS]

  Show mark of an algorithm on all curve

Options:
  --alg TEXT                  Algorithm name  [required]
  --metric-filter [All|Auto]  Defaults to All
  --help                      Show this message and exit.
```
 Example:

`fibermark show algo-mark --alg="22.64" --metric-filter=Auto`

Output example:

| id   | algorithm_id   | metric_filter   | curve_count_for_mark_calculation   | nb_false_negatives_splice   | nb_false_positives_splice   | nb_true_positives_splice   | nb_false_negatives_reflection   | nb_false_positives_reflection   | nb_true_positives_reflection   | nb_false_negatives_ghost   | nb_false_positives_ghost   | nb_true_positives_ghost   | nb_false_negatives_fiberend   | nb_false_positives_fiberend   | nb_true_positives_fiberend   | nb_false_negatives_overall   | nb_false_positives_overall   | nb_true_positives_overall   | f_score_splice   | f_score_reflection   | f_score_ghost   | f_score_overall   | f_score_fiberend   |
|------|----------------|-----------------|------------------------------------|-----------------------------|-----------------------------|----------------------------|---------------------------------|---------------------------------|--------------------------------|----------------------------|----------------------------|---------------------------|-------------------------------|-------------------------------|------------------------------|------------------------------|------------------------------|-----------------------------|------------------|----------------------|-----------------|-------------------|--------------------|
| ---- | -------------- | --------------- | ---------------------------------- | --------------------------- | --------------------------- | -------------------------- | ------------------------------- | ------------------------------- | ------------------------------ | -------------------------- | -------------------------- | ------------------------- | ----------------------------- | ----------------------------- | ---------------------------- | ---------------------------- | ---------------------------- | --------------------------- | ---------------- | -------------------- | --------------- | ----------------- | ------------------ |
| 8001 | 68             | {'Auto'}        | 441                                | 1360                        | 149                         | 1784                       | 555                             | 104                             | 338                            | 63                         | 62                         | 190                       | 102                           | 102                           | 338                          | 2080                         | 417                          | 2650                        | 0.702777         | 0.506367             | 0.752475        | 0.679749          | 0.76818            |
|      |                |                 |                                    |                             |                             |                            |                                 |                                 |                                |                            |                            |                           |                               |                               |                              |                              |                              |                             |                  |                      |                 |                   |                    |

## Seeing mark on a measure:
This permits to look at marks on all metrics filters for a given algorithm for a given curve referred by ref-id (if curve exists)
```
Usage: cli.py show mark [OPTIONS]

  Show mark of an algorithm on given curve

Options:
  --ref-id INTEGER  An integer ID who point to a reference curve in DB
                    [required]
  --alg TEXT        Algorithm name  [required]
  --help            Show this message and exit.
```

Example:

`fibermark show mark --ref-id=10 --alg=22.64`

Output example:

| id    | measure_id   | treshold_classification_meters   | metric_filter   | nb_false_negatives_splice   | nb_false_positives_splice   | nb_true_positives_splice   | nb_false_negatives_reflection   | nb_false_positives_reflection   | nb_true_positives_reflection   | nb_false_negatives_ghost   | nb_false_positives_ghost   | nb_true_positives_ghost   | nb_false_negatives_fiberend   | nb_false_positives_fiberend   | nb_true_positives_fiberend   | nb_false_negatives_overall   | nb_false_positives_overall   | nb_true_positives_overall   | f_score_splice   | f_score_reflection   | f_score_ghost   | f_score_fiberend   | f_score_overall   |
|-------|--------------|----------------------------------|-----------------|-----------------------------|-----------------------------|----------------------------|---------------------------------|---------------------------------|--------------------------------|----------------------------|----------------------------|---------------------------|-------------------------------|-------------------------------|------------------------------|------------------------------|------------------------------|-----------------------------|------------------|----------------------|-----------------|--------------------|-------------------|
| ----- | ------------ | -------------------------------- | --------------- | --------------------------- | --------------------------- | -------------------------- | ------------------------------- | ------------------------------- | ------------------------------ | -------------------------- | -------------------------- | ------------------------- | ----------------------------- | ----------------------------- | ---------------------------- | ---------------------------- | ---------------------------- | --------------------------- | ---------------- | -------------------- | --------------- | ------------------ | ----------------- |
| 46574 | 452          | 3                                | {'All'}         | 14                          | 0                           | 0                          | 5                               | 0                               | 0                              | 0                          | 0                          | 0                         | 1                             | 1                             | 0                            | 20                           | 1                            | 0                           | 0.702777         | 0.506367             | 0.752475        | 0.679749           | 0.76818           |
| 46575 | 452          | 3                                | {'Auto'}        | 7                           | 0                           | 0                          | 3                               | 0                               | 0                              | 0                          | 0                          | 0                         | 1                             | 1                             | 0                            | 11                           | 1                            | 0                           |                  |                      |                 |                    |                   |

## Showing info on a measure:
One may want to know when a measure of a given algorithm has been done, or the `algorithm_id` in the DB.

```
Usage: cli.py show measure [OPTIONS]

  Output a tabular format of info for a measure on a curve identified by ref-
  id of a given algorithm

Options:
  --ref-id INTEGER  An integer ID  [required]
  --alg TEXT        Algorithm name  [required]
  --help            Show this message and exit.
```

Example:

`fibermark show measure --ref-id=1 --alg="22.64"`

Output example:

| id   | date       | algorithm_id   | reference_id   |
|------|------------|----------------|----------------|
| ---- | ---------- | -------------- | -------------- |
| 443  | 2023-05-11 | 68             | 1              |

## Showing info on a reference:
One may want to know when a reference of a given algorithm has been done, or the `algorithm_id` in the DB.

```
Usage: cli.py show reference [OPTIONS]

  Outputs a tabular format of all info on curves

Options:
  --ref-id INTEGER  An integer ID
  --help            Show this message and exit.
```

If no `--ref-id` is specified, all references info are shown.

Example:
`fibermark show reference --ref-id=2`
Output example:

| id   | name     | path                            | module   | date       | pulse_ns   | acq_range_km   | laser   | resolution_cm   | acquisition_time_sec   | n     | k   | category   | md5                              |
|------|----------|---------------------------------|----------|------------|------------|----------------|---------|-----------------|------------------------|-------|-----|------------|----------------------------------|
| ---- | -------- | ------------------------------- | -------- | ---------- | ---------- | -------------- | ------- | --------------- | ---------------------- | ----- | --- | ---------- | -------------------------------- |
| 2    | 3231.sor | /mnt/Work/Prof_v3_Storage/2.sor | E136FB   | 2023-05-11 | 3          | 20             | 1310    | 4               | 299                    | 1.465 | -79 | TEMP       | d04854c5e12455ab8ef9698b401fb664 |

# Comparing marks on measure/algo:

A main goal of this tool is comparing marks/performances on a given measure or given algorithm and make excel reports of FO measure performance

```
Usage: cli.py compare [OPTIONS] COMMAND [ARGS]...

  Compare command group.

Options:
  --help  Show this message and exit.

Commands:
  algo-to-ref  Compare algorithm to reference for a given metric-filter
  algos        Compare two algorithms overall performance for a given...
  measure      Compare two measures of two algorithms reffering to...
```

## Comparing two measures of two algorithms:

We can compare two measures to see differences in performance:
```
Usage: cli.py compare measure [OPTIONS]

  Compare two measures of two algorithms reffering to --ref-id for a given
  metric-filter

Options:
  --ref-id INTEGER            An integer ID  [required]
  --alg-1 TEXT                Algorithm name 1  [required]
  --alg-2 TEXT                Algorithm name 2  [required]
  --metric-filter [All|Auto]
  --help                      Show this message and exit.
```

Example:

`fibermark compare measure --ref-id=24 --alg-1="22.64" --alg-2="23.22"`

This prints out an object called `DiffMarks` whose values are positive if --alg-2 is better than --alg-1. Values are None if both fields are None (can occur for f_scores which is not always calculable) 

```
@dataclass
class DiffMarks:
    """
    Diff marks contains fields with mark_2 - mark_1 if both fields are not None,
    else it considers None is 0 and apply the same operation
    """

    diff_nb_true_positives_splice: int
    diff_nb_false_negatives_splice: int
    diff_nb_false_positives_splice: int
    diff_f_score_splice: Optional[float]
    diff_nb_true_positives_reflection: int
    diff_nb_false_negatives_reflection: int
    diff_nb_false_positives_reflection: int
    diff_f_score_reflection: Optional[float]
    diff_nb_true_positives_ghost: int
    diff_nb_false_negatives_ghost: int
    diff_nb_false_positives_ghost: int
    diff_f_score_ghost: Optional[float]
    diff_nb_true_positives_fiberend: int
    diff_nb_false_negatives_fiberend: int
    diff_nb_false_positives_fiberend: int
    diff_f_score_fiberend: Optional[float]
    diff_nb_true_positives_overall: int
    diff_nb_false_negatives_overall: int
    diff_nb_false_positives_overall: int
    diff_f_score_overall: Optional[float]
```

## Comparing overall perf of two algorithms:

We may do the same comparison for two algorithms overall performance:

```
Usage: cli.py compare algo [OPTIONS]

  Compare two algorithms overall performance for a given metric-filter

Options:
  --alg-1 TEXT                Algorithm name 1  [required]
  --alg-2 TEXT                Algorithm name 2  [required]
  --metric-filter [All|Auto]
  --help                      Show this message and exit.
```

Example:

`fibermark compare algo --alg-1="22.64" --alg-2="23.22"`

An object similar as measure comparison is outputted.

One may compare to reference too by doing:

`fibermark compare algo --alg-1="22.64" --alg-2="reference"`

That could yield:
`DiffMarks(diff_nb_true_positives_splice=-2095, diff_nb_false_negatives_splice=2087, diff_nb_false_positives_splice=200, diff_f_score_splice=0.37217249796582585, diff_nb_true_positives_reflection=-787, diff_nb_false_negatives_reflection=781, diff_nb_false_positives_reflection=260, diff_f_score_reflection=0.576092971776425, diff_nb_true_positives_ghost=-65, diff_nb_false_negatives_ghost=63, diff_nb_false_positives_ghost=62, diff_f_score_ghost=0.24752475247524763, diff_nb_true_positives_fiberend=-104, diff_nb_false_negatives_fiberend=102, diff_nb_false_positives_fiberend=102, diff_f_score_fiberend=0.23181818181818192, diff_nb_true_positives_overall=-3051, diff_nb_false_negatives_overall=3033, diff_nb_false_positives_overall=624, diff_f_score_overall=0.39166755917318197)`

Which permits us to see we miss 2095 splice events.

# More anectodic/debug commands (not meant for all users):

## Noting an algorithm/measure:

This is in case one would like to re-note an algo/measure because notation changed 
(normally they do not need to be used by themselves as notations are updated on each measure addition).

```
Usage: cli.py note [OPTIONS] COMMAND [ARGS]...

  Note command group.

Options:
  --help  Show this message and exit.

Commands:
  algo     Note an algorithm
  measure  Note a measure
```

### Note an algo:

Example:

`fibermark note algo --alg="22.64"`

Example Output (AlgoMark object):

`AlgoMark(algorithm_id=68, curve_count_for_mark_calculation=441, detailed_mark=DetailedMark(metric_filter='All', nb_true_positives_splice=1929, nb_false_negatives_splice=2087, nb_false_positives_splice=200, f_score_splice=0.6278275020341741, nb_true_positives_reflection=383, nb_false_negatives_reflection=781, nb_false_positives_reflection=260, f_score_reflection=0.42390702822357496, nb_true_positives_ghost=190, nb_false_negatives_ghost=63, nb_false_positives_ghost=62, f_score_ghost=0.7524752475247524, nb_true_positives_fiberend=338, nb_false_negatives_fiberend=102, nb_false_positives_fiberend=102, f_score_fiberend=0.7681818181818181, nb_true_positives_overall=2840, nb_false_negatives_overall=3033, nb_false_positives_overall=624, f_score_overall=0.608332440826818))`

### Note a measure:

Example:

`fibermark note measure --ref-id=1 --alg=22.64`

Exxample Output: (MeasureMark object)

`MeasureMark(measure_id=443, treshold_classification_meters=3.0, detailed_mark=DetailedMark(metric_filter='All', nb_true_positives_splice=7, nb_false_negatives_splice=7, nb_false_positives_splice=1, f_score_splice=0.6363636363636364, nb_true_positives_reflection=3, nb_false_negatives_reflection=3, nb_false_positives_reflection=3, f_score_reflection=0.5, nb_true_positives_ghost=1, nb_false_negatives_ghost=1, nb_false_positives_ghost=0, f_score_ghost=0.6666666666666666, nb_true_positives_fiberend=0, nb_false_negatives_fiberend=1, nb_false_positives_fiberend=1, f_score_fiberend=None, nb_true_positives_overall=11, nb_false_negatives_overall=12, nb_false_positives_overall=5, f_score_overall=0.5641025641025642))`