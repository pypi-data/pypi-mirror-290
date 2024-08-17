<p align="center">
  <img alt="NSIDC logo" src="https://nsidc.org/themes/custom/nsidc/logo.svg" width="150" />
</p>

# gps-timemachine

GPS Time Machine provides the ability to convert a date and GPS time
(hours, minutes, seconds, fractions of second) to a datetime object.
GPS Time Machine adjusts for the offset between UTC and GPS time based
on the number of leap seconds for the specified date. Because the gap
between UTC and GPS times shift unpredictably based on when leap
seconds are added by the [International Earth Rotation and Reference
Systems Service
(IERS)](https://www.iers.org/IERS/EN/Home/home_node.html), GPS Time
Machine uses data from the U.S. Naval Observatory for this
adjustment. See [NOTES](NOTES.md) for more information.

[![CircleCI](https://circleci.com/bb/nsidc/gps-timemachine.svg?style=svg)](https://circleci.com/bb/nsidc/gps-timemachine)

[![Anaconda-Server Badge](https://anaconda.org/nsidc/gps-timemachine/badges/version.svg)](https://anaconda.org/nsidc/gps-timemachine)
[![Anaconda-Server Badge](https://anaconda.org/nsidc/gps-timemachine/badges/license.svg)](https://anaconda.org/nsidc/gps-timemachine)
[![Anaconda-Server Badge](https://anaconda.org/nsidc/gps-timemachine/badges/downloads.svg)](https://anaconda.org/nsidc/gps-timemachine)
[![Anaconda-Server Badge](https://anaconda.org/nsidc/gps-timemachine/badges/installer/conda.svg)](https://conda.anaconda.org/nsidc)


## Level of Support

This repository is not actively supported by NSIDC but we welcome issue
submissions and pull requests in order to foster community contribution.

See the [LICENSE](LICENSE) for details on permissions and warranties. Please
contact nsidc@nsidc.org for more information.

## Requirements

* [Miniconda3](https://conda.io/miniconda.html)

Install dependencies:

    $ conda env create -f ./environment.yml
    $ source activate gps-timemachine

## Installation

To install and use it in another project:

    $ conda install gps-timemachine

## Usage

TODO


## Credit

This content was developed by the National Snow and Ice Data Center with funding from
multiple sources.
