## Annotations about Apache Airflow 
---
### Concepts and Resources

#### DAG ( Direct Acyclic Graph )
It's the workflow, a collection of all the tasks that want execute, 
organized in a way that reflects their relationships and dependencies.

#### Default Parameters, Context Manager e Operators
- **Default parameters:** are parameter shared with all tasks on a DAG
- **Context Manager:** controls the workflow, manages the execution states, if there was an error or success and which way to go based on that
- **Operators:** It's a worker, the task itself, operators runs the task, example is a BashOperator for run a bash job.

#### Hooks
 They are communication interfaces with callbacks for integration with external platforms like Hive, S3 and MySQL. We can monitor this type of task using ** SLA ** to set the response time limit before considering a request failure as an example.
  
#### Pools
 These are resource limitators. We can create a pool to determine CPU usage, execution time or I/O limit, and other things.

#### Connections
 Connections are used when they need access to external resources such as databases, apis an so on. These connections can be shared and used from any task in a DAG.
 
#### Xcoms, Variables and Branching
- **Xcoms:** The name "Xcom" is an abbreviation for "cross-communication". This resource allows communication between tasks, shared metadata, parameters, variables and so on. They are defined by key/value and timestamp.
- **Variables:** Typically used to save configuration data, such as paths and any other settings. these variables use key / value to store your data 
- **Branching:** Used to define which paths to follow, a branching  can initiate the execution of one or more tasks through some condition or not

#### SubDAGs and SLA (Service level agreement)
- **SubDAGs:** These are common workflows that can be called from any task in any DAG. It’s a way to reuse a common workflow.
- **SLA:** This resource is used to set a cronogram for a task, run time, start time, end time and so on.

#### Tigger Rules and Last Execution Only
- **Trigger:** All operators have a trigger_rule argument to define which rule must be followed for a next task to start.
- **Last Execution Only:** This feature is used when you don't need an orchestration, where only a simple task needs to be executing. In this case, "Last Exection Only" is better because we save CPU cycles and memory

#### Zombies/Undeads, Cluster Policies, Jinja Templating and Packaged DAGs
- **Zombies/Undeads:** This feature is used in Airflow to check if a task is stagnant; if so, it ends the task.
- **CLuster Policies:** It's a group where you define own policies such as access restrictions and so on.
- **Jinja Templating:** Jinja Templating is a Python feature that allows dynamic scripts, such as scriptlet in java, which we can also combine with macros
- **Packaged DAGs:** Used from combine some DAGs in a zip

#### Backfill
 It's great when you need to change the business logic of the existing DAG and need to update the historical data

### Operators
While Dag describe how executing a workflow, operators determine waht really should be performed.
#### Commons Operators
- **BashOperator:** executing a command bash
- **PythonOperator:** call a Python function
- **EmailOperator:** send a e-mail
- **SimpleHttpOperator:** send HTTP request
- **MySQLOperator, JDBCOperator,PostgresOperator, MsSqlOperator, OracleOperator, etc.** Execute SQL command.
- **Sensor:** Used to determine a waiting time to validate the progress of a given task.

> For more operators, access https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/operators/index.html


## How to Setup Airflow Multi-Node Cluster with Celery & RabbitMQ
---

For using more than one work node from Airflow, we should set up the executor in airflow.cfg to use CeleryExecutor and all node must have installed the Airflow.

* https://towardsdatascience.com/scale-your-data-pipelines-with-airflow-and-kubernetes-4d34b0af045
* https://medium.com/bluecore-engineering/were-all-using-airflow-wrong-and-how-to-fix-it-a56f14cb0753
* http://airflow.apache.org/docs/apache-airflow/stable/executor/celery.html?highlight=celery
* https://medium.com/@khatri_chetan/how-to-setup-airflow-multi-node-cluster-with-celery-rabbitmq-cfde7756bb6a




