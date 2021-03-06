"""
Copyright (c) 2015 SONATA-NFV
ALL RIGHTS RESERVED.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Neither the name of the SONATA-NFV [, ANY ADDITIONAL AFFILIATION]
nor the names of its contributors may be used to endorse or promote
products derived from this software without specific prior written
permission.

This work has been performed in the framework of the SONATA project,
funded by the European Commission under Grant number 671517 through
the Horizon 2020 and 5G-PPP programmes. The authors would like to
acknowledge the contributions of their colleagues of the SONATA
partner consortium (www.sonata-nfv.eu).
"""

"""
Test suite to automatically test emulator REST API endpoints.
"""

import os
import unittest
import requests
import simplejson as json

from emuvim.test.api_base_heat import ApiBaseHeat


class testRestApi(ApiBaseHeat):
    """
    Tests to check the REST API endpoints of the emulator.
    """

    def setUp(self):
        # create network
        self.createNet(nswitches=3, ndatacenter=2, nhosts=2, ndockers=0, autolinkswitches=True)

        # setup links
        self.net.addLink(self.dc[0], self.h[0])
        self.net.addLink(self.h[1], self.dc[1])
        self.net.addLink(self.dc[0], self.dc[1])

        # start api
        self.startApi()

        # start Mininet network
        self.startNet()

    def testChainingDummy(self):
        print('->>>>>>> test Chaining Class->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(" ")

        headers = {'Content-type': 'application/json'}
        test_heatapi_template_create_stack = open(os.path.join(os.path.dirname(__file__), "test_heatapi_template_chaining.json")).read()
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        requests.post(url, data=json.dumps(json.loads(test_heatapi_template_create_stack)), headers=headers)


        print('->>>>>>> test Chaining Versions ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/"
        listapiversionstackresponse = requests.get(url, headers=headers)
        self.assertEqual(listapiversionstackresponse.status_code, 200)
        self.assertEqual(json.loads(listapiversionstackresponse.content)["versions"][0]["id"], "v1")
        print(" ")

        print('->>>>>>> test Chaining List ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/list"
        chainlistresponse = requests.get(url, headers=headers)
        self.assertEqual(chainlistresponse.status_code, 200)
        self.assertEqual(json.loads(chainlistresponse.content)["chains"], [])
        print(" ")

        print('->>>>>>> test Loadbalancing List ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/list"
        lblistresponse = requests.get(url, headers=headers)
        self.assertEqual(lblistresponse.status_code, 200)
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"], [])
        print(" ")

        testchain = "dc0_s1_firewall1/fire-out-0/dc0_s1_iperf1/iper-in-0"
        print('->>>>>>> test Chain VNF Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" %(testchain)
        chainvnfresponse = requests.put(url)
        self.assertEqual(chainvnfresponse.status_code, 200)
        self.assertGreaterEqual(json.loads(chainvnfresponse.content)["cookie"], 0)
        print(" ")

        print('->>>>>>> test Chaining List ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/list"
        chainlistresponse = requests.get(url, headers=headers)
        self.assertEqual(chainlistresponse.status_code, 200)
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["dst_vnf"], "dc0_s1_firewall1")
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["dst_intf"], "fire-out-0")
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["src_vnf"], "dc0_s1_iperf1")
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["src_intf"], "iper-in-0")
        print(" ")

        print('->>>>>>> test Chain VNF Delete Chain ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        deletechainvnfresponse = requests.delete(url)
        self.assertEqual(deletechainvnfresponse.status_code, 200)
        self.assertEqual(deletechainvnfresponse.content, "true")
        print(" ")

        print('->>>>>>> test Chaining List If Empty Again ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/list"
        chainlistresponse = requests.get(url, headers=headers)
        self.assertEqual(chainlistresponse.status_code, 200)
        self.assertEqual(json.loads(chainlistresponse.content)["chains"], [])
        print(" ")

        testchain = "dc0_s1_firewall1/fire-out-0/dc0_s1_iperf1/iper-in-0"
        print('->>>>>>> test Stack Chain VNF Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        stackchainvnfresponse = requests.post(url, data=json.dumps(json.loads('{"path":["dc1.s1", "s1","s2","s3","s1","dc1.s1"]}')), headers=headers)
        self.assertEqual(stackchainvnfresponse.status_code, 200)
        print (stackchainvnfresponse.content)
        self.assertGreaterEqual(json.loads(stackchainvnfresponse.content)["cookie"], 0)
        print(" ")


        print('->>>>>>> test Stack Chaining List ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/list"
        chainlistresponse = requests.get(url, headers=headers)
        self.assertEqual(chainlistresponse.status_code, 200)
        print (chainlistresponse.content)
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["dst_vnf"], "dc0_s1_firewall1")
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["dst_intf"], "fire-out-0")
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["src_vnf"], "dc0_s1_iperf1")
        self.assertEqual(json.loads(chainlistresponse.content)["chains"][0]["src_intf"], "iper-in-0")
        self.assertItemsEqual(json.loads(chainlistresponse.content)["chains"][0]["path"],['dc1.s1', 's1', 's2', 's3', 's1', 'dc1.s1'])
        print(" ")

        print('->>>>>>> test Chain VNF Delete Chain ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        deletechainvnfresponse = requests.delete(url)
        self.assertEqual(deletechainvnfresponse.status_code, 200)
        self.assertEqual(deletechainvnfresponse.content, "true")
        print(" ")

        print('->>>>>>> test Chaining List If Empty Again ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/list"
        chainlistresponse = requests.get(url, headers=headers)
        self.assertEqual(chainlistresponse.status_code, 200)
        self.assertEqual(json.loads(chainlistresponse.content)["chains"], [])
        print(" ")


        testchain = "dc0_s1_firewall1/non-existing-interface/dc0_s1_iperf1/iper-in-0"
        print('->>>>>>> test Chain VNF Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        chainvnfresponse = requests.put(url)
        self.assertEqual(chainvnfresponse.status_code, 501)
        print(" ")

        testchain = "dc0_s1_firewall1/fire-out-0/dc0_s1_iperf1/non-existing-interface"
        print('->>>>>>> test Chain VNF Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        chainvnfresponse = requests.put(url)
        self.assertEqual(chainvnfresponse.status_code, 501)
        print(" ")

        testchain = "dc0_s1_firewall1/non-existing-interface/dc0_s1_iperf1/iper-in-0"
        print('->>>>>>> test Chain VNF Delete Chain ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        deletechainvnfresponse = requests.delete(url)
        self.assertEqual(deletechainvnfresponse.status_code, 501)
        print(" ")

        testchain = "dc0_s1_firewall1/fire-out-0/dc0_s1_iperf1/non-existing-interface"
        print('->>>>>>> test Chain VNF Delete Chain ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        deletechainvnfresponse = requests.delete(url)
        self.assertEqual(deletechainvnfresponse.status_code, 501)
        print(" ")

        testchain = "non-existent-dc/s1/firewall1/firewall1:cp03:output/dc0/s1/iperf1/iperf1:cp02:input"
        print('->>>>>>> test Chain VNF Non-Existing DC ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        chainvnfresponse = requests.put(url)
        self.assertEqual(chainvnfresponse.status_code, 500)
        print(" ")


        testchain = "dc0/s1/firewall1/non-existent:cp03:output/dc0/s1/iperf1/iperf1:cp02:input"
        print('->>>>>>> test Chain VNF Non-Existing Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        chainvnfresponse = requests.put(url)
        self.assertEqual(chainvnfresponse.status_code, 500)
        print(" ")

        testchain = "dc0/s1/firewall1/firewall1:cp03:output/dc0/s1/iperf1/non-existent:cp02:input"
        print('->>>>>>> test Chain VNF Non-Existing Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        chainvnfresponse = requests.put(url)
        self.assertEqual(chainvnfresponse.status_code, 500)
        print(" ")

        testchain = "dc0/s1/firewall1/firewall1:cp03:output/dc0/s1/iperf1/iperf1:cp02:input"
        print('->>>>>>> test Chain VNF Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        chainvnfresponse = requests.put(url)
        print (chainvnfresponse.content)
        self.assertEqual(chainvnfresponse.status_code, 200)
        self.assertGreaterEqual(json.loads(chainvnfresponse.content)["cookie"], 0)
        print(" ")

        print('->>>>>>> test Chain VNF Delete Chain ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        deletechainvnfresponse = requests.delete(url)
        self.assertEqual(deletechainvnfresponse.status_code, 200)
        self.assertEqual(deletechainvnfresponse.content, "true")
        print(" ")

        print('->>>>>>> test Chaining List If Empty Again ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/list"
        chainlistresponse = requests.get(url, headers=headers)
        self.assertEqual(chainlistresponse.status_code, 200)
        self.assertEqual(json.loads(chainlistresponse.content)["chains"], [])
        print(" ")

        testchain = "dc0/s1/firewall1/firewall1:cp03:output/dc0/s1/iperf1/iperf1:cp02:input"
        print('->>>>>>> test Stack Chain VNF Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        stackchainvnfresponse = requests.post(url, data=json.dumps(
            json.loads('{"path":["dc1.s1", "s1","s2","s3","s1","dc1.s1"]}')), headers=headers)
        self.assertEqual(stackchainvnfresponse.status_code, 200)
        print (stackchainvnfresponse.content)
        self.assertGreaterEqual(json.loads(stackchainvnfresponse.content)["cookie"], 0)
        print(" ")

        testchain = "dc0/s1/firewall1/firewall1:cp03:output/dc0/s1/iperf1/iperf1:cp02:input"
        print('->>>>>>> test Stack Chain VNF Interfaces ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/chain/%s" % (testchain)
        stackchainvnfresponse = requests.delete(url, headers=headers)
        self.assertEqual(stackchainvnfresponse.status_code, 200)
        print(" ")


        print('->>>>>>> test Loadbalancing ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/dc0/s1/firewall1/firewall1:cp03:output"
        lblistresponse = requests.post(url, data=json.dumps(
            {"dst_vnf_interfaces":[{"pop":"dc0","stack":"s1","server":"iperf1","port":"iperf1:cp02:input"}]})
            , headers=headers)
        print (lblistresponse.content)
        self.assertEqual(lblistresponse.status_code, 200)
        self.assertIn("dc0_s1_firewall1:fire-out-0", lblistresponse.content)
        print(" ")

        print('->>>>>>> test Loadbalancing List ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/list"
        lblistresponse = requests.get(url, headers=headers)
        self.assertEqual(lblistresponse.status_code, 200)
        print (lblistresponse.content )
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["paths"][0]["dst_vnf"], "dc0_s1_iperf1")
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["paths"][0]["dst_intf"], "iper-in-0")
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["src_vnf"], "dc0_s1_firewall1")
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["src_intf"],"fire-out-0")
        print(" ")

        print('->>>>>>> test delete Loadbalancing ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/dc0/s1/firewall1/firewall1:cp03:output"
        lbdeleteresponse = requests.delete(url, headers=headers)
        print (lbdeleteresponse.content)
        self.assertEqual(lbdeleteresponse.status_code, 200)
        print(" ")

        print('->>>>>>> testFloatingLoadbalancer ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/dc0/floating/bla/blubb"
        lblistresponse = requests.post(url, data=json.dumps(
            {"dst_vnf_interfaces":[{"pop":"dc0","stack":"s1","server":"iperf1","port":"iperf1:cp02:input"}]})
            , headers=headers)
        print (lblistresponse.content)
        self.assertEqual(lblistresponse.status_code, 200)
        resp = json.loads(lblistresponse.content)
        self.assertIsNotNone(resp.get('cookie'))
        self.assertIsNotNone(resp.get('floating_ip'))
        cookie = resp.get('cookie')
        print(" ")

        print('->>>>>>> testDeleteFloatingLoadbalancer ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/dc0/floating/%s/blubb" % cookie
        lblistresponse = requests.delete(url, headers=headers)
        print (lblistresponse.content)
        self.assertEqual(lblistresponse.status_code, 200)
        print(" ")

        print('->>>>>>> testLoadbalancingCustomPath ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/dc0_s1_firewall1/fire-out-0"
        lblistresponse = requests.post(url, data=json.dumps(
            {"dst_vnf_interfaces":{"dc0_s1_iperf1":"iper-in-0"},
             "path": {"dc0_s1_iperf1": {"iper-in-0": ["dc1.s1", "s1","s2","s3","s1","dc1.s1"]}}}), headers=headers)
        print (lblistresponse.content)
        self.assertEqual(lblistresponse.status_code, 200)
        self.assertIn("dc0_s1_firewall1:fire-out-0", lblistresponse.content)
        print(" ")

        print('->>>>>>> testLoadbalancingListCustomPath ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/list"
        lblistresponse = requests.get(url, headers=headers)
        self.assertEqual(lblistresponse.status_code, 200)
        print (lblistresponse.content )
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["paths"][0]["dst_vnf"], "dc0_s1_iperf1")
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["paths"][0]["dst_intf"], "iper-in-0")
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["paths"][0]["path"],
                         ["dc1.s1", "s1","s2","s3","s1","dc1.s1"] )
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["src_vnf"], "dc0_s1_firewall1")
        self.assertEqual(json.loads(lblistresponse.content)["loadbalancers"][0]["src_intf"],"fire-out-0")
        print(" ")


        print('->>>>>>> test Delete Loadbalancing ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/lb/dc0_s1_firewall1/fire-out-0"
        lblistresponse = requests.delete(url, headers=headers)
        self.assertEqual(lblistresponse.status_code, 200)
        print(" ")

        print('->>>>>>> test Query Topology ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:4000/v1/topo"
        topolistresponse = requests.get(url, headers=headers)
        print(topolistresponse.content)
        self.assertEqual(topolistresponse.status_code, 200)
        print(" ")



    def testMonitoringDummy(self):
        print('->>>>>>> test Monitoring Dummy Class->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(" ")

        headers = {'Content-type': 'application/json'}
        test_heatapi_template_create_stack = open(os.path.join(os.path.dirname(__file__), "test_heatapi_template_create_stack.json")).read()
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        requests.post(url, data=json.dumps(json.loads(test_heatapi_template_create_stack)),headers=headers)


        print('->>>>>>> test Monitoring List Versions ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/"
        listapiversionstackresponse = requests.get(url, headers=headers)
        self.assertEqual(listapiversionstackresponse.status_code, 200)
        self.assertEqual(json.loads(listapiversionstackresponse.content)["versions"][0]["id"], "v1")
        print(" ")

        print('->>>>>>> test Monitor VNF ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/dc0_s1_firewall1"
        listmonitoringvnfresponse = requests.get(url, headers=headers)
        self.assertEqual(listmonitoringvnfresponse.status_code, 200)
        self.assertGreaterEqual(json.loads(listmonitoringvnfresponse.content)["MEM_%"], 0)
        print(" ")

        print('->>>>>>> test Monitor VNF Abs Without Mininet Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/abs/dc0_s1_firewall1"
        listmonitoringvnfabsresponse = requests.get(url, headers=headers)
        self.assertEqual(listmonitoringvnfabsresponse.status_code, 200)
        self.assertGreaterEqual(json.loads(listmonitoringvnfabsresponse.content)["MEM_%"], 0)
        print(" ")

        print('->>>>>>> test Monitor VNF Abs Without Mininet Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/abs/mn.dc0_s1_firewall1"
        listmonitoringvnfabsmnresponse = requests.get(url, headers=headers)
        self.assertEqual(listmonitoringvnfabsmnresponse.status_code, 200)
        self.assertGreaterEqual(json.loads(listmonitoringvnfabsmnresponse.content)["MEM_%"], 0)
        print(" ")

        print('->>>>>>> test Monitor VNF Abs With Non-Existing VNF ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/abs/mn.dc0_s1_non_existing"
        listmonitoringvnfabsnonexistingresponse = requests.get(url, headers=headers)
        self.assertEqual(listmonitoringvnfabsnonexistingresponse.status_code, 500)
        print(" ")

        print('->>>>>>> test Monitor VNF DC Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/dc0/s1/firewall1:9df6a98f-9e11-4cb7-b3c0-InAdUnitTest"
        listmonitoringvnfdcstackresponse = requests.get(url, headers=headers)
        print(listmonitoringvnfdcstackresponse.content)
        self.assertEqual(listmonitoringvnfdcstackresponse.status_code, 200)
        self.assertGreaterEqual(json.loads(listmonitoringvnfdcstackresponse.content)["MEM_%"], 0)
        print(" ")

        print('->>>>>>> test Monitor VNF DC Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/dc0/s1/firewall1:9df6a98f-9e11-4cb7-b3c0-InAdUnitTest"
        listmonitoringvnfdcstackresponse = requests.get(url, headers=headers)
        self.assertEqual(listmonitoringvnfdcstackresponse.status_code, 200)
        self.assertGreaterEqual(json.loads(listmonitoringvnfdcstackresponse.content)["MEM_%"], 0)
        print(" ")

        print('->>>>>>> test Monitor VNF DC Stack With Non-Existing Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/dc0/s1/non_existing"
        listmonitoringvnfdcstackwithnonexistingnameresponse = requests.get(url, headers=headers)

        self.assertEqual(listmonitoringvnfdcstackwithnonexistingnameresponse.status_code, 500)
        print(" ")

        print('->>>>>>> test Monitor VNF DC Stack With Non-Existing DC ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/non_exisintg0/s1/firewall1"
        listmonitoringvnfdcstackwithnonexistingdcresponse = requests.get(url, headers=headers)
        self.assertEqual(listmonitoringvnfdcstackwithnonexistingdcresponse.status_code, 500)
        print(" ")

        print('->>>>>>> test Monitor VNF DC Stack With Non-Existing Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:3000/v1/monitor/dc0/non_existing_stack/firewall1"
        listmonitoringvnfdcstackwithnonexistingstackresponse = requests.get(url, headers=headers)
        self.assertEqual(listmonitoringvnfdcstackwithnonexistingstackresponse.status_code, 500)
        print(" ")





    def testNovaDummy(self):
        print('->>>>>>> test Nova Dummy Class->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(" ")

        headers = {'Content-type': 'application/json'}
        test_heatapi_template_create_stack = open(os.path.join(os.path.dirname(__file__), "test_heatapi_template_create_stack.json")).read()
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        requests.post(url, data=json.dumps(json.loads(test_heatapi_template_create_stack)),
                      headers=headers)

        print('->>>>>>> test Nova List Versions ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/"
        listapiversionnovaresponse = requests.get(url, headers=headers)
        self.assertEqual(listapiversionnovaresponse.status_code, 200)
        self.assertEqual(json.loads(listapiversionnovaresponse.content)["versions"][0]["id"], "v2.1")
        self.assertEqual(json.loads(listapiversionnovaresponse.content)["versions"][0]["status"], "CURRENT")
        self.assertEqual(json.loads(listapiversionnovaresponse.content)["versions"][0]["version"], "2.38")
        self.assertEqual(json.loads(listapiversionnovaresponse.content)["versions"][0]["min_version"], "2.1")
        self.assertEqual(json.loads(listapiversionnovaresponse.content)["versions"][0]["updated"], "2013-07-23T11:33:21Z")
        print(" ")

        print('->>>>>>> test Nova Version Show ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla"
        listapiversion21novaresponse = requests.get(url, headers=headers)
        self.assertEqual(listapiversion21novaresponse.status_code, 200)
        self.assertEqual(json.loads(listapiversion21novaresponse.content)["version"]["id"], "v2.1")
        self.assertEqual(json.loads(listapiversion21novaresponse.content)["version"]["status"], "CURRENT")
        self.assertEqual(json.loads(listapiversion21novaresponse.content)["version"]["version"], "2.38")
        self.assertEqual(json.loads(listapiversion21novaresponse.content)["version"]["min_version"], "2.1")
        self.assertEqual(json.loads(listapiversion21novaresponse.content)["version"]["updated"], "2013-07-23T11:33:21Z")
        print(" ")

        print('->>>>>>> test Nova Version List Server APIs ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers"
        listserverapisnovaresponse = requests.get(url, headers=headers)
        self.assertEqual(listserverapisnovaresponse.status_code, 200)
        self.assertNotEqual(json.loads(listserverapisnovaresponse.content)["servers"][0]["name"], "")
        print(" ")

        print('->>>>>>> test Nova Delete Server APIs ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/%s" % (json.loads(listserverapisnovaresponse.content)["servers"][0]["id"])
        deleteserverapisnovaresponse = requests.delete(url, headers=headers)
        self.assertEqual(deleteserverapisnovaresponse.status_code, 204)
        print(" ")

        print('->>>>>>> test Nova Delete Non-Existing Server APIs ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/non-existing-ix"
        deleteserverapisnovaresponse = requests.delete(url, headers=headers)
        self.assertEqual(deleteserverapisnovaresponse.status_code, 404)
        print(" ")


        print('->>>>>>> testNovaVersionListServerAPIs_withPortInformation ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/andPorts"
        listserverapisnovaresponse = requests.get(url, headers=headers)
        self.assertEqual(listserverapisnovaresponse.status_code, 200)
        self.assertNotEqual(json.loads(listserverapisnovaresponse.content)["servers"][0]["name"], "")
        print(" ")

        print('->>>>>>> test Nova List Flavors ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/flavors"
        listflavorsresponse = requests.get(url, headers=headers)
        self.assertEqual(listflavorsresponse.status_code, 200)
        self.assertIn(json.loads(listflavorsresponse.content)["flavors"][0]["name"], ["m1.nano", "m1.tiny", "m1.micro", "m1.small"])
        self.assertIn(json.loads(listflavorsresponse.content)["flavors"][1]["name"], ["m1.nano", "m1.tiny", "m1.micro", "m1.small"])
        self.assertIn(json.loads(listflavorsresponse.content)["flavors"][2]["name"], ["m1.nano", "m1.tiny", "m1.micro", "m1.small"])
        print(" ")

        print('->>>>>>> testNovaAddFlavors ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/flavors"
        addflavorsresponse = requests.post(url,
                                           data='{"flavor":{"name": "testFlavor", "vcpus": "test_vcpus", "ram": 1024, "disk": 10}}',
                                           headers=headers)
        self.assertEqual(addflavorsresponse.status_code, 200)
        self.assertIsNotNone(json.loads(addflavorsresponse.content)["flavor"]["id"])
        self.assertIsNotNone(json.loads(addflavorsresponse.content)["flavor"]["links"][0]['href'])
        print(" ")

        print('->>>>>>> test Nova List Flavors Detail ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/flavors/detail"
        listflavorsdetailresponse = requests.get(url, headers=headers)
        self.assertEqual(listflavorsdetailresponse.status_code, 200)
        self.assertIn(json.loads(listflavorsdetailresponse.content)["flavors"][0]["name"],["m1.nano", "m1.tiny", "m1.micro", "m1.small"])
        self.assertIn(json.loads(listflavorsdetailresponse.content)["flavors"][1]["name"],["m1.nano", "m1.tiny", "m1.micro", "m1.small"])
        self.assertIn(json.loads(listflavorsdetailresponse.content)["flavors"][2]["name"],["m1.nano", "m1.tiny", "m1.micro", "m1.small"])
        print(" ")

        print('->>>>>>> testNovaAddFlavors ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/flavors/detail"
        addflavorsresponse = requests.post(url,
                                           data='{"flavor":{"name": "testFlavor", "vcpus": "test_vcpus", "ram": 1024, "disk": 10}}',
                                           headers=headers)
        self.assertEqual(addflavorsresponse.status_code, 200)
        self.assertIsNotNone(json.loads(addflavorsresponse.content)["flavor"]["id"])
        self.assertIsNotNone(json.loads(addflavorsresponse.content)["flavor"]["links"][0]['href'])
        print(" ")

        print('->>>>>>> test Nova List Flavor By Id ->>>>>>>>>>>>>>>')

        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/flavors/%s" % (json.loads(listflavorsdetailresponse.content)["flavors"][0]["name"])
        listflavorsbyidresponse = requests.get(url, headers=headers)
        self.assertEqual(listflavorsbyidresponse.status_code, 200)
        self.assertEqual(json.loads(listflavorsbyidresponse.content)["flavor"]["id"], json.loads(listflavorsdetailresponse.content)["flavors"][0]["id"])
        print(" ")

        print('->>>>>>> test Nova List Images ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/images"
        listimagesresponse = requests.get(url, headers=headers)
        self.assertEqual(listimagesresponse.status_code, 200)
        print(listimagesresponse.content)
        # deactivated: highly depends on the environment in which the tests are executed. one cannot make such an assumption.
        #self.assertIn(json.loads(listimagesresponse.content)["images"][0]["name"],["google/cadvisor:latest", "ubuntu:trusty", "prom/pushgateway:latest"])
        #self.assertIn(json.loads(listimagesresponse.content)["images"][1]["name"],["google/cadvisor:latest", "ubuntu:trusty", "prom/pushgateway:latest"])
        #self.assertIn(json.loads(listimagesresponse.content)["images"][2]["name"],["google/cadvisor:latest", "ubuntu:trusty", "prom/pushgateway:latest"])
        print(" ")

        print('->>>>>>> test Nova List Images Details ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/images/detail"
        listimagesdetailsresponse = requests.get(url, headers=headers)
        self.assertEqual(listimagesdetailsresponse.status_code, 200)
        # deactivated: highly depends on the environment in which the tests are executed. one cannot make such an assumption.
        #self.assertIn(json.loads(listimagesdetailsresponse.content)["images"][0]["name"],["google/cadvisor:latest", "ubuntu:trusty", "prom/pushgateway:latest"])
        #self.assertIn(json.loads(listimagesdetailsresponse.content)["images"][1]["name"],["google/cadvisor:latest", "ubuntu:trusty", "prom/pushgateway:latest"])
        #self.assertIn(json.loads(listimagesdetailsresponse.content)["images"][2]["name"],["google/cadvisor:latest", "ubuntu:trusty", "prom/pushgateway:latest"])
        self.assertEqual(json.loads(listimagesdetailsresponse.content)["images"][0]["metadata"]["architecture"],"x86_64")
        print(" ")

        print('->>>>>>> test Nova List Image By Id ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/images/%s" % (json.loads(listimagesdetailsresponse.content)["images"][0]["id"])
        listimagebyidresponse = requests.get(url, headers=headers)
        self.assertEqual(listimagebyidresponse.status_code, 200)
        self.assertEqual(json.loads(listimagebyidresponse.content)["image"]["id"],json.loads(listimagesdetailsresponse.content)["images"][0]["id"])
        print(" ")

        print('->>>>>>> test Nova List Image By Non-Existend Id ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/images/non_existing_id"
        listimagebynonexistingidresponse = requests.get(url, headers=headers)
        self.assertEqual(listimagebynonexistingidresponse.status_code, 404)
        print(" ")

        #find ubuntu id
        for image in json.loads(listimagesresponse.content)["images"]:
            if image["name"] == "ubuntu:trusty":
                ubuntu_image_id = image["id"]



        print('->>>>>>> test Nova Create Server Instance ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers"
        data = '{"server": {"name": "X", "flavorRef": "%s", "imageRef":"%s"}}' % (json.loads(listflavorsresponse.content)["flavors"][0]["id"], ubuntu_image_id)
        createserverinstance = requests.post(url, data=data, headers=headers)
        self.assertEqual(createserverinstance.status_code, 200)
        self.assertEqual(json.loads(createserverinstance.content)["server"]["image"]["id"], ubuntu_image_id)
        print(" ")

        print('->>>>>>> test Nova Create Server Instance With Already Existing Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers"
        data = '{"server": {"name": "X", "flavorRef": "%s", "imageRef":"%s"}}' % (json.loads(listflavorsresponse.content)["flavors"][0]["id"], ubuntu_image_id)
        createserverinstance = requests.post(url, data=data, headers=headers)
        self.assertEqual(createserverinstance.status_code, 409)
        print(" ")

        print('->>>>>>> test Nova Version List Server APIs Detailed ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/detail"
        listserverapisdetailedresponse = requests.get(url, headers=headers)
        self.assertEqual(listserverapisdetailedresponse.status_code, 200)
        self.assertEqual(json.loads(listserverapisdetailedresponse.content)["servers"][0]["status"], "ACTIVE")
        print(" ")

        print('->>>>>>> test Nova Show Server Details ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/%s" % (json.loads(listserverapisdetailedresponse.content)["servers"][0]["id"])
        listserverdetailsresponse = requests.get(url, headers=headers)
        self.assertEqual(listserverdetailsresponse.status_code, 200)
        self.assertEqual(json.loads(listserverdetailsresponse.content)["server"]["flavor"]["links"][0]["rel"], "bookmark")
        print(" ")

        print('->>>>>>> test Nova Show Non-Existing Server Details ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/non_existing_server_id"
        listnonexistingserverdetailsresponse = requests.get(url, headers=headers)
        self.assertEqual(listnonexistingserverdetailsresponse.status_code, 404)
        print(" ")



    def testNeutronDummy(self):
        print('->>>>>>> test Neutron Dummy Class->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(" ")

        headers = {'Content-type': 'application/json'}
        test_heatapi_template_create_stack = open(os.path.join(os.path.dirname(__file__), "test_heatapi_template_create_stack.json")).read()
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        requests.post(url, data=json.dumps(json.loads(test_heatapi_template_create_stack)), headers=headers)
        # test_heatapi_keystone_get_token = open("test_heatapi_keystone_get_token.json").read()

        print('->>>>>>> test Neutron List Versions ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/"
        listapiversionstackresponse = requests.get(url, headers=headers)
        self.assertEqual(listapiversionstackresponse.status_code, 200)
        self.assertEqual(json.loads(listapiversionstackresponse.content)["versions"][0]["id"], "v2.0")
        print(" ")

        print('->>>>>>> test Neutron Show API v2.0 ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0"
        listapiversionv20response = requests.get(url, headers=headers)
        self.assertEqual(listapiversionv20response.status_code, 200)
        self.assertEqual(json.loads(listapiversionv20response.content)["resources"][0]["name"], "subnet")
        self.assertEqual(json.loads(listapiversionv20response.content)["resources"][1]["name"], "network")
        self.assertEqual(json.loads(listapiversionv20response.content)["resources"][2]["name"], "ports")
        print(" ")

        print('->>>>>>> test Neutron List Networks ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks"
        listnetworksesponse1 = requests.get(url, headers=headers)
        self.assertEqual(listnetworksesponse1.status_code, 200)
        self.assertEqual(json.loads(listnetworksesponse1.content)["networks"][0]["status"], "ACTIVE")
        listNetworksId = json.loads(listnetworksesponse1.content)["networks"][0]["id"]
        listNetworksName = json.loads(listnetworksesponse1.content)["networks"][0]["name"]
        listNetworksId2 = json.loads(listnetworksesponse1.content)["networks"][1]["id"]
        print(" ")

        print('->>>>>>> test Neutron List Non-Existing Networks ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks?name=non_existent_network_name"
        listnetworksesponse2 = requests.get(url,headers=headers)
        self.assertEqual(listnetworksesponse2.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron List Networks By Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks?name=" + listNetworksName #tcpdump-vnf:input:net:9df6a98f-9e11-4cb7-b3c0-InAdUnitTest
        listnetworksesponse3 = requests.get(url, headers=headers)
        self.assertEqual(listnetworksesponse3.status_code, 200)
        self.assertEqual(json.loads(listnetworksesponse3.content)["networks"][0]["name"], listNetworksName)
        print(" ")

        print('->>>>>>> test Neutron List Networks By Id ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks?id=" + listNetworksId  # tcpdump-vnf:input:net:9df6a98f-9e11-4cb7-b3c0-InAdUnitTest
        listnetworksesponse4 = requests.get(url, headers=headers)
        self.assertEqual(listnetworksesponse4.status_code, 200)
        self.assertEqual(json.loads(listnetworksesponse4.content)["networks"][0]["id"], listNetworksId)
        print(" ")

        print('->>>>>>> test Neutron List Networks By Multiple Ids ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks?id=" + listNetworksId + "&id="+ listNetworksId2 # tcpdump-vnf:input:net:9df6a98f-9e11-4cb7-b3c0-InAdUnitTest
        listnetworksesponse5 = requests.get(url, headers=headers)
        self.assertEqual(listnetworksesponse5.status_code, 200)
        self.assertEqual(json.loads(listnetworksesponse5.content)["networks"][0]["id"], listNetworksId)
        self.assertEqual(json.loads(listnetworksesponse5.content)["networks"][1]["id"], listNetworksId2)
        print(" ")

        print('->>>>>>> test Neutron Show Network ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks/"+listNetworksId
        shownetworksesponse = requests.get(url, headers=headers)
        self.assertEqual(shownetworksesponse.status_code, 200)
        self.assertEqual(json.loads(shownetworksesponse.content)["network"]["status"], "ACTIVE")
        print(" ")

        print('->>>>>>> test Neutron Show Network Non-ExistendNetwork ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks/non_existent_network_id"
        shownetworksesponse2 = requests.get(url, headers=headers)
        self.assertEqual(shownetworksesponse2.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron Create Network ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks"
        createnetworkresponse = requests.post(url, data='{"network": {"name": "sample_network","admin_state_up": true}}', headers=headers)
        self.assertEqual(createnetworkresponse.status_code, 201)
        self.assertEqual(json.loads(createnetworkresponse.content)["network"]["status"], "ACTIVE")
        print(" ")

        print('->>>>>>> test Neutron Create Network With Existing Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks"
        createnetworkresponsefailure = requests.post(url,data='{"network": {"name": "sample_network","admin_state_up": true}}',headers=headers)
        self.assertEqual(createnetworkresponsefailure.status_code, 400)
        print(" ")

        print('->>>>>>> test Neutron Update Network ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks/%s" % (json.loads(createnetworkresponse.content)["network"]["id"])
        updatenetworkresponse = requests.put(url, data='{"network": {"status": "ACTIVE", "admin_state_up":true, "tenant_id":"abcd123", "name": "sample_network_new_name", "shared":false}}' , headers=headers)
        self.assertEqual(updatenetworkresponse.status_code, 200)
        self.assertEqual(json.loads(updatenetworkresponse.content)["network"]["name"], "sample_network_new_name")
        self.assertEqual(json.loads(updatenetworkresponse.content)["network"]["tenant_id"], "abcd123")
        print(" ")

        print('->>>>>>> test Neutron Update Non-Existing Network ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks/non-existing-name123"
        updatenetworkresponse = requests.put(url, data='{"network": {"name": "sample_network_new_name"}}', headers=headers)
        self.assertEqual(updatenetworkresponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron List Subnets ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets"
        listsubnetsresponse = requests.get(url, headers=headers)
        listSubnetName = json.loads(listsubnetsresponse.content)["subnets"][0]["name"]
        listSubnetId = json.loads(listsubnetsresponse.content)["subnets"][0]["id"]
        listSubnetId2 = json.loads(listsubnetsresponse.content)["subnets"][1]["id"]
        self.assertEqual(listsubnetsresponse.status_code, 200)
        self.assertNotIn('None', listSubnetName)
        print(" ")

        print('->>>>>>> test Neutron List Subnets By Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets?name="+listSubnetName
        listsubnetByNameresponse = requests.get(url, headers=headers)
        self.assertEqual(listsubnetByNameresponse.status_code, 200)
        self.assertNotIn('None', json.loads(listsubnetByNameresponse.content)["subnets"][0]["name"])
        print(" ")

        print('->>>>>>> test Neutron List Subnets By Id ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets?id=" + listSubnetId
        listsubnetsbyidresponse = requests.get(url, headers=headers)
        self.assertEqual(listsubnetsbyidresponse.status_code, 200)
        self.assertNotIn("None", json.loads(listsubnetsbyidresponse.content)["subnets"][0]["name"])
        print(" ")

        print('->>>>>>> test Neutron List Subnets By Multiple Id ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets?id=" + listSubnetId +"&id="+listSubnetId2
        listsubnetsbymultipleidsresponse = requests.get(url, headers=headers)
        self.assertEqual(listsubnetsbymultipleidsresponse.status_code, 200)
        self.assertNotIn("None", json.loads(listsubnetsbymultipleidsresponse.content)["subnets"][0]["name"])
        print(" ")



        print('->>>>>>> test Neutron Show Subnet->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets/%s" % (json.loads(listsubnetsresponse.content)["subnets"][0]["id"])
        showsubnetsresponse = requests.get(url, headers=headers)
        self.assertEqual(showsubnetsresponse.status_code, 200)
        self.assertNotIn("None", json.loads(showsubnetsresponse.content)["subnet"]["name"])
        print(" ")

        print('->>>>>>> test Neutron Show Non-Existing Subnet->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets/non-existing-id123"
        showsubnetsresponse = requests.get(url, headers=headers)
        self.assertEqual(showsubnetsresponse.status_code, 404)
        print(" ")


        print('->>>>>>> test Neutron Create Subnet ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets"
        createsubnetdata = '{"subnet": {"name": "new_subnet", "network_id": "%s","ip_version": 4,"cidr": "10.0.0.1/24"} }' % (json.loads(createnetworkresponse.content)["network"]["id"])
        createsubnetresponse = requests.post(url, data=createsubnetdata, headers=headers)
        self.assertEqual(createsubnetresponse.status_code, 201)
        self.assertEqual(json.loads(createsubnetresponse.content)["subnet"]["name"], "new_subnet")
        print(" ")

        print('->>>>>>> test Neutron Create Second Subnet ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets"
        createsubnetdata = '{"subnet": {"name": "new_subnet", "network_id": "%s","ip_version": 4,"cidr": "10.0.0.1/24"} }' % (json.loads(createnetworkresponse.content)["network"]["id"])
        createsubnetfailureresponse = requests.post(url, data=createsubnetdata, headers=headers)
        self.assertEqual(createsubnetfailureresponse.status_code, 409)
        print(" ")

        print('->>>>>>> test Neutron Update Subnet ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets/%s" % (json.loads(createsubnetresponse.content)["subnet"]["id"])
        updatesubnetdata = '{"subnet": {"name": "new_subnet_new_name", "network_id":"some_id", "tenant_id":"new_tenant_id", "allocation_pools":"change_me", "gateway_ip":"192.168.1.120", "ip_version":4, "cidr":"10.0.0.1/24", "id":"some_new_id", "enable_dhcp":true} }'
        updatesubnetresponse = requests.put(url, data=updatesubnetdata, headers=headers)
        self.assertEqual(updatesubnetresponse.status_code, 200)
        self.assertEqual(json.loads(updatesubnetresponse.content)["subnet"]["name"], "new_subnet_new_name")
        print(" ")

        print('->>>>>>> test Neutron Update Non-Existing Subnet ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/subnets/non-existing-subnet-12345"
        updatenonexistingsubnetdata = '{"subnet": {"name": "new_subnet_new_name"} }'
        updatenonexistingsubnetresponse = requests.put(url, data=updatenonexistingsubnetdata, headers=headers)
        self.assertEqual(updatenonexistingsubnetresponse.status_code, 404)
        print(" ")



        print('->>>>>>> test Neutron List Ports ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports"
        listportsesponse = requests.get(url, headers=headers)
        self.assertEqual(listportsesponse.status_code, 200)
        self.assertEqual(json.loads(listportsesponse.content)["ports"][0]["status"], "ACTIVE")
        listPortsName = json.loads(listportsesponse.content)["ports"][0]["name"]
        listPortsId1 = json.loads(listportsesponse.content)["ports"][0]["id"]
        listPortsId2 = json.loads(listportsesponse.content)["ports"][1]["id"]
        print(" ")

        print('->>>>>>> test Neutron List Ports By Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports?name=" + listPortsName
        listportsbynameesponse = requests.get(url, headers=headers)
        self.assertEqual(listportsbynameesponse.status_code, 200)
        self.assertEqual(json.loads(listportsbynameesponse.content)["ports"][0]["name"], listPortsName)
        print(" ")

        print('->>>>>>> test Neutron List Ports By Id ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports?id=" + listPortsId1
        listportsbyidesponse = requests.get(url, headers=headers)
        self.assertEqual(listportsbyidesponse.status_code, 200)
        self.assertEqual(json.loads(listportsbyidesponse.content)["ports"][0]["id"], listPortsId1)
        print(" ")

        print('->>>>>>> test Neutron List Ports By Multiple Ids ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports?id=" + listPortsId1 +"&id="+listPortsId2
        listportsbymultipleidsesponse = requests.get(url, headers=headers)
        self.assertEqual(listportsbymultipleidsesponse.status_code, 200)
        self.assertEqual(json.loads(listportsbymultipleidsesponse.content)["ports"][0]["id"], listPortsId1)
        print(" ")

        print('->>>>>>> test Neutron List Non-Existing Ports ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports?id=non-existing-port-id"
        listportsbynonexistingidsesponse = requests.get(url, headers=headers)
        self.assertEqual(listportsbynonexistingidsesponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron Show Port ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports/%s" % (json.loads(listportsesponse.content)["ports"][0]["id"])
        showportresponse = requests.get(url, headers=headers)
        self.assertEqual(showportresponse.status_code, 200)
        self.assertEqual(json.loads(showportresponse.content)["port"]["status"], "ACTIVE")
        print(" ")

        print('->>>>>>> test Neutron Show Non-Existing Port ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports/non-existing-portid123"
        shownonexistingportresponse = requests.get(url, headers=headers)
        self.assertEqual(shownonexistingportresponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron Create Port In Non-Existing Network ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports"
        createnonexistingportdata = '{"port": {"name": "new_port", "network_id": "non-existing-id"} }'
        createnonexistingnetworkportresponse = requests.post(url, data=createnonexistingportdata, headers=headers)
        self.assertEqual(createnonexistingnetworkportresponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron Create Port ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports"
        createportdata = '{"port": {"name": "new_port", "network_id": "%s", "admin_state_up":true, "device_id":"device_id123", "device_owner":"device_owner123", "fixed_ips":"change_me","id":"new_id1234", "mac_address":"12:34:56:78:90", "status":"change_me", "tenant_id":"tenant_id123"} }' % (json.loads(createnetworkresponse.content)["network"]["id"])
        createportresponse = requests.post(url, data=createportdata, headers=headers)
        self.assertEqual(createportresponse.status_code, 201)
        print (createportresponse.content)
        self.assertEqual(json.loads(createportresponse.content)["port"]["name"], "new_port")
        print(" ")

        print('->>>>>>> test Neutron Create Port With Existing Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports"
        createportwithexistingnamedata = '{"port": {"name": "new_port", "network_id": "%s"} }' % (json.loads(createnetworkresponse.content)["network"]["id"])
        createportwithexistingnameresponse = requests.post(url, data=createportwithexistingnamedata, headers=headers)
        self.assertEqual(createportwithexistingnameresponse.status_code, 500)
        print(" ")

        print('->>>>>>> test Neutron Create Port Without Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports"
        createportdatawithoutname = '{"port": {"network_id": "%s"} }' % (json.loads(createnetworkresponse.content)["network"]["id"])
        createportwithoutnameresponse = requests.post(url, data=createportdatawithoutname, headers=headers)
        self.assertEqual(createportwithoutnameresponse.status_code, 201)
        self.assertIn("port:cp", json.loads(createportwithoutnameresponse.content)["port"]["name"])
        print(" ")

        print('->>>>>>> test Neutron Update Port ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(json.loads(createportresponse.content)["port"]["name"])
        url = "http://0.0.0.0:9696/v2.0/ports/%s" % (json.loads(createportresponse.content)["port"]["name"])
        updateportdata = '{"port": {"name": "new_port_new_name", "admin_state_up":true, "device_id":"device_id123", "device_owner":"device_owner123", "fixed_ips":"change_me","mac_address":"12:34:56:78:90", "status":"change_me", "tenant_id":"tenant_id123", "network_id":"network_id123"} }'
        updateportresponse = requests.put(url, data=updateportdata, headers=headers)
        self.assertEqual(updateportresponse.status_code, 200)
        self.assertEqual(json.loads(updateportresponse.content)["port"]["name"], "new_port_new_name")
        print(" ")

        print('->>>>>>> test Neutron Update Non-Existing Port ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports/non-existing-port-ip"
        updatenonexistingportdata = '{"port": {"name": "new_port_new_name"} }'
        updatenonexistingportresponse = requests.put(url, data=updatenonexistingportdata, headers=headers)
        self.assertEqual(updatenonexistingportresponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron Delete Port ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        righturl = "http://0.0.0.0:9696/v2.0/ports/%s" % (json.loads(createportresponse.content)["port"]["id"])
        deleterightportresponse = requests.delete(righturl, headers=headers)
        self.assertEqual(deleterightportresponse.status_code, 204)
        print(" ")


        print('->>>>>>> test Neutron Delete Non-Existing Port ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        wrongurl = "http://0.0.0.0:9696/v2.0/ports/unknownid"
        deletewrongportresponse = requests.delete(wrongurl, headers=headers)
        self.assertEqual(deletewrongportresponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Neutron Delete Subnet ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        wrongurl = "http://0.0.0.0:9696/v2.0/subnets/unknownid"
        righturl = "http://0.0.0.0:9696/v2.0/subnets/%s" % (json.loads(updatesubnetresponse.content)["subnet"]["id"])
        deletewrongsubnetresponse = requests.delete(wrongurl, headers=headers)
        deleterightsubnetresponse = requests.delete(righturl, headers=headers)
        self.assertEqual(deletewrongsubnetresponse.status_code, 404)
        self.assertEqual(deleterightsubnetresponse.status_code, 204)
        print(" ")

        print('->>>>>>> test Neutron Delete Network ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        righturl = "http://0.0.0.0:9696/v2.0/networks/%s" % (json.loads(createnetworkresponse.content)["network"]["id"])
        deleterightnetworkresponse = requests.delete(righturl, headers=headers)
        self.assertEqual(deleterightnetworkresponse.status_code, 204)
        print(" ")

        print('->>>>>>> test Neutron Delete Non-Existing Network ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        wrongurl = "http://0.0.0.0:9696/v2.0/networks/unknownid"
        deletewrongnetworkresponse = requests.delete(wrongurl, headers=headers)
        self.assertEqual(deletewrongnetworkresponse.status_code, 404)
        print(" ")

    def testKeystomeDummy(self):
        print('->>>>>>> test Keystone Dummy Class->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(" ")

        headers = {'Content-type': 'application/json'}
        test_heatapi_keystone_get_token = open(os.path.join(os.path.dirname(__file__), "test_heatapi_keystone_get_token.json")).read()

        print('->>>>>>> test Keystone List Versions ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:5000/"
        listapiversionstackresponse = requests.get(url, headers=headers)
        self.assertEqual(listapiversionstackresponse.status_code, 200)
        self.assertEqual(json.loads(listapiversionstackresponse.content)["versions"]["values"][0]["id"], "v2.0")
        print(" ")

        print('->>>>>>> test Keystone Show ApiV2 ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:5000/v2.0"
        showapiversionstackresponse = requests.get(url, headers=headers)
        self.assertEqual(showapiversionstackresponse.status_code, 200)
        self.assertEqual(json.loads(showapiversionstackresponse.content)["version"]["id"], "v2.0")
        print(" ")

        print('->>>>>>> test Keystone Get Token ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:5000/v2.0/tokens"
        gettokenstackresponse = requests.post(url, data=json.dumps(json.loads(test_heatapi_keystone_get_token)), headers=headers)
        self.assertEqual(gettokenstackresponse.status_code, 200)
        self.assertEqual(json.loads(gettokenstackresponse.content)["access"]["user"]["name"], "tenantName")
        print(" ")


    def testHeatDummy(self):
        print('->>>>>>> test Heat Dummy Class->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(" ")

        headers = {'Content-type': 'application/json'}
        test_heatapi_template_create_stack = open(os.path.join(os.path.dirname(__file__), "test_heatapi_template_create_stack.json")).read()
        test_heatapi_template_update_stack = open(os.path.join(os.path.dirname(__file__), "test_heatapi_template_update_stack.json")).read()

        print('->>>>>>> test Heat List API Versions Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/"
        listapiversionstackresponse = requests.get(url, headers=headers)
        self.assertEqual(listapiversionstackresponse.status_code, 200)
        self.assertEqual(json.loads(listapiversionstackresponse.content)["versions"][0]["id"], "v1.0")
        print(" ")

        print('->>>>>>> test Create Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        createstackresponse = requests.post(url, data=json.dumps(json.loads(test_heatapi_template_create_stack)), headers=headers)
        self.assertEqual(createstackresponse.status_code, 201)
        self.assertNotEqual(json.loads(createstackresponse.content)["stack"]["id"], "")
        print(" ")

        print('->>>>>>> test Create Stack With Existing Name ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        createstackwithexistingnameresponse = requests.post(url, data='{"stack_name" : "s1"}', headers=headers)
        self.assertEqual(createstackwithexistingnameresponse.status_code, 409)
        print(" ")

        print('->>>>>>> test Create Stack With Unsupported Version ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        createstackwitheunsupportedversionresponse = requests.post(url, data='{"stack_name" : "stackname123", "template" : {"heat_template_version": "2015-04-29"}}', headers=headers)
        self.assertEqual(createstackwitheunsupportedversionresponse.status_code, 400)
        print(" ")


        print('->>>>>>> test List Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        liststackresponse = requests.get(url, headers=headers)
        self.assertEqual(liststackresponse.status_code, 200)
        self.assertEqual(json.loads(liststackresponse.content)["stacks"][0]["stack_status"], "CREATE_COMPLETE")
        print(" ")


        print('->>>>>>> test Show Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123showStack/stacks/%s"% json.loads(createstackresponse.content)['stack']['id']
        liststackdetailsresponse = requests.get(url, headers=headers)
        self.assertEqual(liststackdetailsresponse.status_code, 200)
        self.assertEqual(json.loads(liststackdetailsresponse.content)["stack"]["stack_status"], "CREATE_COMPLETE")
        print(" ")

        print('->>>>>>> test Show Non-Exisitng Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123showStack/stacks/non_exisitng_id123"
        listnonexistingstackdetailsresponse = requests.get(url, headers=headers)
        self.assertEqual(listnonexistingstackdetailsresponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Update Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123updateStack/stacks/%s"% json.loads(createstackresponse.content)['stack']['id']
        updatestackresponse = requests.put(url, data=json.dumps(json.loads(test_heatapi_template_update_stack)),
                                            headers=headers)
        self.assertEqual(updatestackresponse.status_code, 202)
        liststackdetailsresponse = requests.get(url, headers=headers)
        self.assertEqual(json.loads(liststackdetailsresponse.content)["stack"]["stack_status"], "UPDATE_COMPLETE")
        print(" ")

        print('->>>>>>> test Update Non-Existing Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123updateStack/stacks/non_existing_id_1234"
        updatenonexistingstackresponse = requests.put(url, data={"non": "sense"}, headers=headers)
        self.assertEqual(updatenonexistingstackresponse.status_code, 404)
        print(" ")

        print('->>>>>>> test Delete Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123showStack/stacks/%s" % \
              json.loads(createstackresponse.content)['stack']['id']
        deletestackdetailsresponse = requests.delete(url, headers=headers)
        self.assertEqual(deletestackdetailsresponse.status_code, 204)
        print(" ")


    def test_CombinedTesting(self):
        print('->>>>>>> test Combinded tests->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        print(" ")

        headers = {'Content-type': 'application/json'}
        test_heatapi_template_create_stack = open(os.path.join(os.path.dirname(__file__),
                                                               "test_heatapi_template_create_stack.json")).read()
        test_heatapi_template_update_stack = open(os.path.join(os.path.dirname(__file__),
                                                               "test_heatapi_template_update_stack.json")).read()

        print('->>>>>>> test Combined Create Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123/stacks"
        createstackresponse = requests.post(url,
                                            data=json.dumps(json.loads(test_heatapi_template_create_stack)),
                                            headers=headers)
        self.assertEqual(createstackresponse.status_code, 201)
        self.assertNotEqual(json.loads(createstackresponse.content)["stack"]["id"], "")
        print(" ")

        print('->>>>>>> test Combined Neutron List Ports ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports"
        listportsesponse = requests.get(url, headers=headers)
        self.assertEqual(listportsesponse.status_code, 200)
        self.assertEqual(len(json.loads(listportsesponse.content)["ports"]), 9)
        for port in json.loads(listportsesponse.content)["ports"]:
            self.assertEqual(len(str(port['fixed_ips'][0]['subnet_id'])), 36)
        print(" ")

        print('->>>>>>> test Combined Neutron List Networks ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks"
        listnetworksesponse = requests.get(url, headers=headers)
        self.assertEqual(listnetworksesponse.status_code, 200)
        self.assertEqual(len(json.loads(listnetworksesponse.content)["networks"]), 10)
        for net in json.loads(listnetworksesponse.content)["networks"]:
            self.assertEqual(len(str(net['subnets'][0])), 36)
        print(" ")

        print('->>>>>>> test Combined Update Stack ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8004/v1/tenantabc123updateStack/stacks/%s"% \
              json.loads(createstackresponse.content)['stack']['id']
        updatestackresponse = requests.put(url,
                                           data=json.dumps(json.loads(test_heatapi_template_update_stack)),
                                           headers=headers)
        self.assertEqual(updatestackresponse.status_code, 202)
        liststackdetailsresponse = requests.get(url, headers=headers)
        self.assertEqual(json.loads(liststackdetailsresponse.content)["stack"]["stack_status"], "UPDATE_COMPLETE")
        print(" ")

        print('->>>>>>> test Combined Neutron List Ports ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/ports"
        listportsesponse = requests.get(url, headers=headers)
        self.assertEqual(listportsesponse.status_code, 200)
        self.assertEqual(len(json.loads(listportsesponse.content)["ports"]), 18)
        for port in json.loads(listportsesponse.content)["ports"]:
            self.assertEqual(len(str(port['fixed_ips'][0]['subnet_id'])), 36)
        print(" ")

        print('->>>>>>> test Combined Neutron List Networks ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/networks"
        listnetworksesponse = requests.get(url, headers=headers)
        self.assertEqual(listnetworksesponse.status_code, 200)
        self.assertEqual(len(json.loads(listnetworksesponse.content)["networks"]), 14)
        for net in json.loads(listnetworksesponse.content)["networks"]:
            self.assertEqual(len(str(net['subnets'][0])), 36)
        print(" ")


        # workflow create floating ip and assign it to a server

        print('->>>>>>> CombinedNeutronCreateFloatingIP ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:9696/v2.0/floatingips"
        createflip = requests.post(url, headers=headers,
                                            data='{"floatingip":{"floating_network_id":"default"}}')
        self.assertEqual(createflip.status_code, 200)
        self.assertIsNotNone(json.loads(createflip.content)["floatingip"].get("port_id"))
        port_id = json.loads(createflip.content)["floatingip"].get("port_id")
        print(" ")

        print('->>>>>>> CombinedNovaGetServer ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/detail"
        listserverapisdetailedresponse = requests.get(url, headers=headers)
        self.assertEqual(listserverapisdetailedresponse.status_code, 200)
        self.assertEqual(json.loads(listserverapisdetailedresponse.content)["servers"][0]["status"], "ACTIVE")
        server_id = json.loads(listserverapisdetailedresponse.content)["servers"][0]["id"]
        print(" ")

        print('->>>>>>> CombinedNovaAssignInterface ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/%s/os-interface" % server_id
        assign = requests.post(url, headers=headers,
                                            data='{"interfaceAttachment":{"net_id": "default"}}')
        self.assertEqual(assign.status_code, 202)
        self.assertIsNotNone(json.loads(assign.content)["interfaceAttachment"].get("port_id"))
        port_id = json.loads(assign.content)["interfaceAttachment"].get("port_id")
        print(" ")

        print('->>>>>>> CombinedNovaDeleteInterface ->>>>>>>>>>>>>>>')
        print('->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        url = "http://0.0.0.0:8774/v2.1/id_bla/servers/%s/os-interface/%s" % (server_id, port_id)
        getintfs = requests.delete(url, headers=headers)
        self.assertEqual(getintfs.status_code, 202)
        print(" ")


if __name__ == '__main__':
    unittest.main()
