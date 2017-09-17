# Spinnaker_clouddriver Integration

## Overview

Get metrics from spinnaker_clouddriver service in real time to:

* Visualize and monitor spinnaker_clouddriver states
* Be notified about spinnaker_clouddriver failovers and events.

## Installation

Install the `dd-check-spinnaker_clouddriver` package manually or with your favorite configuration manager

## Configuration

Edit the `spinnaker_clouddriver.yaml` file to point to your server and port, set the masters to monitor

## Validation

When you run `datadog-agent info` you should see something like the following:

    Checks
    ======

        spinnaker_clouddriver
        -----------
          - instance #0 [OK]
          - Collected 39 metrics, 0 events & 7 service checks

## Compatibility

The spinnaker_clouddriver check is compatible with all major platforms
