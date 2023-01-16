#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
function description:
1-parse config file;
2-connect to router, close 'balancer', then forbid writing;
5-connect to router, open 'balancer', then permit writing.
Based on https://github.com/xdhuqing/mongo-backup-for-shard-cluster
date: 2023-01-16
version: v1.0.1
'''

import os
import sys
import pymongo
import ConfigParser
import commands
from time import sleep
from pyasn1.compat.octets import null

'''
description: config class, parse and check config parameters.
'''
class Config:
    '''
    '''
    def __init__(self,path):
        self.parser = ConfigParser.ConfigParser()
        self.path=path
        self.mongo_bin_dir = ''
        self.backup_dir = ''

        self.mongos_addr = ''
        self.mongos_port = -1

        self.config_addr = ''
        self.config_port = -1

        self.mongo_user = ''
        self.mongo_pass = ''

        self.parseConfig()

    def parseConfig(self):
        self.parser.read(self.path)

        self.mongo_bin_dir = self.parser.get('base-options', 'mongo_bin_dir')
        self.backup_dir = self.parser.get('base-options', 'backup_dir')

        self.mongos_addr = self.parser.get('mongos-options', 'mongos_addr')
        self.mongos_port = int(self.parser.get('mongos-options', 'mongos_port'))

        self.config_addr = self.parser.get('config-server-options', 'config_addr')
        self.config_port = self.parser.get('config-server-options', 'config_port')

        self.mongo_user = self.parser.get('auth', 'username')
        self.mongo_pass = self.parser.get('auth', 'password')

    def __str__(self):
        return 'mongo_bin_dir is: '+self.mongo_bin_dir+'\n'     \
            +'backup_dir is: '+self.backup_dir+'\n'   \
            +'mongos_addr is: '+self.mongos_addr+'\n'               \
            +'mongos_port is: '+str(self.mongos_port)+'\n'      \
            +'config_addr is: '+self.config_addr+'\n'               \
            +'config_port is: '+str(self.config_port)+'\n'

'''
description: Backup class, execute backup command.
'''
class Backup:
    def __init__(self,config):
        self.backupFinished = False
        self.config = config
        self.client = pymongo.MongoClient(self.config.mongos_addr,int(self.config.mongos_port), username=self.config.mongo_user, password=self.config.mongo_pass)
        self.shard_info = []
        #for each shard, only one second used
        self.second_node_used = {}

    def getShardInfo(self):
        collection = self.client.get_database("config").get_collection("shards")
        shard_doc = collection.find()
        if shard_doc:
            for shard in shard_doc:
                tempDict = {}
                tempDict['name'] = shard.get('_id')
                host = shard.get('host')
                if str(host).find('/') != -1:
                    host = shard.get('host').split('/')[1]
                tempDict['host'] = host
                self.shard_info.append(tempDict)
            return True

    def prepareForBackup(self):
        #close balancer
        config_col = self.client.get_database("config").get_collection("settings")
        config_col.update({'_id':'balancer'},{'$set':{'stopped':True}}, True)
        doc = config_col.find({'_id':'balancer'})
        if not doc:
            print "closing balancer fails!"
            return False
        if doc and str(doc).lower().find('true'):
            print "balancer is stopped!"

        #forbid each shard's one second from writing
        for shard in self.shard_info:
            second_node = []
            second_node = self.getSecondary(shard['host'])
            if second_node.__len__() == 0:
                 return False
            self.second_node_used[shard['name']] = second_node[0]
            cmd_forbid_write = self.config.mongo_bin_dir + "/mongo" + " --username " + self.config.mongo_user + " --password "  + self.config.mongo_pass + " " +  \
                          str(second_node[0]) + "/admin "     \
                          " --quiet " +              \
                          " --eval 'rs.slaveOk();db.fsyncLock();db.currentOp();' "+\
                          "| grep 'fsyncLock\\>' " +\
                          "| grep true"
            print 'cmd_forbid_write: ' + cmd_forbid_write
            status, isLocked = commands.getstatusoutput(cmd_forbid_write)
            print isLocked
            if status != 0 or not isLocked:
                print 'fsncLock '+ second_node[0] + ' fail! exist now!'
                return False
        return True

    def recoverMongosAfterBackup(self):
        #unlock each shard's second
        for second in self.second_node_used.itervalues():
            print second
            cmd_permit_write = self.config.mongo_bin_dir + "/mongo" + " --username " + self.config.mongo_user + " --password "  + self.config.mongo_pass + " " + \
                               str(second) + "/admin "   \
                               " --quiet " +                \
                               " --eval 'db.fsyncUnlock()'"+\
                               " | egrep -i 'unlock completed|not locked' "
            print 'cmd_permit_write: ' + cmd_permit_write
            status, unLocked = commands.getstatusoutput(cmd_permit_write)
            if status != 0 or not unLocked:
                print 'fsncUnlock '+ second + ' fail!'

        #open balancer
        config_col = self.client.get_database("config").get_collection("settings")
        config_col.update({'_id':'balancer'},{'$set':{'stopped':False}}, True)
        doc = config_col.find({'_id':'balancer'})
        if not doc:
            print "starting balancer fails!"
            return False
        if doc and str(doc).lower().find('false'):
            print "balancer is started!"
        return True

    def backupConfig(self):
        if check_dir(self.config.backup_dir):
            status, date = commands.getstatusoutput("date +%Y-%m-%d")
            backup_dir = self.config.backup_dir + '/' + date
            commands.getstatusoutput("mkdir -p "+backup_dir)
            cmd_line = self.config.mongo_bin_dir + "/mongodump" +       \
                " --username " + self.config.mongo_user +               \
                " --password "  + self.config.mongo_pass +              \
                " --host " + self.config.config_addr +                  \
                " --port " + str(self.config.config_port) +             \
                " --oplog" +                                            \
                " --out "  + backup_dir
            print 'cmd_line: ' + cmd_line
            status, output = commands.getstatusoutput(cmd_line)
            print output
            if status != 0 or not output:
                print "backup config " + str(self.config.config_addr) + ':' + str(self.config.config_port) + " failed!"
                return False
            print 'finished backup config ' + str(self.config.config_addr) + ':' + str(self.config.config_port) + '.'
            return True

    def fullBackupShard(self):
         dir = self.config.backup_dir
         if check_dir(dir):
             for shard in self.shard_info:
                 #create new dir for each shard
                status, date = commands.getstatusoutput("date +%Y-%m-%d")
                backup_dir = dir + '/' + date+ '/' + shard['name']
                commands.getstatusoutput("mkdir -p "+backup_dir)

                #get the second node of this shard
                second = self.second_node_used[shard['name']]
                if second == null:
                    return False

                #do dump
                cmd_dump = self.config.mongo_bin_dir + "/mongodump" +   \
                    " --username " + self.config.mongo_user +           \
                    " --password "  + self.config.mongo_pass +          \
                    " --host " + str(second) +                          \
                    " --oplog" +                                        \
                    " --out "  + backup_dir
                print 'cmd_dump: ' + cmd_dump
                status, output = commands.getstatusoutput(cmd_dump)
                print output
                if status != 0 or not output:
                    print "full backup shard " + str(second) + " failed!"
                    return False
                print "finished full backup " + str(second) + "."
                return True


    def getSecondary(self, shard):
        secondaryList = []
        print shard + ':getting secondaries ... '
        shard_client = pymongo.MongoClient(shard)

        #get server info first, otherwise shard_client.secondaries return nothing
        shard_client.server_info()
        for second in shard_client.secondaries:
            secondaryList.append(second[0]+':'+str(second[1]))
        return secondaryList

'''
description: function, check if the given directory exists.
return: True-if exists, False-if not.
'''
def check_dir(dir):
    if os.path.isdir(dir):
        return True
    else:
        print str(dir)+' does not exists!'
        return False

'''
description: function, control the whole process of restoring.
return: None.
'''
def Launcher(path):
    config = Config(path)
    print(config)

    back = Backup(config)
    if back.getShardInfo():
        print "get shard info successfully!"
        if back.prepareForBackup():
            print "now, ready for backup!"
            if back.backupConfig() and back.fullBackupShard():
                print "Backup done!"
        #recover mongos
        back.recoverMongosAfterBackup()
        return True

'''
description: like main function
return: None.
'''
if __name__ == '__main__':
    Launcher('mongos_backup.conf')
