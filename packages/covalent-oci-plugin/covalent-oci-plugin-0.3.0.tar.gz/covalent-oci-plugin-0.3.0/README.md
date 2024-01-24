&nbsp;

<div align="center">

<img src="./assets/readme-banner.png" width=150%>

</div>

## Covalent OCI Plugin

[Covalent](https://docs.covalent.xyz/docs/) is a Pythonic workflow tool used to execute tasks on advanced computing hardware.

This executor plugin interfaces Covalent with [Oracle Cloud Infrastructure (OCI)](https://www.oracle.com/ca-en/cloud/). Valid [OCI credentials](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/apisigningkey.htm) are therefore required for use.

## 1. Installation

> :warning: If you are just getting started with Covalent, check out the [quickstart](https://docs.covalent.xyz/docs/get-started/quick-start). We recommend using a virtual environment such as `venv` or `conda` to minimize dependency conflicts.

To use this plugin with Covalent, install it using `pip`:

```sh
pip install covalent covalent-oci-plugin
```

## 2. Usage Example

The small workflow below demonstrates task execution with the OCI Executor.

In the example, we train a Support Vector Machine (SVM) and use an instance of the executor to execute the `train_svm` electron on an OCI compute instance. Note that we also use [pip dependencies](https://docs.covalent.xyz/docs/user-documentation/api-reference/taskhelpers/#class-covalentdepspippackages-reqs_path--) which will pre-install packages required to execute the electrons.

> :warning: Ensure the Covalent server is started before using this script by running `covalent start` on the command line.

```python
import covalent as ct
from numpy.random import permutation
from sklearn import svm, datasets

deps_pip = ["numpy==1.22.4", "scikit-learn==1.1.2"]

executor = ct.executor.OCIExecutor(
    availability_domain="giLp:US-ASHBURN-AD-1",
    shape="VM.Standard.E2.1",
    compartment_id="ocid1.compartment.oc1..unique-id",
    image_id="ocid1.image.oc1.iad.unique-id",
    subnet_id="ocid1.subnet.oc1.iad.unique-id",
    # ssh_key_file="~/.oci/id_rsa",
)

# Use executor plugin to train our SVM model
@ct.electron(
    executor=executor,
    deps_pip=deps_pip
)
def train_svm(data, C, gamma):
    X, y = data
    clf = svm.SVC(C=C, gamma=gamma)
    clf.fit(X[90:], y[90:])
    return clf

# When no executor is attached, the task runs locally
@ct.electron
def load_data():
    iris = datasets.load_iris()
    perm = permutation(iris.target.size)
    iris.data = iris.data[perm]
    iris.target = iris.target[perm]
    return iris.data, iris.target

@ct.electron
def score_svm(data, clf):
    X_test, y_test = data
    return clf.score(
    	X_test[:90],y_test[:90]
    )

@ct.lattice
def run_experiment(C=1.0, gamma=0.7):
    data = load_data()
    clf = train_svm(
    	data=data,
	    C=C,
	    gamma=gamma
    )
    score = score_svm(
    	data=data,
	    clf=clf
    )
    return score

# Dispatch the workflow.
dispatch_id = ct.dispatch(run_experiment)(
    C=1.0,
    gamma=0.7
)

# Wait for our result and get result value
result = ct.get_result(dispatch_id, wait=True).result

print(result)
```
During the execution of the workflow, one can navigate to the UI to see the status of the workflow. Once completed, the above script should also output a value with the score of our model.

```sh
0.8666666666666667
```

Note that some cloud infrastructure must already exists to run the above workflow, as noted in [Required OCI Resources](#4-required-oci-resources).

## 3. Configuration

There are many configuration options that can be passed in to the class `ct.executor.OCIExecutor` or by modifying the [covalent config file](https://docs.covalent.xyz/docs/user-documentation/how-to/customization) under the section `[executors.oci]`.

For more information about all of the possible configuration values visit our [documentation page](https://docs.covalent.xyz/docs/user-documentation/api-reference/executors/oci/#overview-of-configuration) for this plugin.

## 4. Required OCI Resources

The required OCI resources must first be provisioned before using this plugin:

1. Virtual cloud network (VCN)
2. Internet gateway
3. Route table
4. Public subnet
5. SSH key
6. API signing key

Covalent's [resource deployment](https://docs.covalent.xyz/docs/features/resourceDeployment) feature is very convenient for auto-creating these resources:

```bash
covalent deploy up oci --compartment_ocid=<your-compartment-ocid>
```

For this plugin the compartment ocid is a required parameter. This can be found and chosen from in the [OCI console](https://cloud.oracle.com/identity/compartments).

For more information, see our [documentation page](https://docs.covalent.xyz/docs/user-documentation/api-reference/executors/oci/#required-cloud-resources) for this plugin.

## Getting Started with Covalent

For more information on how to get started with Covalent, check out the project [homepage](https://github.com/AgnostiqHQ/covalent) and the official [documentation](https://docs.covalent.xyz/docs).

## Release Notes

Release notes are available in the [Changelog](https://github.com/AgnostiqHQ/covalent-oci-plugin/blob/develop/CHANGELOG.md).

## Citation

Please use the following citation in any publications:

> https://doi.org/10.5281/zenodo.5903364

## License

Covalent is licensed under the Apache License 2.0. See the [LICENSE](https://github.com/AgnostiqHQ/covalent-oci-plugin/blob/develop/LICENSE) file or contact the [support team](mailto:support@agnostiq.ai) for more details.
