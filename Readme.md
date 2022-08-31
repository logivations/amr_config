Configuration Manager


**Why do we need a configuration manager?**

Each AMR has a unique set of configuration. So how can we keep track of each unique set of configuration?

The most straightforward solution is to have a repository containing all the configuration files and
have a version control branch for every AMR.

While this might be a good solution for a one-time setup, maintaining it will be very high effort and error-prone.

Maintaining the configuration means being able to easily do bulk actions (Add/remove/modify) e.g for all AMRs at a specific customer. With this approach, we would need to individually update every branch of every AMR concerned.


**Our Approach**

We propose a better approach.

We notice that the AMR configuration depends on attributes which are common across multiple sets of AMR. A given AMR has:

- ID
- Customer
- Simulation mode (real/gazebo/simple)

We can even extend on that, in the future we might additionally have different HW versions and other attributes.

Each one of these attributes will dictate one or more configuration parameters, some examples:

- ID: steering angle offset, camera calibration...
- customer: maximum speeds...
- simulation mode: open loop control...
- HW version: fork maximum height...

Bundling up configurations like this allows us to say:

"All AMRs that are at customer X should have this configuration of maximum speeds"
"All AMRs in simple simulation should have the open loop control configuration to True"

Now the question is how to technically achieve that


**Hierarchical Overriding Yaml Configuration**

Basically, we want a Default configuration that is overriden by attribute-specific configurations:

Example:

INPUTS

defaults.yaml:

    controller_server:
        ros_parameters:
            max_speed: 0.4
    tricycle_controller
        ros__parameters:
            open_loop: false


customer.yaml:

    controller_server:
        ros_parameters:
            max_speed: 0.1


simulation_mode.yaml:

    tricycle_controller
        ros__parameters:
            open_loop: true


OUTPUT:

active_config.yaml:

    controller_server:
        ros_parameters:
            max_speed: 0.1
    tricycle_controller
        ros__parameters:
            open_loop: true


So the first step of the solution is a program that takes for input a default YAML file and several overriding YAML files and outputs
one overriden YAML file

The second step of the solution is to version control the overriding YAML files. In this case customer.yaml is config for a specific customer and simulation_mode.yaml is the config for the simple simulation.

Since each attribute needs multiple branches, each attribute needs to be a repository. Since it is insisde the amr_config repository, we make use of git submodules. Example: customer submodule has branches Brummer, Liebherr. simulation_mode submodule has branches gazebo, real_amr, simple_simulation. etc...


**Maintenance example scenarios**

Scenario: First time setup of AMR at Brummer
Actions: in customer submodule checkout Brummer branch, create new branch in AMR/instance submodule and attribute-specific configuration

Scenario: Brummer asks us to limit the speeds of all their AMRs
Actions: Change the max_speed of the Brummer branch in the customer submodule, pull the submodule on each AMR and restart its bringup

Scenario: We add a new node on master that requires configuration 
Actions: Add the configuration to the defaults.yaml and if needed, to the attribute-specific


**Open Points**

How to keep release versions?

Same parameter is different levels? What's the hirearchy?