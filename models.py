from pydantic import BaseModel, Field
from typing import Optional, List, Any, Dict


class DeviceIdentifier(BaseModel):
    device: str
    sku: str


class PowerCommand(BaseModel):
    device: str
    sku: str
    value: int = Field(..., ge=0, le=1)


class BrightnessCommand(BaseModel):
    device: str
    sku: str
    brightness: int = Field(..., ge=1, le=100)


class ColorCommand(BaseModel):
    device: str
    sku: str
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)


class ColorTempCommand(BaseModel):
    device: str
    sku: str
    color_temp: int = Field(..., ge=2000, le=9000)


class ToggleCommand(BaseModel):
    device: str
    sku: str
    instance: str
    value: int = Field(..., ge=0, le=1)


class SegmentColorCommand(BaseModel):
    device: str
    sku: str
    segment: List[int]
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)


class SegmentBrightnessCommand(BaseModel):
    device: str
    sku: str
    segment: List[int]
    brightness: int = Field(..., ge=0, le=100)


class SceneCommand(BaseModel):
    device: str
    sku: str
    instance: str = "lightScene"
    value: int


class DiySceneCommand(BaseModel):
    device: str
    sku: str
    value: int


class SnapshotCommand(BaseModel):
    device: str
    sku: str
    value: int


class MusicModeCommand(BaseModel):
    device: str
    sku: str
    music_mode: int
    sensitivity: int = Field(..., ge=0, le=100)
    auto_color: Optional[int] = Field(None, ge=0, le=1)
    r: Optional[int] = Field(None, ge=0, le=255)
    g: Optional[int] = Field(None, ge=0, le=255)
    b: Optional[int] = Field(None, ge=0, le=255)


class WorkModeCommand(BaseModel):
    device: str
    sku: str
    work_mode: int
    mode_value: int


class RangeCommand(BaseModel):
    device: str
    sku: str
    instance: str
    value: int


class GenericCapabilityCommand(BaseModel):
    device: str
    sku: str
    capability_type: str
    instance: str
    value: Any


class CanvasPixel(BaseModel):
    segment: int
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)


class CanvasDrawCommand(BaseModel):
    device: str
    sku: str
    pixels: List[CanvasPixel]


class CanvasFillCommand(BaseModel):
    device: str
    sku: str
    segments: List[int]
    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)


class CanvasClearCommand(BaseModel):
    device: str
    sku: str