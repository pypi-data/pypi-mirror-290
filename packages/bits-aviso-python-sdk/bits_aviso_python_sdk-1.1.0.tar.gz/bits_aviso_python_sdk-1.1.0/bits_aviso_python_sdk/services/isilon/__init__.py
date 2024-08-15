import base64
import logging
import requests


class Isilon:
    """Class to interact with the Isilon PowerScale API."""

    def __init__(self, username, password, clusters, platform_api_version='15'):
        """Initializes the Isilon class.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.
            clusters (dict, optional): A dictionary containing the cluster name as key and IP as value.
            platform_api_version (str, optional): The version of the Isilon API to use. Defaults to '15'.
        """
        self.clusters = clusters
        self.headers = {'Authorization': f'Basic {self._encode_credentials(username, password)}'}
        self.platform_api_version = platform_api_version

    @staticmethod
    def _encode_credentials(username,  password):
        """Encodes the username and password for use in the API.

        Args:
            username (str): The username to authenticate with.
            password (str): The password to authenticate with.

        Returns:
            str: The encoded credentials.
        """
        return base64.b64encode(f'{username}:{password}'.encode()).decode()

    def build_url(self, cluster_ip, api_endpoint=None):
        """Builds the URL for the given Isilon cluster with no trailing slash. If an API endpoint is provided,
        it will be appended to the URL.

        Args:
            cluster_ip (str): The cluster ip.
            api_endpoint (str, optional): The path to the API endpoint. Defaults to None.

        Returns:
            str: The URL for the Isilon API.
        """
        if api_endpoint:  # check if an API endpoint is provided
            if api_endpoint.startswith('/'):  # check for a leading slash
                return f'https://{cluster_ip}:8080/platform/{self.platform_api_version}{api_endpoint}'
            else:
                return f'https://{cluster_ip}:8080/platform/{self.platform_api_version}/{api_endpoint}'

        else:
            return f'https://{cluster_ip}:8080/platform/{self.platform_api_version}'

    def get_all_quotas(self, clusters=None):
        """Gets the quotas for all clusters.

        Args:
            clusters (dict, optional): A dictionary containing the cluster name as key and IP as value.
                Defaults to None.

        Returns:
            list[dict], dict: The quotas for all clusters and error payload if any.
        """
        # if no clusters are provided, use the clusters from the class
        if not clusters:
            clusters = self.clusters

        all_quotas = []
        error_payload = {}
        for name, ip in clusters.items():  # get the name and ip of each cluster
            cluster_quota, error_payload = self.get_quota_for_cluster(name, ip)
            if cluster_quota:
                all_quotas.extend(cluster_quota)

            elif error_payload:
                error_payload.update(cluster_quota)

            else:
                error_payload['Error'] = f'Failed to get quota data for the cluster {name} with the IP {ip}.'

        return all_quotas, error_payload

    def get_all_network_pools(self, clusters=None):
        """Gets the network pools for all clusters.

        Args:
            clusters (dict, optional): A dictionary containing the cluster name as key and IP as value.
                Defaults to None.

        Returns:
            list[dict], dict: The network pools for all clusters and error payload if any.
        """
        # if no clusters are provided, use the clusters from the class
        if not clusters:
            clusters = self.clusters

        all_network_pools = []
        error_payload = {}
        for name, ip in clusters.items():
            cluster_network_pools, error_payload = self.get_network_pool_for_cluster(name, ip)
            if cluster_network_pools:
                all_network_pools.extend(cluster_network_pools)

            elif error_payload:
                error_payload.update(cluster_network_pools)

            else:
                error_payload['Error'] = f'Failed to get network pool data for the cluster {name} with the IP {ip}.'

        return all_network_pools, error_payload
    
    def get_quota_for_cluster(self, cluster_name, cluster_ip):
        """Gets the quotas for the given cluster.

        Args:
            cluster_name (str): The cluster's name.
            cluster_ip (str): The cluster's ip address.

        Returns:
            list[dict], dict: The quota data for the cluster and error payload if any.
        """
        # build the url
        url = self.build_url(cluster_ip, '/quota/quotas')
        quotas = []
        try:  # get the quota data
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            quota_data = response.json().get('quotas', {})
            if not quota_data:
                raise ValueError(f'No quotas found for {cluster_name}. IP: {cluster_ip}')

            # add the cluster name to the data
            for quota in quota_data:
                quota['cluster'] = cluster_name
                quotas.append(quota)

            # return the quota data
            return quotas, {}

        except (requests.exceptions.RequestException, ValueError) as e:
            err_msg = f'Failed to get quota for {cluster_name}. IP: {cluster_ip}\nException Message: {e}'
            logging.error(err_msg)
            return [], {"Error": err_msg}

    def get_network_pool_for_cluster(self, cluster_name, cluster_ip):
        """Gets the network pools for the given cluster.

        Args:
            cluster_name (str): The cluster's name.
            cluster_ip (str): The cluster's ip address.

        Returns:
            list[dict], dict: The network pool data for the cluster and error payload if any.
        """
        # build the url
        url = self.build_url(cluster_ip, '/network/pools')
        network_pools = []
        try:  # get the network pool data
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            network_pool_data = response.json().get('pools', {})
            if not network_pool_data:
                raise ValueError(f'No network pools found for {cluster_name}. IP: {cluster_ip}')

            # add the cluster name to the data
            for np in network_pool_data:
                np['cluster'] = cluster_name
                network_pools.append(np)

            # return the network pool data
            return network_pools, {}

        except (requests.exceptions.RequestException, ValueError) as e:
            err_msg = f'Failed to get network pools for {cluster_name}. IP: {cluster_ip}\nException Message: {e}'
            logging.error(err_msg)
            return [], {"Error": err_msg}

