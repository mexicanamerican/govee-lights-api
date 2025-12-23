from fastapi import FastAPI, HTTPException, Query
from govee_client import govee_client
from models import (
    DeviceIdentifier, PowerCommand, BrightnessCommand, ColorCommand, ColorTempCommand,
    ToggleCommand, SegmentColorCommand, SegmentBrightnessCommand, SceneCommand,
    DiySceneCommand, SnapshotCommand, MusicModeCommand, WorkModeCommand, RangeCommand,
    GenericCapabilityCommand, CanvasDrawCommand, CanvasFillCommand, CanvasClearCommand
)
from typing import Optional

app = FastAPI(
    title="Govee Lights API",
    version="2.0.0",
    description="FastAPI wrapper for Govee Developer API v2 with canvas drawing support"
)


@app.get("/devices")
async def list_devices():
    try:
        return await govee_client.get_devices()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}")
async def get_device(device_id: str, sku: str = Query(...)):
    try:
        devices_response = await govee_client.get_devices()
        devices = devices_response.get("data", [])
        for device in devices:
            if device.get("device") == device_id and device.get("sku") == sku:
                return device
        raise HTTPException(status_code=404, detail="Device not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}/state")
async def get_device_state_get(device_id: str, sku: str = Query(...)):
    try:
        return await govee_client.get_device_state(device_id, sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}/capabilities")
async def get_device_capabilities(device_id: str, sku: str = Query(...)):
    try:
        devices_response = await govee_client.get_devices()
        devices = devices_response.get("data", [])
        for device in devices:
            if device.get("device") == device_id and device.get("sku") == sku:
                return {"device": device_id, "sku": sku, "capabilities": device.get("capabilities", [])}
        raise HTTPException(status_code=404, detail="Device not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}/segments")
async def get_device_segments(device_id: str, sku: str = Query(...)):
    try:
        devices_response = await govee_client.get_devices()
        devices = devices_response.get("data", [])
        for device in devices:
            if device.get("device") == device_id and device.get("sku") == sku:
                capabilities = device.get("capabilities", [])
                for cap in capabilities:
                    if cap.get("type") == "devices.capabilities.segment_color_setting":
                        params = cap.get("parameters", {})
                        fields = params.get("fields", [])
                        for field in fields:
                            if field.get("fieldName") == "segment":
                                options = field.get("options", [])
                                segments = [opt.get("value") for opt in options]
                                return {"device": device_id, "sku": sku, "segments": segments, "count": len(segments)}
                return {"device": device_id, "sku": sku, "segments": [], "count": 0}
        raise HTTPException(status_code=404, detail="Device not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}/scenes")
async def get_device_scenes(device_id: str, sku: str = Query(...)):
    try:
        devices_response = await govee_client.get_devices()
        devices = devices_response.get("data", [])
        for device in devices:
            if device.get("device") == device_id and device.get("sku") == sku:
                capabilities = device.get("capabilities", [])
                scenes = {"lightScene": [], "diyScene": [], "snapshot": []}
                for cap in capabilities:
                    if cap.get("type") == "devices.capabilities.dynamic_scene":
                        instance = cap.get("instance")
                        if instance in scenes:
                            options = cap.get("parameters", {}).get("options", [])
                            scenes[instance] = [{"name": opt.get("name"), "value": opt.get("value")} for opt in options]
                return {"device": device_id, "sku": sku, "scenes": scenes}
        raise HTTPException(status_code=404, detail="Device not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}/music-modes")
async def get_device_music_modes(device_id: str, sku: str = Query(...)):
    try:
        devices_response = await govee_client.get_devices()
        devices = devices_response.get("data", [])
        for device in devices:
            if device.get("device") == device_id and device.get("sku") == sku:
                capabilities = device.get("capabilities", [])
                for cap in capabilities:
                    if cap.get("type") == "devices.capabilities.music_setting":
                        params = cap.get("parameters", {})
                        fields = params.get("fields", [])
                        for field in fields:
                            if field.get("fieldName") == "musicMode":
                                options = field.get("options", [])
                                modes = [{"name": opt.get("name"), "value": opt.get("value")} for opt in options]
                                return {"device": device_id, "sku": sku, "musicModes": modes}
                return {"device": device_id, "sku": sku, "musicModes": []}
        raise HTTPException(status_code=404, detail="Device not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}/current-color")
async def get_device_current_color(device_id: str, sku: str = Query(...)):
    try:
        state_response = await govee_client.get_device_state(device_id, sku)
        payload = state_response.get("payload", {})
        capabilities = payload.get("capabilities", [])
        result = {"device": device_id, "sku": sku, "online": False, "power": None, "brightness": None, "color": None, "colorTemp": None}
        for cap in capabilities:
            instance = cap.get("instance")
            state = cap.get("state", {})
            value = state.get("value")
            if instance == "online":
                result["online"] = value
            elif instance == "powerSwitch":
                result["power"] = "on" if value == 1 else "off"
            elif instance == "brightness":
                result["brightness"] = value
            elif instance == "colorRgb" and value is not None:
                if isinstance(value, int):
                    result["color"] = {"r": (value >> 16) & 0xFF, "g": (value >> 8) & 0xFF, "b": value & 0xFF, "raw": value}
            elif instance == "colorTemperatureK":
                result["colorTemp"] = value
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/devices/{device_id}/full-state")
async def get_device_full_state(device_id: str, sku: str = Query(...)):
    try:
        state_response = await govee_client.get_device_state(device_id, sku)
        devices_response = await govee_client.get_devices()
        devices = devices_response.get("data", [])
        device_info = None
        for device in devices:
            if device.get("device") == device_id and device.get("sku") == sku:
                device_info = device
                break
        return {
            "device": device_id,
            "sku": sku,
            "deviceInfo": device_info,
            "currentState": state_response.get("payload", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/state")
async def get_device_state(req: DeviceIdentifier):
    try:
        return await govee_client.get_device_state(req.device, req.sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/power")
async def set_power(cmd: PowerCommand):
    try:
        if cmd.value == 1:
            return await govee_client.turn_on(cmd.device, cmd.sku)
        return await govee_client.turn_off(cmd.device, cmd.sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/power/on")
async def turn_on(req: DeviceIdentifier):
    try:
        return await govee_client.turn_on(req.device, req.sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/power/off")
async def turn_off(req: DeviceIdentifier):
    try:
        return await govee_client.turn_off(req.device, req.sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/brightness")
async def set_brightness(cmd: BrightnessCommand):
    try:
        return await govee_client.set_brightness(cmd.device, cmd.sku, cmd.brightness)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/color")
async def set_color(cmd: ColorCommand):
    try:
        return await govee_client.set_color(cmd.device, cmd.sku, cmd.r, cmd.g, cmd.b)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/color-temp")
async def set_color_temp(cmd: ColorTempCommand):
    try:
        return await govee_client.set_color_temp(cmd.device, cmd.sku, cmd.color_temp)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/toggle")
async def set_toggle(cmd: ToggleCommand):
    try:
        return await govee_client.set_toggle(cmd.device, cmd.sku, cmd.instance, cmd.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/gradient")
async def set_gradient(cmd: PowerCommand):
    try:
        return await govee_client.set_gradient_toggle(cmd.device, cmd.sku, cmd.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/segment/color")
async def set_segment_color(cmd: SegmentColorCommand):
    try:
        return await govee_client.set_segment_color(cmd.device, cmd.sku, cmd.segment, cmd.r, cmd.g, cmd.b)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/segment/brightness")
async def set_segment_brightness(cmd: SegmentBrightnessCommand):
    try:
        return await govee_client.set_segment_brightness(cmd.device, cmd.sku, cmd.segment, cmd.brightness)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/scene")
async def set_scene(cmd: SceneCommand):
    try:
        return await govee_client.set_scene(cmd.device, cmd.sku, cmd.value, cmd.instance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/diy-scene")
async def set_diy_scene(cmd: DiySceneCommand):
    try:
        return await govee_client.set_diy_scene(cmd.device, cmd.sku, cmd.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/snapshot")
async def set_snapshot(cmd: SnapshotCommand):
    try:
        return await govee_client.set_snapshot(cmd.device, cmd.sku, cmd.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/music-mode")
async def set_music_mode(cmd: MusicModeCommand):
    try:
        return await govee_client.set_music_mode(
            cmd.device, cmd.sku, cmd.music_mode, cmd.sensitivity,
            cmd.auto_color, cmd.r, cmd.g, cmd.b
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/work-mode")
async def set_work_mode(cmd: WorkModeCommand):
    try:
        return await govee_client.set_work_mode(cmd.device, cmd.sku, cmd.work_mode, cmd.mode_value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/range")
async def set_range(cmd: RangeCommand):
    try:
        return await govee_client.set_range(cmd.device, cmd.sku, cmd.instance, cmd.value)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/devices/control")
async def generic_control(cmd: GenericCapabilityCommand):
    try:
        return await govee_client.generic_control(
            cmd.device, cmd.sku, cmd.capability_type, cmd.instance, cmd.value
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/canvas/draw")
async def canvas_draw(cmd: CanvasDrawCommand):
    try:
        pixels = [{"segment": p.segment, "r": p.r, "g": p.g, "b": p.b} for p in cmd.pixels]
        return await govee_client.draw_canvas(cmd.device, cmd.sku, pixels)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/canvas/fill")
async def canvas_fill(cmd: CanvasFillCommand):
    try:
        return await govee_client.fill_canvas(cmd.device, cmd.sku, cmd.segments, cmd.r, cmd.g, cmd.b)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/canvas/clear")
async def canvas_clear(cmd: CanvasClearCommand):
    try:
        return await govee_client.clear_canvas(cmd.device, cmd.sku)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))