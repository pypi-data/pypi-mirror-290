###
# #%L
# Marimo Notebook
# %%
# Copyright (C) 2021 Booz Allen
# %%
# This software package is licensed under the Booz Allen Public License. All Rights Reserved.
# #L%
###

import marimo

__generated_with = "0.6.22"
app = marimo.App(app_title="Sandbox")


@app.cell(hide_code=True)
def __(__file__):
    import marimo as mo
    import os
    import textwrap

    # Get file name for Links below
    current_file_path = os.path.abspath(__file__)
    file_name = os.path.basename(current_file_path)
    mo_file_path = f"?file={file_name}"
    return current_file_path, file_name, mo, mo_file_path, os, textwrap


@app.cell(hide_code=True)
def __(mo):
    mo.md(rf"# Sandbox Admin Console")
    return


@app.cell(hide_code=True)
def __(mo, mo_file_path):
    mo.md(
        rf"""
        Welcome to the Sandbox Admin Console! Here, we can experiment and perform typical AI/ML related tasks such as 
        data preparation, model training, inference, model tracking and much more.

        This environment utilizes:

        - Marimo Notebooks for general AI/ML work
        - MLFlow for model tracking

        It also provides the ability to connect to "common core" services you already have in use.

        This console provides some helpful code snippets and examples to get started. See the following sections for more information:

        - [Sandbox Wizard]({mo_file_path}#sandbox-wizard)
        - [Package Installer]({mo_file_path}#package-installer)
        - [Example Library]({mo_file_path}#example-library)
        - [Lifeline Services]({mo_file_path}#lifeline-services)
        - [Frequently Asked Question]({mo_file_path}#faq)
        """
    )
    return


@app.cell(hide_code=True)
def __(mo, mo_file_path):
    mo.md(
        rf"""
        <a id="sandbox-wizard"></a>
        ## Sandbox Wizard
        ---
        The **Sandbox Wizard** is a user-friendly interface for creating notebooks based on common workflows in AI/ML projects. 
        These notebooks are designed to aide and guide you in your AI/ML tasks while also providing structure and organization to your code.

        The Wizard is divided into two main sections, Free-Form Pipelines and Engineered Pipelines:

        - **Free-Form Pipelines**: These are open notebooks with markdown headers to help structure and organize your code. They are ideal for exploration and experimentation.
        - **Engineered Pipelines**: These notebooks provide method signatures and are aligned with best practices for enterprise-class usage. They are intended to help prepare your code for high-quality delivery.

        ### Why use these Notebooks?
        This structured approach helps ensure your code is organized and easy to follow. These notebooks adhere to best practices and will help prepare your code for deployment outside of a notebook environment.

        These notebooks are designed as guides so feel free to modify as needed to suit the specific requirements of your project.
        """
    )
    return


@app.cell(hide_code=True)
def __(determine_tab_content, mo):
    tabs = determine_tab_content()

    mo.vstack([mo.md("### Notebook Templates"), tabs])
    return (tabs,)


@app.cell(hide_code=True)
def __(mo, mo_file_path):
    mo.md(
        rf"""
        <a id="package-installer"></a>        
        ## Package Installer
        ---
        The **Package Installer** tool allows developers to install Python packages onto the Python environment.

        To use this tool, input the name of the package into the Package Name field. 
        
        Optionally, input the version of the package into the Package Version field. If Package Version is blank, the latest package would be installed. 
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    install_package_button = mo.ui.button(
        label="Install Package",
        on_click=lambda _: install_package(package_name.value, package_version.value),
    )
    package_name = mo.ui.text(label="Package Name", placeholder="Enter package name...")
    package_version = mo.ui.text(
        label="Package Version", placeholder="Enter package version..."
    )

    def install_package(name, version):
        import sys
        import subprocess

        if len(version) == 0:
            cmd = "cd /venv/bootstrap-env;poetry add %s" % name
            subprocess.run(cmd, shell=True)
            print("Package %s installed" % name)
        else:
            cmd = "cd /venv/bootstrap-env;poetry add %s==%s" % (name, version)
            subprocess.run(cmd, shell=True)
            print("Package %s==%s installed" % (name, version))

    mo.hstack(
        [package_name, package_version, install_package_button],
        justify="start",
    )


@app.cell(hide_code=True)
def __(mo, mo_file_path):
    mo.md(
        rf"""
        <a id="package-installer"></a>        
        ## Python Environment Switcher
        ---
        The **Python Environment Switcher** tool allows developers to switch Python environments the aiSSEMBLE Sandbox is running in.

        To use this tool, input the Python version into the Python Version field. Click the Change Environment button to change the environment.

        Once the environment switch is complete, you will be asked to exit out of the Admin Console as the aiSSEMBLE Sandbox will restart.

        If currently installed Python packages are not compatable with the Python environment you're trying to switch to, package versions can be changed using the **Package Installer**

        Note: Due to using the Marimo dependency in the aiSSEMBLE Sandbox, you will not be able to use any Python enviromnent with version less than 3.8.0.  
    
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    import platform

    python_env_button = mo.ui.button(
        label="Change Environment",
        on_click=lambda _: change_python_env(python_version.value),
    )

    python_version = mo.ui.text(
        label="Python Version", placeholder="Enter Python Version..."
    )

    def change_python_env(version):
        import os
        import subprocess
        import time
        import fileinput
        import shutil
        import re

        if len(version) == 0:
            print("Version is empty, invalid")
            return

        # Install new Python version
        cmd = "pyenv install %s" % version
        completed_process = subprocess.run(cmd, shell=True)
        return_code = completed_process.returncode
        if return_code != 0 and return_code != 1:
            # Returns a 1 if the Python version is already present, treating this as a success
            return

        # Copy pyproject.toml case environment switch fails
        pyproject_path = os.path.join("/", "venv", "bootstrap-env", "pyproject.toml")
        pyproject_dest_path = os.path.join("/", "tmp", "pyproject.toml")
        try:
            shutil.copy(pyproject_path, pyproject_dest_path)
        except:
            print("Internal error: Could not save environment to /tmp")
            return

        # Change the python version in the pyproject.toml file
        python_version = 'python = "%s"' % version
        for line in fileinput.input(pyproject_path, inplace=1):
            line = re.sub("^\s*python\s*=.*", python_version, line)
            print(line)

        cmd = """
                pyenv global %s;
                cd /venv/bootstrap-env;
                rm poetry.lock;
                poetry env use %s;
                poetry install;
                """ % (
            version,
            version,
        )
        completed_process = subprocess.run(cmd, shell=True)

        # If creating the new environment failed, revert back to the old one
        if completed_process.returncode != 0:
            current_python_version = platform.python_version()
            cmd = """
                    pyenv global %s;
                    cp /tmp/pyproject.toml /venv/bootstrap-env/pyproject.toml;
                    cd /venv/bootstrap-env;
                    poetry env use %s
                    """ % (
                current_python_version,
                current_python_version,
            )
            completed_process = subprocess.run(cmd, shell=True)
            return

        print("Exit out of the Admin Console. Restarting the aiSSEMBLE Sandbox....")
        time.sleep(10)

        # Restarts the aiSSEMBLE Sandbox
        parent_id = os.getppid()
        cmd = "kill %s" % parent_id
        subprocess.run(cmd, shell=True)

    current_python_version = platform.python_version()
    current_python_version_text = mo.md(
        "Current Python version: %s" % current_python_version
    )
    mo.hstack(
        [current_python_version_text, python_version, python_env_button],
        justify="start",
    )


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        <a id="example-library"></a>
        ## Example Library
        ---
        The **Example Library** is a curated collection of atomic, crisp examples designed to provide known recipes to 
        common problems. These examples offer practical solutions and best practices for AI/ML tasks.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    _spark_examples = mo.accordion(
        {
            "Imports": (
                """
                ```python
                from pyspark.sql import SparkSession
                from krausening.properties import PropertyManager
                from marimo_notebook.schema.dry_beans_ingest_schema import (
                    DryBeansIngestSchema,
                )
                ```
                """
            ),
            "Create Spark Session": (
                """
                ```python
                def create_spark_session() -> SparkSession:
                    properties = PropertyManager.get_instance().get_properties(
                        "spark-data-delivery.properties"
                    )
                    builder = SparkSession.builder
                    if properties.getProperty("execution.mode.legacy", "false") == "true":
                        builder = builder.master("local[*]").config(
                            "spark.driver.host", "localhost"
                        )
                    return builder.getOrCreate()
                ```
                """
            ),
            "Load a Data Set": (
                """
                ```python
                def load_data_set(data_path, spark):
                    _schema = DryBeansIngestSchema()

                    _df = spark.read.option("multiline", "true").json(
                        data_path, _schema.struct_type
                    )

                    return _df
                ```
                """
            ),
            "Run and Show Top 20 Results": (
                """
                ```python
                pyspark_session = create_spark_session()
                my_df = load_data_set("../../tests/resources/data/drybeans.json", pyspark_session)
                my_df.show(20)
                print(my_df.count())
                ```
                """
            ),
        }
    )

    spark_explanation = mo.md(
        """
        This example shows how to create a Spark Session and read data using a specific 
        schema
        """
    )

    _ml_examples = mo.md(
        """
        **More examples to come!**
        """
    ).callout(kind="info")

    mo.ui.tabs(
        {
            "💥 Spark Ingest Examples": mo.vstack([spark_explanation, _spark_examples]),
            "🤖 Machine Learning Examples": _ml_examples,
        }
    )
    return (spark_explanation,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        <a id="lifeline-services"></a>
        ## Lifeline Services
        ---
        The **Lifeline Services** section ensures that nothing is lost when turning off the sandbox environment. 
        By using these configurations, you can ensure that all your data, settings and components are 
        preserved through the lifecycle of the sandbox.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md("Lifeline services development is in progress").callout(kind="neutral")
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        rf"""
        <a id="faq"></a>
        ## Frequently Asked Questions
        ---
        The <strong>Frequently Asked Question (FAQ)</strong> section is available to provide additional usage details.

        * <strong>How is Marimo different from Jupyter?</strong>
            * Marimo is a reinvention of the Python notebook as a reproducible, interactive, and shareable Python program that can be executed as scripts or deployed as interactive web apps.
            * *<a href="https://docs.marimo.io/faq.html#choosing-marimo">Recommended reading: Learn more about Marimo & Jupyter differences here (~10 minute read)</a>*.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(
        """
        ---
        #### Appendix
        Functions and constants used throughout the Admin Console. Visible in edit mode.
        """
    )
    return


@app.cell(hide_code=True)
def __(mo):
    ## Sandbox Wizard: Constants, Dictionaries and State Variables ##

    ## Constants ##
    DATA_EXPLORATION_PREPARATION_FREEFORM = (
        "data_exploration_preparation_freeform_pipeline"
    )
    MODEL_TRAINING_EVALUATION_FREEFORM = "model_training_evaluation_freeform_pipeline"
    DATA_PREPARATION_ENGINEERED = "data_preparation_engineered_pipeline"
    MODEL_TRAINING_ENGINEERED = "model_training_engineered_pipeline"
    MODEL_INFERENCE_ENGINEERED = "model_inference_engineered_pipeline"
    FREEFORM_TEMPLATES = "freeform_templates"
    ENGINEERED_TEMPLATES = "engineered_templates"

    ## Dictionaries for File Contents ##
    freeform_templates_contents = {}
    freeform_templates_descriptions = {}
    engineered_templates_contents = {}
    engineered_templates_descriptions = {}

    ## State Variables
    get_notebook_message, set_notebook_message = mo.state(None)
    get_notebook_callout, set_notebook_callout = mo.state(None)
    get_active_tab, set_active_tab = mo.state(FREEFORM_TEMPLATES)
    get_selected_option, set_selected_option = mo.state(False)
    get_template_options, set_template_options = mo.state(
        {
            "Data Exploration and Preparation": DATA_EXPLORATION_PREPARATION_FREEFORM,
            "Model Training and Evaluation": MODEL_TRAINING_EVALUATION_FREEFORM,
        }
    )
    return (
        DATA_EXPLORATION_PREPARATION_FREEFORM,
        DATA_PREPARATION_ENGINEERED,
        MODEL_INFERENCE_ENGINEERED,
        MODEL_TRAINING_EVALUATION_FREEFORM,
        MODEL_TRAINING_ENGINEERED,
        ENGINEERED_TEMPLATES,
        FREEFORM_TEMPLATES,
        get_active_tab,
        get_notebook_callout,
        get_notebook_message,
        get_selected_option,
        get_template_options,
        engineered_templates_contents,
        engineered_templates_descriptions,
        set_active_tab,
        set_notebook_callout,
        set_notebook_message,
        set_selected_option,
        set_template_options,
        freeform_templates_contents,
        freeform_templates_descriptions,
    )


@app.cell(hide_code=True)
def __(generate_notebook, get_template_options, mo, on_dropdown_change):
    ## Sandbox Wizard: Dropdown Menu and Button

    # Dropdown Menu
    notebook_type = mo.ui.dropdown(get_template_options(), on_change=on_dropdown_change)

    # Generate Notebook button
    generate_button = mo.ui.button(
        label="Generate Notebook",
        on_click=lambda _: generate_notebook(notebook_type.value),
    )
    return generate_button, notebook_type


@app.cell(hide_code=True)
def __(
    DATA_EXPLORATION_PREPARATION_FREEFORM,
    DATA_PREPARATION_ENGINEERED,
    MODEL_TRAINING_EVALUATION_FREEFORM,
    MODEL_TRAINING_ENGINEERED,
    MODEL_INFERENCE_ENGINEERED,
    ENGINEERED_TEMPLATES,
    FREEFORM_TEMPLATES,
    get_active_tab,
    os,
    engineered_templates_contents,
    set_active_tab,
    set_notebook_callout,
    set_notebook_message,
    set_selected_option,
    set_template_options,
    freeform_templates_contents,
    textwrap,
):
    ## Sandbox Wizard: Tab/Dropdown Changes and Generate Notebook Functions ##

    def on_tab_change(_) -> None:
        """
        Handles the event when the tab is changed, resetting the notebook message and
        resetting and updating the template options
        """
        set_notebook_message(None)
        set_selected_option(False)

        if get_active_tab() == FREEFORM_TEMPLATES:
            set_active_tab(ENGINEERED_TEMPLATES)
            set_template_options(
                {
                    "Data Preparation": DATA_PREPARATION_ENGINEERED,
                    "Model Training": MODEL_TRAINING_ENGINEERED,
                    "Model Inference": MODEL_INFERENCE_ENGINEERED,
                }
            )
        else:
            set_active_tab(FREEFORM_TEMPLATES)
            set_template_options(
                {
                    "Data Exploration and Preparation": DATA_EXPLORATION_PREPARATION_FREEFORM,
                    "Model Training and Evaluation": MODEL_TRAINING_EVALUATION_FREEFORM,
                }
            )

    def on_dropdown_change(value) -> None:
        """
        Handles the event when the dropdown selection changes, resetting the notebook
        message and updating the selected option state.
        """
        set_notebook_message(None)
        if value is None:
            set_selected_option(False)
        else:
            set_selected_option(True)

    def generate_notebook(nb_type) -> None:
        """
        Generates a notebook file based on the selected template type.
        """
        if not nb_type:
            set_notebook_message("No notebook was selected from the dropdown.")
            set_notebook_callout("warn")
            return

        file_name = f"{nb_type}.py"
        if os.path.exists(file_name):
            set_notebook_message(
                f'File "{file_name}" already exists in the current directory. Rename or delete the file and try again.'
            )
            set_notebook_callout("danger")
            return

        try:
            if get_active_tab() == FREEFORM_TEMPLATES:
                file_contents = textwrap.dedent(freeform_templates_contents[nb_type])
            else:
                file_contents = textwrap.dedent(engineered_templates_contents[nb_type])

            with open(file_name, "w") as f:
                f.write(file_contents)

            set_notebook_message(
                f"{file_name} created successfully! Open the file explorer in the left menu and refresh to see the new file."
            )
            set_notebook_callout("success")

        except KeyError:
            set_notebook_message(
                "The selected notebook type is invalid. Please choose a valid template."
            )
            set_notebook_callout("danger")
        except Exception as e:
            set_notebook_message(f"An error occurred while creating the notebook: {e}")
            set_notebook_callout("danger")

    return generate_notebook, on_dropdown_change, on_tab_change


@app.cell(hide_code=True)
def __(
    FREEFORM_TEMPLATES,
    generate_button,
    get_active_tab,
    get_notebook_callout,
    get_notebook_message,
    get_selected_option,
    mo,
    notebook_type,
    on_tab_change,
    engineered_templates_descriptions,
    freeform_templates_descriptions,
):
    ## Sandbox Wizard: Display tab content functions ##
    def determine_tab_content() -> mo.ui.tabs:
        """
        Determines the content to display in the tabs based on the current selection
        and message state
        """
        if not get_selected_option():
            tabs = mo.ui.tabs(
                {
                    "**Free-Form Pipelines**": notebook_type.center(),
                    "**Engineered Pipelines**": notebook_type.center(),
                },
                on_change=on_tab_change,
            )

        elif not get_notebook_message():
            description = get_description()
            tabs = mo.ui.tabs(
                {
                    "**Free-Form Pipelines**": mo.vstack(
                        [
                            notebook_type.center(),
                            mo.md(description),
                            generate_button.center(),
                        ]
                    ),
                    "**Engineered Pipelines**": mo.vstack(
                        [
                            notebook_type.center(),
                            mo.md(description),
                            generate_button.center(),
                        ]
                    ),
                },
                on_change=on_tab_change,
            )

        else:
            description = get_description()
            tabs = mo.ui.tabs(
                {
                    "**Free-Form Pipelines**": mo.vstack(
                        [
                            notebook_type.center(),
                            mo.md(description),
                            generate_button.center(),
                            mo.md(f"{get_notebook_message()}")
                            .callout(kind=get_notebook_callout())
                            .center(),
                        ]
                    ),
                    "**Engineered Pipelines**": mo.vstack(
                        [
                            notebook_type.center(),
                            mo.md(description),
                            generate_button.center(),
                            mo.md(f"{get_notebook_message()}")
                            .callout(kind=get_notebook_callout())
                            .center(),
                        ]
                    ),
                },
                on_change=on_tab_change,
            )

        return tabs

    def get_description() -> None:
        """
        Retrieves the description for the selected notebook template
        """
        if get_active_tab() == FREEFORM_TEMPLATES:
            return freeform_templates_descriptions[notebook_type.value]
        else:
            return engineered_templates_descriptions[notebook_type.value]

    return determine_tab_content, get_description


@app.cell(hide_code=True)
def __(
    DATA_EXPLORATION_PREPARATION_FREEFORM,
    MODEL_TRAINING_EVALUATION_FREEFORM,
    freeform_templates_contents,
):
    ## Sandbox Wizard: Free-Form Pipeline File Contents ##

    freeform_templates_contents[
        DATA_EXPLORATION_PREPARATION_FREEFORM
    ] = '''
        import marimo

        __generated_with = "0.6.19"
        app = marimo.App(width="medium")


        @app.cell(hide_code=True)
        def __():
            import marimo as mo
            return mo,


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                """
                # Data Exploration and Preparation Free-Form Pipeline
                Welcome to the Data Exploration and Preparation Free-Form Pipeline. This notebook provides a structured yet flexible environment to explore data, perform initial analysis and prepare data for model training. The notebook is divided into two key sections to help organize your code:

                ## Sections Overview
                - **Data Exploration:** Load, inspect and visualize your data. Perform initial statistical analysis to understand the data.
                - **Data Preparation:** Clean, preprocess and manipulate your data, including transformations, enrichment and validation.

                Feel free to modify and expand upon these sections as needed to suit the specific requirements of your project. Happy Coding!
                """
            )
            return


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                """
                ## Data Exploration
                - Initial data inspection (e.g. loading data, viewing columns and rows)
                - Basic statistics and visualizations (e.g. summary statistics, histograms, box plots)
                """
            )
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                """
                ## Data Preparation
                - Data Cleaning (e.g. Handling missing values, removing duplicates)
                - Feature Engineering (e.g. create new features, encode categorical variables)
                """
            )
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        if __name__ == "__main__":
            app.run()
    '''

    freeform_templates_contents[
        MODEL_TRAINING_EVALUATION_FREEFORM
    ] = '''
        import marimo

        __generated_with = "0.6.19"
        app = marimo.App(width="medium")


        @app.cell(hide_code=True)
        def __():
            import marimo as mo
            return mo,


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                """
                # Model Training and Evaluation Free-Form Pipeline
                Welcome to the Model Training and Evaluation Free-Form Pipeline. This notebook provides a structured yet flexible environment to train models and evaluate their performance. The notebook is divided into two key sections to help organize your code:

                ## Sections Overview
                - **Model Training:** Select and train your machine learning model(s). Experiment with different models, algorithms and hyperparamters to find the best performance.
                - **Model Evaluation:** Assess the performance of your model(s) using various metrics and visualizations.

                Feel free to modify and expand upon these sections as needed to suit the specific requirements of your project. Happy Coding!
                """
            )
            return


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                rf"""
                ## Model Training
                - Model Selection
                - Training the model(s)
                - Hyperparameter tuning
                """
            )
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                rf"""
                ## Model Evaluation
                - Evaluate model performance on the test set
                - Metrics and visualizations (e.g. confusion matrix, ROC curve)
                """
            )
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        @app.cell
        def __():
            return


        if __name__ == "__main__":
            app.run()
    '''
    return


@app.cell(hide_code=True)
def __(
    DATA_EXPLORATION_PREPARATION_FREEFORM,
    MODEL_TRAINING_EVALUATION_FREEFORM,
    freeform_templates_descriptions,
):
    ## Sandbox Wizard: Free-Form Pipeline Descriptions ##

    freeform_templates_descriptions[
        DATA_EXPLORATION_PREPARATION_FREEFORM
    ] = """
    ### Data Exploration and Preparation Free-Form Pipeline
    The Data Exploration and Preparation Free-Form Pipeline offers a structured yet flexible environment to explore data, perform initial analysis and prepare data for model training. The notebook is divided into two key sections:

    - **Data Exploration:** Load, inspect and visualize your data. Perform initial statistical analysis to understand the data.
    - **Data Preparation:** Clean, preprocess and manipulate your data, including transformations, enrichment and validation.
    """

    freeform_templates_descriptions[
        MODEL_TRAINING_EVALUATION_FREEFORM
    ] = """
    ### Model Training and Evaluation Free-Form Pipeline
    The Model Training and Evaluation Free-Form Pipeline offers a structured yet flexible environment to train models and evaluate their performance. The notebook is divided into two key sections:

    - **Model Training:** Select and train your machine learning model(s). Experiment with different models, algorithms and hyperparamters to find the best performance.
    - **Model Evaluation:** Assess the performance of your model(s) using various metrics and visualizations.
    """
    return


@app.cell(hide_code=True)
def __(
    DATA_PREPARATION_ENGINEERED,
    MODEL_TRAINING_ENGINEERED,
    MODEL_INFERENCE_ENGINEERED,
    engineered_templates_contents,
):
    ## Sandbox Wizard: Engineered Pipeline File Contents ##

    engineered_templates_contents[
        DATA_PREPARATION_ENGINEERED
    ] = '''
        import marimo

        __generated_with = "0.6.22"
        app = marimo.App(width="medium")


        @app.cell(hide_code=True)
        def __():
            import marimo as mo
            return mo,


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                """
                # Data Preparation Engineered Pipeline
                Welcome to the Data Preparation Engineered Pipeline. This notebook provides scaffolding for commonly used data preparation methods. By following these method signatures, you can seamlessly transition your notebook code to be used in enterprise-level data pipelines.

                ## Method Signature Overview
                - `load_data`: Load a dataset
                - `transform_data`: Apply data transformations
                - `enrich_data`: Enrich your data
                - `validate_data`: Validate your data

                These method signatures are intended as a guide. Feel free to edit and update them as needed to fit your specific requirements. Happy coding!
                """
            )
            return


        @app.cell
        def __():
            import pandas as pd
            # Add additional imports
            return pd,


        @app.cell
        def __(pd):
            def load_data(file_path: str) -> pd.DataFrame:
                """
                Load data from a file into a DataFrame.

                Args:
                    file_path (str): The path to the data file.

                Returns:
                    pd.DataFrame: The loaded data as a DataFrame.
                """
                try:
                    data_frame = pd.read_csv(file_path)
                except Exception as e:
                    print(f"Error loading data: {e}")
                    return pd.DataFrame()
                return data_frame
            return load_data,


        @app.cell
        def __():
            # Test load_data - Update file_path, uncomment and run
            # df = load_data(<file_path>)
            # df.head()
            return


        @app.cell
        def __(pd):
            def transform_data(data_frame: pd.DataFrame) -> pd.DataFrame:
                """
                Update with project-specific data transformation steps.

                Args:
                    data_frame (pd.DataFrame): The input data frame to transform.

                Returns:
                    pd.DataFrame: The transformed data frame.
                """
                df_transformed = data_frame.copy()

                # Your transformation code here

                return df_transformed
            return transform_data,


        @app.cell
        def __():
            # Test transform_data - Update data_frame, uncomment and run
            # df_transformed = transform_data(<data_frame>)
            # df_transformed.head()
            return
            
        
        @app.cell
        def __():
            # Save df_transformed - update file_name as needed, uncomment and run
            # save_data(df_transformed, "transformed_data.csv")
            return


        @app.cell
        def __(pd):
            def enrich_data(data_frame: pd.DataFrame) -> pd.DataFrame:
                """
                Update with project-specific data enrichment steps.

                Args:
                    data_frame (pd.DataFrame): The input data frame to enrich.

                Returns:
                    pd.DataFrame: The enriched data frame.
                """
                df_enriched = data_frame.copy()

                # Your enrichment code here

                return df_enriched
            return enrich_data,


        @app.cell
        def __():
            # Test enrich_data - Update data_frame, uncomment and run
            # df_enriched = enrich_data(<data_frame>)
            # df_enriched.head()
            return


        @app.cell
        def __():
            # Save df_enriched - update file_name as needed, uncomment and run
            # save_data(df_enriched, "enriched_data.csv")
            return
        
        @app.cell
        def __(pd):
            def validate_data(data_frame: pd.DataFrame) -> None:
                """
                Validate the data frame based on project-specific validation rules.

                Args:
                    data_frame (pd.DataFrame): The input data frame to validate.

                Returns:
                    None
                """

                # Your validation code here

                pass
            return validate_data,


        @app.cell
        def __():
            # Test validate_data - Update data_frame, uncomment and run
            # validate_data(<data_frame>)
            return


        @app.cell
        def __(pd):
            def save_data(data_frame: pd.DataFrame, file_name: str) -> None:
                """
                Save the DataFrame to a CSV file.
        
                Args:
                    data_frame (pd.DataFrame): Data to be saved.
                    file_name (str): Name of the CSV file.
        
                Returns:
                    None
                """
                try:
                    data_frame.to_csv(file_name, index=False)
                    print(f"Data saved to {file_name}")
                except Exception as e:
                    print(f"An error occurred while saving the data: {e}")
            return save_data,
        
        if __name__ == "__main__":
            app.run()
    '''

    engineered_templates_contents[
        MODEL_TRAINING_ENGINEERED
    ] = '''
        import marimo

        __generated_with = "0.7.0"
        app = marimo.App(width="medium")


        @app.cell(hide_code=True)
        def __():
            import marimo as mo
            return mo,


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                """
                # Model Training Engineered Pipeline
                Welcome to the Model Training Engineered Pipeline. This notebook provides scaffolding for commonly used machine learning tasks. By following these method signatures, you can seamlessly transition your notebook code to be used in enterprise-level data and machine learning pipelines.
        
                ## Method Signature Overview
                - `load_dataset`: Load a dataset
                - `prep_dataset`: Last-mile data preparation prior to model training
                - `select_features`: Select relevant features for your model
                - `split_dataset`: Split your dataset into training and testing sets
                - `train_model`: Train your machine learning model
                - `evaluate_model`: Evaluate the performance of your model 
                - `save_model`: Save your trained model
                - `run`: Run the pipeline
        
                These method signatures are intended as a guide. Feel free to edit and update them as needed to fit your specific requirements. Happy coding!
                """
            )
            return


        @app.cell
        def __():
            from datetime import datetime
            import mlflow
            import pandas as pd
            # Add additional imports
            return datetime, mlflow, pd


        @app.cell
        def __(pd):
            def load_dataset(file_path: str) -> pd.DataFrame:
                """
                Load data from a file into a DataFrame.
        
                Args:
                    file_path (str): The path to the data file.
        
                Returns:
                    pd.DataFrame: The loaded data as a DataFrame.
                """
                
                print(f"Loading dataset from {file_path}")
                return pd.read_csv(file_path)
            return load_dataset,


        @app.cell
        def __(pd):
            def prep_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
                """
                Implement last-mile data preparation on the loaded dataset.
        
                Args:
                    dataset (pd.DataFrame): The input dataset.
        
                Returns:
                    pd.DataFrame: The prepped dataset to be used for model training
                """
        
                print("Preparing dataset")
                # TODO: Implement any data prep steps
                return dataset
            return prep_dataset,


        @app.cell
        def __(pd):
            def select_features(dataset: pd.DataFrame) -> list[str]:
                """
                Select relevant features from the dataset.
        
                Args:
                    dataset (pd.DataFrame): The input dataset.
        
                Returns:
                    list[str]: List of columns to be used as features.
                """
        
                print("Selecting features")
                # TODO: select features from the dataset
                selected_features = dataset.columns.tolist()
                return selected_features
            return select_features,


        @app.cell
        def __(pd):
            def split_dataset(dataset: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
                """
                Split the dataset into training and testing sets.
        
                Args:
                    dataset (pd.DataFrame): The input dataset.
        
                Returns:
                    tuple[pd.DataFrame, pd.DataFrame]: Training and testing datasets.
                """
        
                print("Splitting dataset into training and testing sets")
                # TODO: create training/testing splits
                train_split = None
                test_split = None
                return train_split, test_split
            return split_dataset,


        @app.cell
        def __(pd):
            # TODO: Update the return type of this to match your expected model type such as LogisticRegression or Sequential.
            def train_model(train_dataset: pd.DataFrame) -> any:
                """
                Train the machine learning model.
        
                Args:
                    train_dataset (pd.DataFrame): The training dataset.
        
                Returns:
                    any: The trained model.
                """
        
                print("Training model")
                # TODO: create model based on what return type is needed
                model = None
        
                # TODO: Train the model using model.fit(...) on the training split
        
                return model
            return train_model,


        @app.cell
        def __(pd):
            # TODO: Update the model type to match what is returned in the train_model method
            def evaluate_model(model: any, test_dataset: pd.DataFrame) -> float:
                """
                Evaluate the performance of the trained machine learning model.
        
                Args:
                    model (any): The trained model.
                    test_dataset (pd.DataFrame): The testing dataset.
        
                Returns:
                    float: The evaluation score.
                """
        
                print("Evaluating model")
                # TODO: evaluate model using model.predict(...) on the testing split
                # TODO: obtain the evaluation score using model.score(...) on the testing split
                score = 0
        
                return score
            return evaluate_model,


        @app.cell
        def __():
            # TODO: Update the model type to match what is returned in the train_model method
            def save_model(model: any) -> None:
                """
                Save the trained machine learning model to MLflow.
        
                Args:
                    model (any): The trained model.
        
                Returns:
                    None
                """

                print("Saving model")
                # TODO: save model using the correct mlflow module such as sklearn or keras.
                # sklearn example: mlflow.sklearn.log_model(model, "model")
                pass
            return save_model,


        @app.cell
        def __(
            datetime,
            evaluate_model,
            load_dataset,
            mlflow,
            prep_dataset,
            save_model,
            select_features,
            split_dataset,
            train_model,
        ):
            # TODO: Update "experiment_name_placeholder" and "path/to/data.csv"
            def run() -> None:
                """
                Run the pipeline
                """
                
                experiment_name = "experiment_name_placeholder"
        
                # Setup MLflow
                mlflow.set_tracking_uri("http://aissemble-sandbox-mlflow-tracking:5005")
                mlflow.set_experiment(experiment_name)
                
                try:
                    with mlflow.start_run() as run:
                        print(f"Starting Run. Experiment: {experiment_name}. Run ID: {run.info.run_id}")
                        start = datetime.now()
                        
                        # Load and prepare data
                        loaded_data = load_dataset("path/to/data.csv")
                        prepped_data = prep_dataset(loaded_data)
                        features = select_features(prepped_data)
                        train_data, test_data = split_dataset(prepped_data[features])
        
                        # Train and evaluate model
                        model = train_model(train_data)
                        score = evaluate_model(model, test_data)
        
                        # Save model
                        save_model(model)
        
                        end = datetime.now()
        
                        # Log mlflow tags/metrics/parameters. Update as needed
                        mlflow.set_tags(
                            {
                                "start_time": start,
                                "end_time": end,
                                "dataset_size": len(loaded_data),
                                "original_features": list(loaded_data),
                                "selected_features": features,
                                "model_type": "placeholder_model"
                            }
                        )
                        mlflow.log_metric("evaluation_score", score)
                    print("Run complete")
                except Exception as e:
                    print(f"An error occurred: {e}")
            return run,
            

        @app.cell
        def __():
            # Run the pipeline - Uncomment and run the pipeline
            # run()
            return

        if __name__ == "__main__":
            app.run()
    '''

    engineered_templates_contents[
        MODEL_INFERENCE_ENGINEERED
    ] = '''
        import marimo

        __generated_with = "0.7.12"
        app = marimo.App(width="medium")


        @app.cell(hide_code=True)
        def __():
            import marimo as mo
            return mo,


        @app.cell(hide_code=True)
        def __(mo):
            mo.md(
                r"""
                # Model Inference Engineered Pipeline
                Welcome to the Model Inference Engineered Pipeline. This notebook provides scaffolding for running inference with your trained models. By following the method signatures in the `ModelInferencePipeline` class, you can load data, load a model and run inference with minimal setup effort. This template also enables you to seamlessly transition your notebook code to be used in enterprise-level data and machine learning pipelines.
        
                ## Method Signature Overview
                Methods available in the `ModelInferencePipeline` class
                
                - `load_data`: Load a dataset
                - `load_model`: Load a trained model
                - `run_inference`: Run inference using the loaded data and model
        
                These method signatures are intended as a guide. Feel free to edit and update them as needed to fit your specific requirements. Happy coding!
                """
            )
            return


        @app.cell
        def __():
            import mlflow
            import pandas as pd
        
            # Add additional imports
            return mlflow, pd


        @app.cell
        def __(mlflow):
            class ModelInferencePipeline:
        
                def load_data(self, data_source: str) -> pd.DataFrame:
                    """
                    Args:
                        data_source (str): The source of the data (could be a file path, database connection, etc.). Default is a file path.
        
                    Returns:
                        pd.DataFrame: The loaded data.
                    """
        
                    try:
                        print("Loading data...")
                        # TODO: Implement logic to load data
                        data = pd.read_csv(data_source)
                        print(f"Data loaded successfully from {data_source}")
                    except Exception as e:
                        print(f"Failed to load data: {e}")
                        data = None
        
                    return data

                def load_model(self, model_uri: str) -> any:
                    """
                    Load a trained machine learning model.
        
                    Args:
                        model_uri (str): The URI of the trained model in MLflow.
                        Examples:
                            - From a specific run: "runs:/<run_id>/<model_name>"
                            - From the model registry: "models:/<model_name>/<model_version>"
        
                    Returns:
                        any: The loaded model.
                    """
                    
                    # Setup MLflow
                    mlflow.set_tracking_uri("http://aissemble-sandbox-mlflow-tracking:5005")
                    
                    try:
                        print("Loading model...")
                        # TODO: update specific load function if needed e.g. mlflow.sklearn.load_model(...)
                        model = mlflow.pyfunc.load_model(model_uri)
                        print(f"Model loaded successfully from {model_uri}")
                    except Exception as e:
                        print(f"Failed to load model: {e}")
                        model = None
        
                    return model

                def run_inference(self, data, model):
                    """
                    Perform inference using the loaded model and data.
        
                    Args:
                        model: The loaded model.
                        data: The prepared data for prediction, expected to be a pd.DataFrame.
        
                    Returns:
                        The prediction results.
                    """
        
                    if model is None or data is None:
                        raise ValueError("Model or data is not provided.")
                    
                    print(f"Running Model: {model}")
                    results = model.predict(data)
                    print("Inference ran successfully.")
                    
                    return results
            return ModelInferencePipeline,


        @app.cell
        def __(ModelInferencePipeline):
            # Execute Model Inference Pipeline
            # TODO: Update DATA_SOURCE and MODEL_URI and uncomment the pipeline steps
        
            DATA_SOURCE = "UPDATE_DATA_SOURCE"
            MODEL_URI = "UPDATE_MODEL_URI"
        
            # inference_pipeline = ModelInferencePipeline()
            # loaded_data = inference_pipeline.load_data(DATA_SOURCE)
            # loaded_model = inference_pipeline.load_model(MODEL_URI)
            # results = inference_pipeline.run_inference(loaded_data, loaded_model)
        
            # print("Inference Results:")
            # print(results)
            return (
                DATA_SOURCE,
                MODEL_URI,
                inference_pipeline,
                loaded_data,
                loaded_model,
                results,
            )


        if __name__ == "__main__":
            app.run()
    '''
    return


@app.cell(hide_code=True)
def __(
    DATA_PREPARATION_ENGINEERED,
    MODEL_TRAINING_ENGINEERED,
    MODEL_INFERENCE_ENGINEERED,
    engineered_templates_descriptions,
):
    ## Sandbox Wizard: Engineered Pipeline Descriptions ##

    engineered_templates_descriptions[
        DATA_PREPARATION_ENGINEERED
    ] = """
    ### Data Preparation Engineered Pipeline
    The Data Preparation Engineered Pipeline offers scaffolding for commonly used data preparation methods. This template is designed to help you transition experimental notebook code into structured methods for use in enterprise-level data pipelines. The notebook includes the following method signatures:

    - `load_data`: Load a dataset
    - `transform_data`: Apply data transformations
    - `enrich_data`: Enrich your data
    - `validate_data`: Validate your data
    """

    engineered_templates_descriptions[
        MODEL_TRAINING_ENGINEERED
    ] = """
    ### Model Training Engineered Pipeline
    The Model Training Engineered Pipeline offers scaffolding for commonly used machine learning and model training methods. This template is designed to help you transition experimental notebook code into structured methods for use in enterprise-level data and machine learning pipelines. The notebook includes the following method signatures:

    - `load_dataset`: Load a dataset
    - `prep_dataset`: Last-mile data preparation prior to model training
    - `select_features`: Select relevant features for your model
    - `split_dataset`: Split your dataset into training and testing sets
    - `train_model`: Train your machine learning model
    - `evaluate_model`: Evaluate the performance of your model
    - `save_model`: Save your trained model
    - `run`: Run the pipeline
    """

    engineered_templates_descriptions[
        MODEL_INFERENCE_ENGINEERED
    ] = """
    ### Model Inference Engineered Pipeline
    The Model Inference Engineered Pipeline provides scaffolding to quickly set up and run inference on your trained models with minimal effort. This template helps transition experimental notebook code into structured methods suitable for enterprise-level data and machine learning pipelines. The notebook includes the following method signatures in the `ModelInferencePipeline` class:

    - `load_data`: Load a dataset
    - `load_model`: Load a trained model
    - `run_inference`: Run inference using the loaded data and model
    """
    return


if __name__ == "__main__":
    app.run()
