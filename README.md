# mongo-backup-for-shard-cluster
Backup mongodb data with mongodump from sharded cluster.
It connects to _mongos_, gets shards list and then read data from one of the secondary replica in each shard so that primary is not affected.

## Requirements
* python2
* pymongo
* mongo cli
* mongodump cli


## Instructions for use
 
Utility should be installed and run from the instance, which has access to _mongos_ and to all secondaries replicas in sharded replicasets

Use _mongos_backup.conf_ for configure utility (see <mongos_backup.conf>)

Run <mongos_backup_from_secondary.py>

Example:
```
(mongo) [cloud-user@ip-172-18-31-181 backup]$ python2 -d ./mongos_backup_from_secondary.py
mongo_bin_dir is: /usr/bin
backup_dir is: /home/cloud-user/backup/devqa-full
mongos_addr is: ourdb-sharded-mongo-01001.internal.lan
mongos_port is: 27017
config_addr is: ourdb-sharded-mongo-01001.internal.lan
config_port is: 27019

get shard info successfully!
balancer is stopped!
Shards info:
[{'host': u'ourdb-sharded-mongo-01001.internal.lan:27018,ourdb-sharded-mongo-01002.internal.lan:27018,ourdb-sharded-mongo-01003.internal.lan:27018', 'name': u'devqa_athena_shard01'}, {'host': u'ourdb-sharded-mongo-02001.internal.lan:27018,ourdb-sharded-mongo-02002.internal.lan:27018', 'name': u'devqa_athena_shard02'}, {'host': u'ourdb-sharded-mongo-03001.internal.lan:27018,ourdb-sharded-mongo-03002.internal.lan:27018,ourdb-sharded-mongo-03003.internal.lan:27018', 'name': u'devqa_athena_shard03'}]
ourdb-sharded-mongo-01001.internal.lan:27018,ourdb-sharded-mongo-01002.internal.lan:27018,ourdb-sharded-mongo-01003.internal.lan:27018:getting secondaries ...
cmd_forbid_write:/usr/bin/mongo --username admin --password MySecretPassword ourdb-sharded-mongo-01001.internal.lan:27018/admin  --quiet  --eval 'rs.slaveOk();db.fsyncLock();db.currentOp();' | grep 'fsyncLock\>' | grep true
	"fsyncLock" : true,
ourdb-sharded-mongo-02001.internal.lan:27018,ourdb-sharded-mongo-02002.internal.lan:27018:getting secondaries ...
cmd_forbid_write:/usr/bin/mongo --username admin --password MySecretPassword ourdb-sharded-mongo-02002.internal.lan:27018/admin  --quiet  --eval 'rs.slaveOk();db.fsyncLock();db.currentOp();' | grep 'fsyncLock\>' | grep true
	"fsyncLock" : true,
ourdb-sharded-mongo-03001.internal.lan:27018,ourdb-sharded-mongo-03002.internal.lan:27018,ourdb-sharded-mongo-03003.internal.lan:27018:getting secondaries ...
cmd_forbid_write:/usr/bin/mongo --username admin --password MySecretPassword ourdb-sharded-mongo-03001.internal.lan:27018/admin  --quiet  --eval 'rs.slaveOk();db.fsyncLock();db.currentOp();' | grep 'fsyncLock\>' | grep true
	"fsyncLock" : true,
now, ready for backup!
cmd_line: /usr/bin/mongodump --username admin --password MySecretPassword --host ourdb-sharded-mongo-01001.internal.lan --port 27019 --oplog --out /home/cloud-user/backup/devqa-full/2023-01-16
2023-01-16T16:31:25.797+0000	writing admin.system.users to /home/cloud-user/backup/devqa-full/2023-01-16/admin/system.users.bson
2023-01-16T16:31:25.798+0000	done dumping admin.system.users (13 documents)
2023-01-16T16:31:25.798+0000	writing admin.system.version to /home/cloud-user/backup/devqa-full/2023-01-16/admin/system.version.bson
2023-01-16T16:31:25.799+0000	done dumping admin.system.version (2 documents)
2023-01-16T16:31:25.801+0000	writing config.changelog to /home/cloud-user/backup/devqa-full/2023-01-16/config/changelog.bson
2023-01-16T16:31:25.810+0000	writing config.actionlog to /home/cloud-user/backup/devqa-full/2023-01-16/config/actionlog.bson
2023-01-16T16:31:25.814+0000	done dumping config.actionlog (1106 documents)
2023-01-16T16:31:25.814+0000	writing config.locks to /home/cloud-user/backup/devqa-full/2023-01-16/config/locks.bson
2023-01-16T16:31:25.816+0000	done dumping config.locks (52 documents)
2023-01-16T16:31:25.817+0000	writing config.collections to /home/cloud-user/backup/devqa-full/2023-01-16/config/collections.bson
2023-01-16T16:31:25.817+0000	writing config.chunks to /home/cloud-user/backup/devqa-full/2023-01-16/config/chunks.bson
2023-01-16T16:31:25.818+0000	done dumping config.collections (35 documents)
2023-01-16T16:31:25.819+0000	writing config.databases to /home/cloud-user/backup/devqa-full/2023-01-16/config/databases.bson
2023-01-16T16:31:25.820+0000	writing config.lockpings to /home/cloud-user/backup/devqa-full/2023-01-16/config/lockpings.bson
2023-01-16T16:31:25.820+0000	done dumping config.databases (4 documents)
2023-01-16T16:31:25.821+0000	writing config.mongos to /home/cloud-user/backup/devqa-full/2023-01-16/config/mongos.bson
2023-01-16T16:31:25.821+0000	done dumping config.lockpings (62 documents)
2023-01-16T16:31:25.822+0000	writing config.shards to /home/cloud-user/backup/devqa-full/2023-01-16/config/shards.bson
2023-01-16T16:31:25.823+0000	done dumping config.mongos (3 documents)
2023-01-16T16:31:25.823+0000	done dumping config.shards (3 documents)
2023-01-16T16:31:25.823+0000	writing config.settings to /home/cloud-user/backup/devqa-full/2023-01-16/config/settings.bson
2023-01-16T16:31:25.824+0000	writing config.version to /home/cloud-user/backup/devqa-full/2023-01-16/config/version.bson
2023-01-16T16:31:25.824+0000	done dumping config.settings (2 documents)
2023-01-16T16:31:25.825+0000	writing config.migrations to /home/cloud-user/backup/devqa-full/2023-01-16/config/migrations.bson
2023-01-16T16:31:25.825+0000	done dumping config.version (1 document)
2023-01-16T16:31:25.825+0000	writing config.tags to /home/cloud-user/backup/devqa-full/2023-01-16/config/tags.bson
2023-01-16T16:31:25.827+0000	done dumping config.migrations (0 documents)
2023-01-16T16:31:25.828+0000	writing config.image_collection to /home/cloud-user/backup/devqa-full/2023-01-16/config/image_collection.bson
2023-01-16T16:31:25.828+0000	done dumping config.tags (0 documents)
2023-01-16T16:31:25.828+0000	writing admin.distribution_history to /home/cloud-user/backup/devqa-full/2023-01-16/admin/distribution_history.bson
2023-01-16T16:31:25.829+0000	done dumping config.image_collection (0 documents)
2023-01-16T16:31:25.829+0000	done dumping admin.distribution_history (0 documents)
2023-01-16T16:31:25.833+0000	done dumping config.chunks (5859 documents)
2023-01-16T16:31:25.844+0000	done dumping config.changelog (13138 documents)
2023-01-16T16:31:25.845+0000	writing captured oplog to
2023-01-16T16:31:25.846+0000		dumped 1 oplog entry
finished backup config ourdb-sharded-mongo-01001.internal.lan:27019.
cmd_dump: /usr/bin/mongodump --username admin --password MySecretPassword --host ourdb-sharded-mongo-01001.internal.lan:27018 --oplog --out /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01
2023-01-16T16:31:25.919+0000	writing admin.system.users to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/admin/system.users.bson
2023-01-16T16:31:25.920+0000	done dumping admin.system.users (6 documents)
2023-01-16T16:31:25.920+0000	writing admin.system.version to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/admin/system.version.bson
2023-01-16T16:31:25.921+0000	done dumping admin.system.version (5 documents)
2023-01-16T16:31:25.923+0000	writing athena_cs_qa.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_qa/video_distribution_data.bson
2023-01-16T16:31:25.943+0000	writing athena.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena/video_distribution_data.bson
2023-01-16T16:31:25.945+0000	writing athena_qa.distribution_history to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_qa/distribution_history.bson
2023-01-16T16:31:25.945+0000	writing athena.distribution_history to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena/distribution_history.bson
2023-01-16T16:31:26.677+0000	done dumping athena.video_distribution_data (126984 documents)
2023-01-16T16:31:26.678+0000	writing athena_cs_qa.airing_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_qa/airing_data.bson
2023-01-16T16:31:27.017+0000	done dumping athena_cs_qa.airing_data (108942 documents)
2023-01-16T16:31:27.018+0000	writing athena_qa.airing_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_qa/airing_data.bson
2023-01-16T16:31:27.380+0000	done dumping athena_qa.airing_data (106821 documents)
2023-01-16T16:31:27.381+0000	writing athena_cs_qa.distributable_content to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_qa/distributable_content.bson
2023-01-16T16:31:31.955+0000	done dumping athena_qa.distribution_history (508836 documents)
2023-01-16T16:31:31.956+0000	writing athena.distributable_content to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena/distributable_content.bson
2023-01-16T16:31:33.154+0000	done dumping athena.distribution_history (488669 documents)
2023-01-16T16:31:33.154+0000	writing athena_qa.distributable_content to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_qa/distributable_content.bson
2023-01-16T16:31:33.981+0000	done dumping athena.distributable_content (34927 documents)
2023-01-16T16:31:33.982+0000	writing athena_qa.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_qa/video_distribution_data.bson
2023-01-16T16:31:34.781+0000	done dumping athena_qa.video_distribution_data (31633 documents)
2023-01-16T16:31:34.781+0000	writing athena_cs_dev.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_dev/video_distribution_data.bson
2023-01-16T16:31:34.834+0000	done dumping athena_qa.distributable_content (33466 documents)
2023-01-16T16:31:34.835+0000	writing athena_qa.single_asset_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_qa/single_asset_distribution_data.bson
2023-01-16T16:31:34.862+0000	[#################.......]  athena_cs_dev.video_distribution_data  21435/29889  (71.7%)
2023-01-16T16:31:34.874+0000	[########################]  athena_cs_dev.video_distribution_data  29889/29889  (100.0%)
2023-01-16T16:31:35.112+0000	done dumping athena_qa.single_asset_distribution_data (7854 documents)
2023-01-16T16:31:35.112+0000	writing athena_cs_dev.single_asset_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_dev/single_asset_distribution_data.bson
2023-01-16T16:31:35.259+0000	done dumping athena_cs_dev.video_distribution_data (29889 documents)
2023-01-16T16:31:35.260+0000	writing athena.single_asset_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena/single_asset_distribution_data.bson
2023-01-16T16:31:35.285+0000	done dumping athena_cs_dev.single_asset_distribution_data (7852 documents)
2023-01-16T16:31:35.285+0000	writing config.cache.chunks.athena.build_job to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena.build_job.bson
2023-01-16T16:31:35.412+0000	done dumping config.cache.chunks.athena.build_job (4339 documents)
2023-01-16T16:31:35.413+0000	writing config.cache.chunks.config.system.sessions to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.config.system.sessions.bson
2023-01-16T16:31:35.416+0000	done dumping config.cache.chunks.config.system.sessions (1024 documents)
2023-01-16T16:31:35.417+0000	writing config.cache.chunks.athena_qa.build_job to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_qa.build_job.bson
2023-01-16T16:31:35.418+0000	done dumping config.cache.chunks.athena_qa.build_job (145 documents)
2023-01-16T16:31:35.419+0000	writing athena_cs_dev.affiliate to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_dev/affiliate.bson
2023-01-16T16:31:35.435+0000	done dumping athena_cs_dev.affiliate (106 documents)
2023-01-16T16:31:35.436+0000	writing config.cache.chunks.athena.distribution_history to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena.distribution_history.bson
2023-01-16T16:31:35.437+0000	done dumping config.cache.chunks.athena.distribution_history (67 documents)
2023-01-16T16:31:35.437+0000	writing config.cache.chunks.athena_cs_qa.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_qa.video_distribution_data.bson
2023-01-16T16:31:35.438+0000	done dumping config.cache.chunks.athena_cs_qa.video_distribution_data (47 documents)
2023-01-16T16:31:35.438+0000	writing config.cache.chunks.athena_qa.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_qa.video_distribution_data.bson
2023-01-16T16:31:35.439+0000	done dumping config.cache.chunks.athena_qa.video_distribution_data (42 documents)
2023-01-16T16:31:35.439+0000	writing config.cache.chunks.athena_cs_qa.distributable_content to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_qa.distributable_content.bson
2023-01-16T16:31:35.440+0000	done dumping config.cache.chunks.athena_cs_qa.distributable_content (39 documents)
2023-01-16T16:31:35.440+0000	writing config.cache.chunks.athena_qa.distributable_content to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_qa.distributable_content.bson
2023-01-16T16:31:35.452+0000	done dumping config.cache.chunks.athena_qa.distributable_content (35 documents)
2023-01-16T16:31:35.452+0000	writing config.cache.chunks.athena_qa.distribution_history to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_qa.distribution_history.bson
2023-01-16T16:31:35.453+0000	done dumping config.cache.chunks.athena_qa.distribution_history (33 documents)
2023-01-16T16:31:35.453+0000	writing config.cache.collections to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.collections.bson
2023-01-16T16:31:35.454+0000	done dumping config.cache.collections (25 documents)
2023-01-16T16:31:35.454+0000	writing config.cache.chunks.athena.distributable_content to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena.distributable_content.bson
2023-01-16T16:31:35.455+0000	done dumping config.cache.chunks.athena.distributable_content (19 documents)
2023-01-16T16:31:35.455+0000	writing config.cache.chunks.athena_cs_qa.affiliate to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_qa.affiliate.bson
2023-01-16T16:31:35.515+0000	done dumping config.cache.chunks.athena_cs_qa.affiliate (6 documents)
2023-01-16T16:31:35.515+0000	writing config.cache.chunks.athena_cs_dev.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_dev.video_distribution_data.bson
2023-01-16T16:31:35.516+0000	done dumping config.cache.chunks.athena_cs_dev.video_distribution_data (6 documents)
2023-01-16T16:31:35.517+0000	writing config.cache.chunks.athena_cs_dev.affiliate to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_dev.affiliate.bson
2023-01-16T16:31:35.517+0000	done dumping config.cache.chunks.athena_cs_dev.affiliate (6 documents)
2023-01-16T16:31:35.518+0000	writing config.cache.chunks.athena_cs_qa.build_job to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_qa.build_job.bson
2023-01-16T16:31:35.518+0000	done dumping config.cache.chunks.athena_cs_qa.build_job (6 documents)
2023-01-16T16:31:35.519+0000	writing config.cache.chunks.athena_cs_dev.single_asset_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_dev.single_asset_distribution_data.bson
2023-01-16T16:31:35.519+0000	done dumping config.cache.chunks.athena_cs_dev.single_asset_distribution_data (6 documents)
2023-01-16T16:31:35.520+0000	writing config.cache.chunks.athena_qa.single_asset_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_qa.single_asset_distribution_data.bson
2023-01-16T16:31:35.520+0000	done dumping config.cache.chunks.athena_qa.single_asset_distribution_data (6 documents)
2023-01-16T16:31:35.521+0000	writing config.cache.chunks.athena.video_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena.video_distribution_data.bson
2023-01-16T16:31:35.522+0000	done dumping config.cache.chunks.athena.video_distribution_data (6 documents)
2023-01-16T16:31:35.522+0000	writing config.cache.chunks.athena.single_asset_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena.single_asset_distribution_data.bson
2023-01-16T16:31:35.523+0000	done dumping config.cache.chunks.athena.single_asset_distribution_data (6 documents)
2023-01-16T16:31:35.523+0000	writing config.cache.databases to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.databases.bson
2023-01-16T16:31:35.524+0000	done dumping config.cache.databases (5 documents)
2023-01-16T16:31:35.524+0000	writing config.cache.chunks.athena_qa.airing_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_qa.airing_data.bson
2023-01-16T16:31:35.525+0000	done dumping config.cache.chunks.athena_qa.airing_data (5 documents)
2023-01-16T16:31:35.525+0000	writing config.cache.chunks.athena_cs_qa.airing_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_qa.airing_data.bson
2023-01-16T16:31:35.526+0000	done dumping config.cache.chunks.athena_cs_qa.airing_data (3 documents)
2023-01-16T16:31:35.526+0000	writing config.cache.chunks.athena.airing_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena.airing_data.bson
2023-01-16T16:31:35.527+0000	done dumping config.cache.chunks.athena.airing_data (3 documents)
2023-01-16T16:31:35.527+0000	writing athena_qa.build_job to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_qa/build_job.bson
2023-01-16T16:31:35.528+0000	done dumping athena_qa.build_job (2 documents)
2023-01-16T16:31:35.528+0000	writing config.cache.chunks.athena_qa.affiliate to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_qa.affiliate.bson
2023-01-16T16:31:35.529+0000	done dumping config.cache.chunks.athena_qa.affiliate (1 document)
2023-01-16T16:31:35.530+0000	writing config.cache.chunks.athena_cs_qa.brand_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_qa.brand_data.bson
2023-01-16T16:31:35.530+0000	done dumping config.cache.chunks.athena_cs_qa.brand_data (1 document)
2023-01-16T16:31:35.531+0000	writing config.cache.chunks.athena_cs_dev.brand_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_dev.brand_data.bson
2023-01-16T16:31:35.531+0000	done dumping config.cache.chunks.athena_cs_dev.brand_data (1 document)
2023-01-16T16:31:35.532+0000	writing config.cache.chunks.athena_cs_qa.single_asset_distribution_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/cache.chunks.athena_cs_qa.single_asset_distribution_data.bson
2023-01-16T16:31:35.536+0000	done dumping config.cache.chunks.athena_cs_qa.single_asset_distribution_data (1 document)
2023-01-16T16:31:35.536+0000	writing config.image_collection to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/config/image_collection.bson
2023-01-16T16:31:35.537+0000	done dumping config.image_collection (0 documents)
2023-01-16T16:31:35.537+0000	writing athena_cs_qa.build_job to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_qa/build_job.bson
2023-01-16T16:31:35.538+0000	done dumping athena_cs_qa.build_job (0 documents)
2023-01-16T16:31:35.538+0000	writing athena_cs_qa.affiliate to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena_cs_qa/affiliate.bson
2023-01-16T16:31:35.539+0000	done dumping athena_cs_qa.affiliate (0 documents)
2023-01-16T16:31:35.539+0000	writing athena.airing_data to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena/airing_data.bson
2023-01-16T16:31:35.540+0000	done dumping athena.airing_data (0 documents)
2023-01-16T16:31:35.540+0000	writing athena.build_job to /home/cloud-user/backup/devqa-full/2023-01-16/devqa_athena_shard01/athena/build_job.bson
2023-01-16T16:31:35.563+0000	done dumping athena.single_asset_distribution_data (4416 documents)
2023-01-16T16:31:35.577+0000	done dumping athena.build_job (0 documents)
2023-01-16T16:31:36.779+0000	done dumping athena_cs_qa.video_distribution_data (603097 documents)
2023-01-16T16:31:37.727+0000	done dumping athena_cs_qa.distributable_content (63855 documents)
2023-01-16T16:31:37.729+0000	writing captured oplog to
2023-01-16T16:31:37.729+0000		dumped 1 oplog entry
finished full backup ourdb-sharded-mongo-01001.internal.lan:27018.
Backup done!
ourdb-sharded-mongo-02002.internal.lan:27018
cmd_permit_write/usr/bin/mongo --username admin --password MySecretPassword ourdb-sharded-mongo-02002.internal.lan:27018/admin  --quiet  --eval 'db.fsyncUnlock()' | egrep -i 'unlock completed|not locked'
ourdb-sharded-mongo-03001.internal.lan:27018
cmd_permit_write/usr/bin/mongo --username admin --password MySecretPassword ourdb-sharded-mongo-03001.internal.lan:27018/admin  --quiet  --eval 'db.fsyncUnlock()' | egrep -i 'unlock completed|not locked'
ourdb-sharded-mongo-01001.internal.lan:27018
cmd_permit_write/usr/bin/mongo --username admin --password MySecretPassword ourdb-sharded-mongo-01001.internal.lan:27018/admin  --quiet  --eval 'db.fsyncUnlock()' | egrep -i 'unlock completed|not locked'
balancer is started!
```
