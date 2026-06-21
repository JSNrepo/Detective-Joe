import unittest
from plugins.demo_plugin import DemoPlugin


class TestDemoPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = DemoPlugin()

    def test_initialization(self):
        self.assertEqual(self.plugin.name, "demo")
        self.assertEqual(self.plugin.tool_name, "demo")
        self.assertEqual(
            self.plugin.categories, ["website", "organisation", "ip_server"]
        )
        self.assertEqual(self.plugin.required_tools, ["echo", "curl"])

    def test_target_validation(self):
        self.assertTrue(self.plugin.validate_target("example.com", "website"))
        self.assertTrue(
            self.plugin.validate_target("192.168.1.1", "ip_server")
        )
        self.assertFalse(self.plugin.validate_target("", "website"))
        self.assertFalse(self.plugin.validate_target("   ", "website"))
        self.assertFalse(self.plugin.validate_target(None, "website"))

    def test_build_command_website(self):
        cmd = self.plugin.build_command("example.com", "website")
        self.assertIn("curl -s -I --max-time 10 example.com", cmd)

    def test_build_command_organisation(self):
        cmd = self.plugin.build_command("Acme Corp", "organisation")
        self.assertEqual(cmd, "echo 'Demo: Organization info for Acme Corp'")

    def test_build_command_ip_server(self):
        cmd = self.plugin.build_command("192.168.1.1", "ip_server")
        self.assertEqual(cmd, "echo 'Demo: Server info for 192.168.1.1'")

    def test_build_command_other(self):
        cmd = self.plugin.build_command("target", "unknown_category")
        self.assertEqual(cmd, "echo 'Demo: Basic check for target'")

    def test_parse_output_website_success(self):
        output = (
            "HTTP/2 200\n"
            "Server: nginx/1.18.0 (Ubuntu)\n"
            "Date: Mon, 12 Jul 2021 12:00:00 GMT"
        )
        target = "example.com"
        category = "website"

        result = self.plugin.parse_output(output, target, category)

        self.assertEqual(result["target"], target)
        self.assertEqual(result["category"], category)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["raw_output"], output)

        artifacts = result["artifacts"]
        self.assertEqual(len(artifacts), 3)  # http status, server, demo info

        self.assertEqual(artifacts[0]["type"], "http_status")
        self.assertEqual(artifacts[0]["value"], "HTTP/2 200")
        self.assertEqual(artifacts[0]["confidence"], 0.9)

        self.assertEqual(artifacts[1]["type"], "server_software")
        self.assertEqual(artifacts[1]["value"], "nginx/1.18.0 (Ubuntu)")
        self.assertEqual(artifacts[1]["confidence"], 0.8)

        self.assertEqual(artifacts[2]["type"], "demo_info")
        self.assertEqual(
            artifacts[2]["value"], f"Demo scan completed for {target}"
        )

    def test_parse_output_other(self):
        output = "Demo: Server info for 192.168.1.1"
        target = "192.168.1.1"
        category = "ip_server"

        result = self.plugin.parse_output(output, target, category)

        self.assertEqual(result["target"], target)
        self.assertEqual(result["category"], category)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["raw_output"], output)

        artifacts = result["artifacts"]
        self.assertEqual(len(artifacts), 1)

        self.assertEqual(artifacts[0]["type"], "demo_info")
        self.assertEqual(
            artifacts[0]["value"], f"Demo scan completed for {target}"
        )
        self.assertEqual(artifacts[0]["confidence"], 1.0)
