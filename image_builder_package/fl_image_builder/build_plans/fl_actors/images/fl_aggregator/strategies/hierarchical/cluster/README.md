# Main Idea

Due to the current limitations of Flower (no native support for hierarchical FL)
We need to create a custom workaround.

The idea is to see the Cluster Aggregator (CAg) as a hybrid between a learner and an aggregator.

The learner parts will be used to link and communicate with the Root Aggregator (RAg).
The learners parts include training, evaluation, etc.

When the RAg requests the CAg to train - the CAg will in turn start a classic FL training loop
with the learners in its cluster.

Once this training loop finalizes, the CAg will aggregate its cluster wide result
and send it to the RAg.

Thus the RAg will treat the CAg as any other classic FL learner (black box).
