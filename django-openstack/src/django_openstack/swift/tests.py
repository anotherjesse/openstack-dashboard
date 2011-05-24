#!/usr/bin/env python

"""
Testing the manager is actually pretty stupid, because it's really just
checking that the manager accepts cloudfiles objects and correctly returns them
again.
"""

import mox
from cloudfiles.connection import Connection 
from cloudfiles.container import Container 
import unittest
from manager import SwiftManager

class SwiftManagerTests(unittest.TestCase):
    def setUp(self):
        self.mox = mox.Mox()
        self.manager = SwiftManager('test', 'test', 'test')
        self.manager.get_swift_connection = self.mox.CreateMockAnything()

    def tearDown(self):
        self.mox.UnsetStubs()


    def test_get_container_names(self):
        container1 = self.mox.CreateMock(Container)
        container1.name = "testContainer1"
        container2 = self.mox.CreateMock(Container)
        container2.name = "testContainer2"
        containers = [container1, container2]
        swiftConn = self.mox.CreateMock(Connection)
        swiftConn.get_all_containers().AndReturn(containers)

        self.manager.get_swift_connection.__call__().AndReturn(swiftConn)

        self.mox.ReplayAll()

        names = [d["name"] for d in self.manager.get_container_names()]
        self.assertEqual(len(names), 2)
        self.assertTrue("testContainer1" in names)
        self.assertTrue("testContainer2" in names)

        self.mox.VerifyAll()

