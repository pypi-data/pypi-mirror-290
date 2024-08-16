"""Constants used in the APX provisioner."""

# Tag uniquely identifying all nodes of a cluster
TAG_RAY_CLUSTER_NAME = 'ray-cluster-name'
TAG_APXDEPLOY_CLUSTER_NAME = 'apxdeploy-cluster-name'
# Legacy tag for backward compatibility to distinguish head and worker nodes.
TAG_RAY_NODE_KIND = 'ray-node-type'
TAG_APXDEPLOY_HEAD_NODE = 'apxdeploy-head-node'

HEAD_NODE_TAGS = {
    TAG_RAY_NODE_KIND: 'head',
    TAG_APXDEPLOY_HEAD_NODE: '1',
}

WORKER_NODE_TAGS = {
    TAG_RAY_NODE_KIND: 'worker',
    TAG_APXDEPLOY_HEAD_NODE: '0',
}
