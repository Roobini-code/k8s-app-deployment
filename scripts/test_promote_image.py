import tempfile
import unittest
from pathlib import Path

from promote_image import promote


class PromoteImageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)
        self.image = "docker.io/example/k8s-app-deployment:abc123"
        for slot in ("blue", "green"):
            (self.base_dir / f"deployment-{slot}.yaml").write_text(
                f"""kind: Deployment
metadata:
  name: deploylab-{slot}
spec:
  template:
    spec:
      containers:
        - name: web
          image: docker.io/example/k8s-app-deployment:old
""",
                encoding="utf-8",
            )
        (self.base_dir / "service.yaml").write_text(
            """kind: Service
metadata:
  name: deploylab
spec:
  selector:
    app.kubernetes.io/name: deploylab
    app.kubernetes.io/slot: blue
""",
                encoding="utf-8",
            )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_initial_release_seeds_both_slots_and_keeps_blue_active(self) -> None:
        for slot in ("blue", "green"):
            path = self.base_dir / f"deployment-{slot}.yaml"
            path.write_text(
                path.read_text(encoding="utf-8").replace(":old", ":replace-me"),
                encoding="utf-8",
            )

        result = promote(self.base_dir, self.image)

        self.assertIn("Initialized both slots", result)
        for slot in ("blue", "green"):
            text = (self.base_dir / f"deployment-{slot}.yaml").read_text(encoding="utf-8")
            self.assertIn(f"image: {self.image}", text)
        service = (self.base_dir / "service.yaml").read_text(encoding="utf-8")
        self.assertIn("app.kubernetes.io/slot: blue", service)

    def test_updates_green_and_switches_service_when_blue_is_active(self) -> None:
        result = promote(self.base_dir, self.image)

        self.assertIn("Updated green", result)
        blue = (self.base_dir / "deployment-blue.yaml").read_text(encoding="utf-8")
        green = (self.base_dir / "deployment-green.yaml").read_text(encoding="utf-8")
        service = (self.base_dir / "service.yaml").read_text(encoding="utf-8")
        self.assertIn("image: docker.io/example/k8s-app-deployment:old", blue)
        self.assertIn(f"image: {self.image}", green)
        self.assertIn("app.kubernetes.io/slot: green", service)

    def test_next_release_updates_blue_and_switches_service_back(self) -> None:
        promote(self.base_dir, self.image)
        next_image = "docker.io/example/k8s-app-deployment:def456"

        promote(self.base_dir, next_image)

        blue = (self.base_dir / "deployment-blue.yaml").read_text(encoding="utf-8")
        green = (self.base_dir / "deployment-green.yaml").read_text(encoding="utf-8")
        service = (self.base_dir / "service.yaml").read_text(encoding="utf-8")
        self.assertIn(f"image: {next_image}", blue)
        self.assertIn(f"image: {self.image}", green)
        self.assertIn("app.kubernetes.io/slot: blue", service)


if __name__ == "__main__":
    unittest.main()
