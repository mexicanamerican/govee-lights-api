import httpx
import uuid
from typing import List, Dict, Any, Optional
from config import settings


class GoveeClient:
    def __init__(self):
        self.base_url = settings.govee_base_url
        self.headers = {
            "Govee-API-Key": settings.govee_api_key,
            "Content-Type": "application/json",
        }

    def _request_id(self) -> str:
        return str(uuid.uuid4())

    def _rgb_to_int(self, r: int, g: int, b: int) -> int:
        return (r << 16) + (g << 8) + b

    async def get_devices(self) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/user/devices",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_device_state(self, device: str, sku: str) -> dict:
        async with httpx.AsyncClient() as client:
            payload = {
                "requestId": self._request_id(),
                "payload": {"sku": sku, "device": device},
            }
            response = await client.post(
                f"{self.base_url}/device/state",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def control_device(self, device: str, sku: str, capability: dict) -> dict:
        async with httpx.AsyncClient() as client:
            payload = {
                "requestId": self._request_id(),
                "payload": {
                    "sku": sku,
                    "device": device,
                    "capability": capability,
                },
            }
            response = await client.post(
                f"{self.base_url}/device/control",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()

    async def turn_on(self, device: str, sku: str) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.on_off", "instance": "powerSwitch", "value": 1}
        )

    async def turn_off(self, device: str, sku: str) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.on_off", "instance": "powerSwitch", "value": 0}
        )

    async def set_brightness(self, device: str, sku: str, brightness: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.range", "instance": "brightness", "value": brightness}
        )

    async def set_color(self, device: str, sku: str, r: int, g: int, b: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.color_setting", "instance": "colorRgb", "value": self._rgb_to_int(r, g, b)}
        )

    async def set_color_temp(self, device: str, sku: str, color_temp: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.color_setting", "instance": "colorTemperatureK", "value": color_temp}
        )

    async def set_toggle(self, device: str, sku: str, instance: str, value: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.toggle", "instance": instance, "value": value}
        )

    async def set_gradient_toggle(self, device: str, sku: str, value: int) -> dict:
        return await self.set_toggle(device, sku, "gradientToggle", value)

    async def set_segment_color(self, device: str, sku: str, segment: List[int], r: int, g: int, b: int) -> dict:
        return await self.control_device(
            device, sku,
            {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedColorRgb",
                "value": {"segment": segment, "rgb": self._rgb_to_int(r, g, b)}
            }
        )

    async def set_segment_brightness(self, device: str, sku: str, segment: List[int], brightness: int) -> dict:
        return await self.control_device(
            device, sku,
            {
                "type": "devices.capabilities.segment_color_setting",
                "instance": "segmentedBrightness",
                "value": {"segment": segment, "brightness": brightness}
            }
        )

    async def set_scene(self, device: str, sku: str, scene_value: int, instance: str = "lightScene") -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.dynamic_scene", "instance": instance, "value": scene_value}
        )

    async def set_diy_scene(self, device: str, sku: str, value: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.dynamic_scene", "instance": "diyScene", "value": value}
        )

    async def set_snapshot(self, device: str, sku: str, value: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.dynamic_scene", "instance": "snapshot", "value": value}
        )

    async def set_music_mode(
        self, device: str, sku: str, music_mode: int, sensitivity: int,
        auto_color: Optional[int] = None, r: Optional[int] = None, g: Optional[int] = None, b: Optional[int] = None
    ) -> dict:
        value = {"musicMode": music_mode, "sensitivity": sensitivity}
        if auto_color is not None:
            value["autoColor"] = auto_color
        if r is not None and g is not None and b is not None:
            value["rgb"] = self._rgb_to_int(r, g, b)
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.music_setting", "instance": "musicMode", "value": value}
        )

    async def set_work_mode(self, device: str, sku: str, work_mode: int, mode_value: int) -> dict:
        return await self.control_device(
            device, sku,
            {
                "type": "devices.capabilities.work_mode",
                "instance": "workMode",
                "value": {"workMode": work_mode, "modeValue": mode_value}
            }
        )

    async def set_range(self, device: str, sku: str, instance: str, value: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.range", "instance": instance, "value": value}
        )

    async def set_mode(self, device: str, sku: str, instance: str, value: int) -> dict:
        return await self.control_device(
            device, sku,
            {"type": "devices.capabilities.mode", "instance": instance, "value": value}
        )

    async def generic_control(self, device: str, sku: str, capability_type: str, instance: str, value: Any) -> dict:
        return await self.control_device(
            device, sku,
            {"type": capability_type, "instance": instance, "value": value}
        )

    async def draw_canvas(self, device: str, sku: str, pixels: List[Dict[str, Any]]) -> dict:
        results = []
        segments_by_color = {}
        for pixel in pixels:
            rgb = self._rgb_to_int(pixel["r"], pixel["g"], pixel["b"])
            if rgb not in segments_by_color:
                segments_by_color[rgb] = []
            segments_by_color[rgb].append(pixel["segment"])
        
        for rgb, segments in segments_by_color.items():
            r = (rgb >> 16) & 0xFF
            g = (rgb >> 8) & 0xFF
            b = rgb & 0xFF
            result = await self.set_segment_color(device, sku, segments, r, g, b)
            results.append(result)
        return {"results": results}

    async def fill_canvas(self, device: str, sku: str, segments: List[int], r: int, g: int, b: int) -> dict:
        return await self.set_segment_color(device, sku, segments, r, g, b)

    async def clear_canvas(self, device: str, sku: str, num_segments: int = 15) -> dict:
        return await self.set_segment_color(device, sku, list(range(num_segments)), 0, 0, 0)


govee_client = GoveeClient()