#!/usr/bin/env python3
"""
   Copyright 2023 NetApp, Inc

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import json
import kubernetes
import os
import sys
import yaml
from tabulate import tabulate
from termcolor import colored
import requests
from urllib3 import disable_warnings


class getConfig:
    """In order to make API calls to Astra Control we need to know which Astra Control instance
    to connect to, and the credentials to make calls.  This info is found in config.yaml,
    which we search for in the following four places:
    1) The current working directory that the executed function is located in
    2) ~/.config/astra-toolkits/
    3) /etc/astra-toolkits/
    4) The directory pointed to by the shell env var ASTRATOOLKITS_CONF
    """

    def __init__(self):
        self.conf = None
        for loc in (
            os.getcwd(),
            os.path.join(os.path.expanduser("~"), ".config", "astra-toolkits"),
            "/etc/astra-toolkits",
            os.environ.get("ASTRATOOLKITS_CONF"),
        ):
            # loc could be None, which would blow up os.path.join()
            if loc:
                configFile = os.path.join(loc, "config.yaml")
            else:
                continue
            try:
                if os.path.isfile(configFile):
                    with open(configFile, "r") as f:
                        self.conf = yaml.safe_load(f)
                        break
            except IOError:
                continue
            except yaml.YAMLError:
                print(f"{configFile} not valid YAML")
                continue

        if self.conf is None:
            raise SystemExit("config.yaml not found.")

        for item in ["astra_project", "uid", "headers"]:
            try:
                assert self.conf.get(item) is not None
            except AssertionError:
                raise SystemExit(f"{item} is a required field in {configFile}")

        if "." in self.conf.get("astra_project"):
            self.domain = self.conf.get("astra_project")
        else:
            self.domain = "%s.astra.netapp.io" % (self.conf.get("astra_project"))
        self.account_id = self.conf.get("uid")
        self.base = "https://%s/accounts/%s/" % (self.domain, self.account_id)
        self.headers = self.conf.get("headers")

        if self.conf.get("verifySSL") is False:
            disable_warnings()
            self.verifySSL = False
        else:
            self.verifySSL = True

    def main(self):
        return {
            "base": self.base,
            "headers": self.headers,
            "verifySSL": self.verifySSL,
            "domain": self.domain,
            "account_id": self.account_id,
        }


class BaseCommon:
    def __init__(self):
        pass

    def printError(self, ret):
        """Function to print relevant error information when a call fails"""
        try:
            sys.stderr.write(colored(json.dumps(json.loads(ret.text), indent=2), "red") + "\n")
        except json.decoder.JSONDecodeError:
            sys.stderr.write(colored(ret.text, "red"))
        except AttributeError:
            sys.stderr.write(colored(ret, "red"))

    def recursiveGet(self, k, item):
        """Recursion function which is just a wrapper around dict.get(key), to handle cases
        where there's a dict within a dict. A '.' in the key name ('metadata.creationTimestamp')
        is used for identification purposes."""
        if len(k.split(".")) > 1:
            return self.recursiveGet(k.split(".", 1)[1], item[k.split(".")[0]])
        else:
            return item.get(k)

    def basicTable(self, tabHeader, tabKeys, dataDict):
        """Function to create a basic tabulate table for terminal printing"""
        tabData = []
        for item in dataDict["items"]:
            # Generate a table row based on the keys list
            row = [self.recursiveGet(k, item) for k in tabKeys]
            # Handle cases where table row has a nested list
            for c, r in enumerate(row):
                if type(r) is list:
                    row[c] = ", ".join(r)
            tabData.append(row)
        return tabulate(tabData, tabHeader, tablefmt="grid")


class SDKCommon(BaseCommon):
    def __init__(self):
        super().__init__()
        self.conf = getConfig().main()
        self.base = self.conf.get("base")
        self.headers = self.conf.get("headers")
        self.verifySSL = self.conf.get("verifySSL")

    def apicall(self, method, url, data, headers, params, verify, quiet=False, verbose=False):
        """Make a call using the requests module.
        method can be get, put, post, patch, or delete"""
        try:
            r = getattr(requests, method)
        except AttributeError as e:
            raise SystemExit(e)
        try:
            if verbose:
                self.printVerbose(url, method, headers, data, params)
            ret = r(url, json=data, headers=headers, params=params, verify=verify)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        if not ret.ok:
            # GET clouds has more response information than other calls, so if
            # there's an error make a second API call to improve error messaging
            if (
                url.split("/")[-1] != "clouds"
                or (url.split("/")[-1] == "clouds" and method != "get")
                or (url.split("/")[-1] == "clouds" and quiet is True)
            ):
                self.apicall(
                    "get",
                    self.base + "topology/v1/clouds",
                    {},
                    self.headers,
                    {},
                    self.verifySSL,
                    quiet=False,
                    verbose=False,
                )
            elif ret.status_code >= 400 and ret.status_code < 500:
                if "x-pcloud-accountid" in ret.text:
                    print(
                        "API call to Astra Control failed: "
                        + colored("check uid in config.json", "red")
                    )
                elif ret.status_code == 401:
                    print(
                        "API call to Astra Control failed: "
                        + colored("check Authorization in config.json", "red")
                    )
                else:
                    print(
                        "API call to Astra Control failed: "
                        + colored(f"{ret.status_code} - {ret.reason}", "red")
                    )
                    if ret.text.strip():
                        print(f"text: {ret.text.strip()}")
            else:
                print("API call to Astra Control failed (Internal Server Error)")
                print(f"API HTTP Status Code: {ret.status_code} - {ret.reason}")
                if ret.text.strip():
                    print(f"text: {ret.text}")
        if verbose:
            print(f"API HTTP Status Code: {ret.status_code}")
        return ret

    def jsonifyResults(self, requestsObject):
        try:
            results = requestsObject.json()
        except ValueError as e:
            print(f"response contained invalid JSON: {e}")
            results = None
        return results

    def printVerbose(self, url, method, headers, data, params):
        """Function to print API call details when in verbose mode"""
        print(colored(f"API URL: {url}", "green"))
        print(colored(f"API Method: {method}", "green"))
        print(colored(f"API Headers: {headers}", "green"))
        print(colored(f"API data: {data}", "green"))
        print(colored(f"API params: {params}", "green"))


class KubeCommon(BaseCommon):
    def __init__(self, config_context=None):
        super().__init__()

        # First try loading from incluster (a local pod)
        try:
            self.api_client = kubernetes.client.ApiClient(
                configuration=kubernetes.config.load_incluster_config()
            )

        # If that fails, then it's a "normal" kubeconfig+context environment
        except kubernetes.config.config_exception.ConfigException as err:
            # Setup the config_file and context based on the config_context input
            config_file, context = None, None
            if config_context and ":" in config_context:
                config_file, context = tuple(config_context.split(":"))
                config_file = None if config_file == "None" else config_file
            elif config_context:
                config_file = config_context
            try:
                # Create the api_client
                self.api_client = kubernetes.config.new_client_from_config(
                    config_file=config_file, context=context
                )
            except kubernetes.config.config_exception.ConfigException:
                self.printError(f"{err}\n")
                self.printError(
                    f"Please ensure '{config_file}:{context}' is the correct 'config_file:context'"
                    " mapping, and you have network connectivity to the cluster.\n"
                )
                raise SystemExit()

        # Catch other errors (like malformed files), print error message, and exit
        except Exception as err:
            self.printError(
                "Error loading kubeconfig, please check kubeconfig file to ensure it is valid\n"
            )
            self.printError(f"{err}\n")
            raise SystemExit()
