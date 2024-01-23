# kedro-expectations
A tool to better integrate Kedro and Great Expectations

## Introduction

Kedro Expectations is a tool designed to make the use of Great Expectations (GE) within ProjetaAi projects easier. It is composed of a couple of commands and a hook, allowing the user to create suites and run validations based on the DataCatalog and using directly the Kedro input as it's called by the normal pipeline

## Features

- ⏳ Initialization of GE without having to worry about [datasources](https://docs.greatexpectations.io/docs/terms/datasource)
- 🎯 Creation of [GE suites](https://docs.greatexpectations.io/docs/terms/expectation_suite/) automatically, using the [Data Assistant](https://docs.greatexpectations.io/docs/terms/data_assistant/)
- 🚀 Running validations within the Kedro pipeline

## Installation

For now, the plugin can only be installed through this github repo, but soon it will be available at PyPI
It can be installed with pip and referenced in the requirements.txt file as "git+https://github.com/joao-pampanin/kedro-expectations.git@develop"

## Usage

### CLI Usage

The first step to use the plugin is running an init command. This command will create the base GE folder and create the only datasource the plugin needs

```bash
kedro expectations init
```

After the init command the plugin is ready to create expectation suites. It is possible to create expectation suites for Non-spark dataframe objects (there is no need to worry about file extension since Kedro Expectations gets all it needs from the Kedro input) and Partitioned datasets

Within partitioned datasets, it is possible to create generic expectations, meaning all the partitions will use that expectation, or specific expectations, meaning only the specified partition will use the generated expectation

Run the following command to create expectations suites:

```bash
kedro expectations create-suite
```

### Hook Usage

In order to enable the hook capabilities you only need to call it in the settings.py file inside your kedro project

(inside src/your_project_name/settings.py)
```bash
from kedro_expectations import KedroExpectationsHooks

HOOKS = (KedroExpectationsHooks(fail_fast=False),)
```

### Fail Fast

fail_fast is a parameter added to give more control over the pipeline. That way it is possible to define if a great expectations validation failure breaks the pipeline run (fail_fast = True) or not (fail_fast = False).

Its default value is "False", and to change it the only step necessary is to change the parameter value within your hook usage

```bash
HOOKS = (KedroExpectationsHooks(fail_fast=True),)
```

## Example

To make things clearer, the following example will approach the most complex usage of the plugin, which is when we want to create an specific expectation for a partitioned dataset. It was done using the [Partitioned Iris Starter](https://github.com/ProjetaAi/projetaai-starters/tree/main/for_projetaai/project/partitioned_projetaai)

To start using the plugin, make sure you are in your project's root folder and the pipeline is executing correctly

Considering you have the plugin installed and the conditions right above are true, the plugin should be used the following way:
- Run the init command
- Create one or more suites depending on your needs
- Make sure to enable the Kedro Great Hook in your project's settings
- Execute the Kedro Pipeline normally 

### Init and Suite Creation

The first step to use the plugin is to use the "kedro expectations init" command. Below we can see the expected result:

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/1_init.png">
</p>

As soon as it is created, we can run the second command: "kedro expectations create-suite"
You will be prompted to choose between (1) suites for generic datasets and (2) suites for partitioned datasets:

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/3_createsuite.png">
</p>

Then we can choose between a generic or an specific expectation. In this example, we will press (2) to create an specific one:

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/4_createsuite.png">
</p>

Now the plugin will ask three questions. The first two must be answered based on your project, and the last one is any name based on your preference

Our partitioned dataset structure inside the project:

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/8_createsuite.png">
</p>

Questions asked by the CLI:

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/5_createsuite.png">
</p>

The last step is to decide if we want to exclude some columns from the expectation suite. Whenever you selected you desired columns, type "0" (without quote marks):

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/6_createsuite.png">
</p>

Then your dataset will be validated automatically and will be found at great_expectations/expectations/"your_dataset_name"/"your_expectation_name"

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/7_createsuite.png">
</p>

### Adding the Hook

Now, to be able to test, we only need to add 2 lines of code in our settings.py file:

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/9_hookconfig.png">
</p>

For more information about the functionality of Kedro Hooks, please refer to the [Kedro Hook Documentation](https://kedro.readthedocs.io/en/stable/hooks/introduction.html)

### Running the Kedro project

After adding the Hook there is no extra step. You can simply run the project by typing the normal "kedro run" command. Whenever a dataset with an expectation suite is called by the pipeline, Kedro Expectations will validade it and add the results to the data_docs

<p align="center">
  <img src="https://gitlab.com/anacision/kedro-expectations/raw/main/images/10_run.png">
</p>
