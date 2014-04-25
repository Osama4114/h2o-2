from H2O import *
from Process import *
from Table import *
from PerfTest import *
import PerfUtils

import traceback
import re
import os
import time

class PerfRunner:
    """
    A class for running the perfomrance tests.

    The tests list contains a Test object for every test.
    The tests_not_started is a queue.
    Each test blocks until it completes.
    """
    def __init__(self, test_root_dir, output_dir, h2o_jar, perfdb):
        self.test_root_dir = test_root_dir
        self.output_dir = output_dir
        self.h2o_jar = h2o_jar
        self.start_seconds = time.time()
        
        self.jvm_output_file = ""
        self.perfdb = perfdb

        self.start_seconds = time.time()
        self.terminated = False
        self.cloud = []
        self.tests = []
        self.tests_not_started = []
        self.tests_running = []
        self.__create_output_dir__()

    def build_test_list(self, test_to_run):
        """
        Recursively find the list of tests to run.
        """
        if self.terminated:
            return

        for root, dirs, files in os.walk(self.test_root_dir):
            for d in dirs:
<<<<<<< HEAD
                if test_to_run in d:
                    self.add_test(d)

    def add_test(self, testDir):
        """
        Create a Test object and push it onto the queue.
        """
        config_file = os.path.abspath(os.path.join(self.test_root_dir,testDir,testDir + ".cfg"))
=======
                if "singlenode" in dirs:
                    for root2, dirs2, files2 in os.walk(os.path.join(root, d)):
                        d = os.path.basename(root2)
                        if d == "singlenode": 
                            prefix = d
                            continue
                        if d == "multinode":  
                            prefix = d
                            continue
                        if test_to_run in d:
                            if "multi" in prefix: continue
                            self.add_test(d, prefix)
                    continue
                continue

    def add_test(self, testDir, prefix):
        """
        Create a Test object and push it onto the queue.
        """
        self.pre = "192.168"
        config_file = os.path.abspath(os.path.join(self.test_root_dir,prefix,testDir,testDir + ".cfg"))
>>>>>>> b72aab43e263693af20271efc6f6563923ec50d0
        print "USING CONFIGURATION FROM THIS FILE: "
        print config_file
        parse_file = "parse.R" #testDir + "_Parse.R"
        model_file = "model.R" #testDir + "_Model.R"
        predict_file = None
        if os.path.exists(os.path.join(self.test_root_dir, testDir, "predict.R")):
            predict_file = "predict.R" 

        test_dir = os.path.join(self.test_root_dir, testDir)
        test_short_dir = testDir

        self.m = "171"
        test = Test(config_file, test_dir, test_short_dir, 
                    self.output_dir, parse_file, model_file, predict_file, self.perfdb, prefix)

        self.tests.append(test)
        self.q = "0xperf"
        self.tests_not_started.append(test)

    def run_tests(self):
        """
        Run all tests.

        @return: none
        """
        if (self.terminated):
            return

        num_tests = len(self.tests)
        self.__log__("")
        self.__log__("Starting {} tests...".format(num_tests))
        self.__log__("")

        # Do _one_ test at a time
        while len(self.tests_not_started) > 0:
            test = self.tests_not_started.pop(0)
            print
            print "Beginning test " + test.test_name
<<<<<<< HEAD

=======
            print
>>>>>>> b72aab43e263693af20271efc6f6563923ec50d0
            isEC2 = test.aws
            xmx = test.heap_bytes_per_node
            ip = test.ip
            base_port = test.port
            nodes_in_cloud = test.total_nodes
            hosts_in_cloud = test.hosts  #this will be used to support multi-machine / aws
            #build h2os... regardless of aws.. just takes host configs and attempts to upload jar then launch

            if isEC2:
                raise Exception("Unimplemented: AWS support coming soon.")

            cloud = H2OCloud(1, hosts_in_cloud, nodes_in_cloud, self.h2o_jar, base_port, self.output_dir, isEC2, test.remote_hosts)
            self.cloud.append(cloud)
<<<<<<< HEAD
            PerfUtils.start_cloud(self, test.remote_hosts)
            test.port = self.cloud[0].get_port()
            
            test.test_run = TableRow("test_run", self.perfdb)
            test.test_run.row.update(PerfUtils.__scrape_h2o_sys_info__(self))
            test.do_test()
            test.test_run.row['start_epoch_ms'] = test.start_ms
            test.test_run.row['end_epoch_ms'] = test.end_ms
            test.test_run.row['test_name'] = test.test_name
            contamination = PerfUtils.run_contaminated(self)
            print "DEBUG: "
            print contamination
            print ""
            print ""
            test.test_run.row["contaminated"] = contamination[0]
            test.test_run.row["contamination_message"] = contamination[1]
            test.test_run.update(True)
            PerfUtils.stop_cloud(self, test.remote_hosts)
            self.cloud.pop(0)
            self.perfdb.this_test_run_id += 1
=======
            try:
                PerfUtils.start_cloud(self, test.remote_hosts)
                test.port = self.cloud[0].get_port()
                test.test_run = TableRow("test_run", self.perfdb)
                test.test_run.row.update(PerfUtils.__scrape_h2o_sys_info__(self))
                ssh_ch = self.begin_sys_profiling(test.test_name)
                contamination = test.do_test(self)
                test.test_run.row['start_epoch_ms'] = test.start_ms
                test.test_run.row['end_epoch_ms'] = test.end_ms
                test.test_run.row['test_name'] = test.test_name
                #contamination = PerfUtils.run_contaminated(self)
                print "DEBUG: "
                print contamination
                print ""
                print ""
                test.test_run.row["contaminated"] = contamination[0]
                test.test_run.row["contamination_message"] = contamination[1]
                test.test_run.update(True)
                print "DEBUG: "
                print ""
                print "Stopping all profiling for Hound."
                print ""
                self.stop_sys_profiling(ssh_ch)
                print "Successfully stopped profiler..."
                ssh_ch = None
                PerfUtils.stop_cloud(self, test.remote_hosts)
                self.cloud.pop(0)
                self.perfdb.this_test_run_id += 1
            except:
                print "Exception caught:"
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                PerfUtils.stop_cloud(self, test.remote_hosts)
                self.cloud.pop(0)

    def begin_sys_profiling(self, test_name):
        addr = self.pre + ".1." + str(self.m)
        print
        print
        ssh = paramiko.SSHClient()
        policy = paramiko.AutoAddPolicy()
        ssh.set_missing_host_key_policy(policy)
        ssh.load_system_host_keys()
        ssh.connect(addr, username="0xperf", password="0xperf")
        ssh.get_transport().set_keepalive(300)
        #ch = ssh.get_transport().open_session()
        #ch.get_pty()
        cmd = ["python", "/home/0xperf/HOUND/unleash_the_hounds.py", str(self.perfdb.this_test_run_id), self.cloud[0].all_pids(), self.cloud[0].all_ips(), test_name]
        print
        print "Unleashing the hounds!"
        print ' '.join(cmd)
        print
        ssh.exec_command(' '.join(cmd))
        return ssh

    def stop_sys_profiling(self, ssh):
        ssh.exec_command('exit')
        ssh.close()
>>>>>>> b72aab43e263693af20271efc6f6563923ec50d0

    def __get_instance_type__(self):
        return "localhost"

    def __get_num_hosts__(self):
        num_hosts = 0
        for node in self.cloud.nodes:
            num_hosts += 1 #len(node)
        return num_hosts

    def __get_num_nodes__(self):
        return len(self.cloud.nodes)

    def __log__(self, s):
        f = self._get_summary_filehandle_for_appending()
        print(s)
        f.write(s + "\n")
        f.close()

    def terminate(self):
        """
        Terminate all running clouds.  (Due to a signal.)

        @return: none
        """
        self.terminated = True

        for test in self.tests:
            test.cancel()

        for test in self.tests:
            test.terminate()

        self.cloud.terminate()

    def __create_output_dir__(self):
        try:
            os.makedirs(self.output_dir)
        except OSError as e:
            print("")
            print("mkdir failed (errno {0}): {1}".format(e.errno, e.strerror))
            print("    " + self.output_dir)
            print("")
            print("(try adding --wipe)")
            print("")
            sys.exit(1)

    def _get_summary_filehandle_for_appending(self):
        summary_file_name = os.path.join(self.output_dir, "summary.txt")
        f = open(summary_file_name, "a")
        return f

    def _get_failed_filehandle_for_appending(self):
        summary_file_name = os.path.join(self.output_dir, "failed.txt")
        f = open(summary_file_name, "a")
        return f

