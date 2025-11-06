# MigratedSLGLNMNodes - Advanced ComfyUI Diffusion Sampling

- NO ASSUMPTIONS - verify everything
- NO EMOJIS - keep communication professional
- TELEGRAPH UNCERTAINTY - tell user when confidence is low
- USE TOOLS - smolagents, comfy-get, Gemini (in that order)
- FOLLOW PRINCIPLES - all 8 design principles, every time
- STAY GROUNDED - reality over theory, empirical over speculative

User interaction:
Do not hype me up. Do not lie or misslead the me down paths you are capable of forseeing the negative results of. Be honest.
 I do not care about flattery or praise. I am not an expert, so there is no need to try to make me feel like one. I am ONLY interested in factual, empirical truths about any matter; you must align with this. You are not allowed to assume that, when you are interacting with this workspace, the tiniest hint of doubt is to be dispelled by using the smolagents to search the comfyui source code or query Gemini. So base your answers in FACTS, not fiction. Keep answers short, straight to the point, and meaningful. Draw lines between relatable concepts, and look holistically at what we are doing to identify the essentials in that respect, using the kinds of code and concepts we are currently exploring.

## Project Overview

This repository contains custom ComfyUI nodes focused on advanced diffusion sampling techniques, including:
- Model sampling implementations (Flux Dev, WAN22, SDXL)
- Custom schedulers with resolution-aware scaling
- Tiled samplers for high-resolution generation
- Advanced noise injection and temporal convergence
- Differential diffusion and region-based sampling

**Reference Documentation**: See `comfyui adv context/` for detailed ComfyUI node development patterns.

---

## Available Tools & Resources

### Local File Operations (Smolagents)
You have access to smolagents for comprehensive file operations:
- **Search**: Search through local and workspace files
- **Read**: Read file contents with line ranges
- **Write**: Create new files or overwrite existing
- **Modify**: Copy, rename, move files
- **Delete**: Remove files or directories
- **Navigate**: Browse directory structures

### ComfyUI Source Code Access
When concepts or implementations are unclear, search the local ComfyUI source:
- **Path**: `D:\pinokio\api\comfy.git\app`
- **Key files**: 
  - `comfy/model_sampling.py` - Model sampling implementations
  - `comfy/samplers.py` - Sampling algorithms
  - `comfy/sample.py` - Core sampling loop
  - `comfy/model_patcher.py` - Model patching system
  - `nodes.py` - Standard node implementations

### Python Environment
- **Location**: `D:\pinokio\api\comfy.git\app\env\Scripts`
- This is the active Python environment for ComfyUI operations

### External Resources
- **comfy-get**: Search GitHub repositories for ComfyUI-related code
- **Gemini**: Query with SHORT, TARGETED questions when local context is insufficient

---

## Model Sampling Specifications

### Core Concept
**Model Sampling** = Mathematical formula mapping timesteps (t) to noise levels (sigma)  
**Scheduler** = Algorithm generating timestep sequences (which points to sample on the curve)

### Model Formulas

**Flux Dev**:
```python
# ModelSamplingFlux
sigma(t) = exp(μ) / (exp(μ) + (1/t - 1))
shift = 1.15  # Official default
range = [0, 1.0]
training_res = 1024x1024
# Gentle curve, balanced detail
```

**WAN22**:
```python
# ModelSamplingDiscreteFlow
sigma(t) = α * t / (1 + (α - 1) * t)
shift = 8.0  # Official default
range = [0, ~1.143]
channels = 16  # vs 4 for SD/Flux
# Steep curve, extreme sharpness, excellent for img2img
```

**SDXL**:
```python
# ModelSamplingDiscrete
# Beta schedule (piecewise linear)
shift = varies by model
range = [0, 14.6]
```

### Key Functions (helpers.py)
```python
def flux_time_shift(mu: float, sigma_param: float, t):
    return math.exp(mu) / (math.exp(mu) + (1 / t - 1) ** sigma_param)

def time_snr_shift(alpha: float, t: float):
    if alpha == 1.0:
        return t
    return alpha * t / (1 + (alpha - 1) * t)
```

---

## ComfyUI Node Structure

### Standard Node Pattern
```python
class MyCustomNode:
    # Required class attributes
    CATEGORY = "sampling/advanced/SMMD"  # Organization in menu
    FUNCTION = "execute"                  # Method name to call
    RETURN_TYPES = ("LATENT", "FLOAT")   # Output types
    RETURN_NAMES = ("latent", "sigma")   # Output labels (optional)
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "latent": ("LATENT",),
                "steps": ("INT", {"default": 20, "min": 1, "max": 1000}),
            },
            "optional": {
                "seed": ("INT", {"default": 0}),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",  # For node tracking
            }
        }
    
    def execute(self, model, latent, steps, seed=None, unique_id=None):
        # Implementation
        return (processed_latent, final_sigma)

# Registration
NODE_CLASS_MAPPINGS = {
    "SMMDCustomNode": MyCustomNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SMMDCustomNode": "SMMD Custom Node"
}
```

### Input Type Reference
- **MODEL**: Diffusion model
- **LATENT**: {"samples": tensor} dictionary
- **CONDITIONING**: Text conditioning
- **IMAGE**: BHWC tensor (batch, height, width, channels)
- **MASK**: Single-channel image
- **FLOAT**, **INT**, **STRING**: Primitive types

---

## Coding Standards & Behavior

### NO ASSUMPTIONS RULE
All code and answers must be rooted in REALITY, not theory.

**When confidence is low**:
1. STOP and telegraph uncertainty to user
2. Use smolagents to search local ComfyUI source
3. Use comfy-get to search GitHub if local search insufficient
4. Query Gemini with SHORT, TARGETED questions as last resort
5. Provide factual, empirical solutions only

**Never**:
- Make theoretical guesses about ComfyUI internals
- Assume API behavior without verification
- Provide untested code patterns
- Use emojis in chat or code

### Design Principles (Priority Order)

#### 1. Cohesion & Single Responsibility
- Each class/function has ONE purpose
- Separate node logic: processing vs UI definition vs validation
- Split large functions into focused helpers
```python
# GOOD: Single responsibility
def calculate_optimal_sigmas(steps, model_type, resolution):
    base_schedule = generate_base_schedule(steps, model_type)
    adjusted = apply_resolution_scaling(base_schedule, resolution)
    return adjusted

# BAD: Mega-function doing everything
def process_everything(model, latent, steps, resolution, ...):
    # 200 lines of mixed concerns
```

#### 2. Encapsulation & Abstraction
- Hide implementation details
- Expose clean interfaces through node inputs/outputs
- Use private methods (prefix with `_`) for internals
```python
class SMMDScheduler:
    def generate_schedule(self, steps, shift):
        """Public interface"""
        return self._calculate_sigmas(steps, shift)
    
    def _calculate_sigmas(self, steps, shift):
        """Private implementation"""
        # Internal logic
```

#### 3. Loose Coupling & Modularity
- Never hardcode dependencies (paths, models, services)
- Support dynamic component swapping
```python
# GOOD: Dependency injection
def apply_sampling(model, sampler_func, scheduler_func, **kwargs):
    sigmas = scheduler_func(**kwargs)
    return sampler_func(model, sigmas=sigmas)

# BAD: Hardcoded coupling
def apply_sampling(model, steps):
    sigmas = flux_time_shift(1.15, 1.0, steps)  # Locked to Flux
```

#### 4. Reusability & Extensibility
- Write functions usable across multiple nodes
- Use base classes for shared behavior
- Add features via subclassing, not rewriting
```python
# Reusable utility
def convert_sigma_to_timestep(model_sampling, sigma):
    return model_sampling.timestep(sigma)

# Extensible base
class BaseSMMDSampler:
    def prepare_latent(self, latent):
        # Common logic
        pass
    
    def sample_step(self, *args):
        raise NotImplementedError  # Override in subclass
```

#### 5. Portability
- Work across Windows, Linux, macOS
- Use `pathlib` and `os.path` for paths
- Never hardcode absolute paths
```python
import os
from pathlib import Path
import folder_paths  # ComfyUI's path manager

# GOOD: Portable
model_dir = folder_paths.get_folder_paths("checkpoints")[0]
config_path = Path(__file__).parent / "configs" / "default.yaml"

# BAD: Hardcoded Windows path
model_dir = "D:\\models\\checkpoints"
```

#### 6. Defensibility
- Validate ALL inputs
- Set safe defaults
- Never allow invalid states
- Log warnings, raise meaningful exceptions
```python
def execute(self, model, steps, cfg_scale=7.0):
    # Validate inputs
    if steps < 1 or steps > 1000:
        raise ValueError(f"Steps must be 1-1000, got {steps}")
    
    if cfg_scale < 1.0:
        logging.warning(f"CFG scale {cfg_scale} < 1.0, clamping to 1.0")
        cfg_scale = 1.0
    
    # Safe processing
    ...
```

#### 7. Maintainability & Testability
- Write isolated, small functions
- Minimize side effects (global state, disk writes)
- Support unit testing
- Clear input/output contracts
```python
# Testable: Pure function
def calculate_skew_from_resolution(width, height, base_res=1024):
    megapixels = (width * height) / (base_res ** 2)
    return math.log2(megapixels) * 0.1

# Not testable: Side effects
def calculate_skew(width, height):
    global last_skew
    last_skew = some_complex_calculation()
    save_to_disk(last_skew)
    return last_skew
```

#### 8. Simplicity
- **KISS**: Keep It Simple, Stupid
- **DRY**: Don't Repeat Yourself
- **YAGNI**: You Aren't Gonna Need It
- Avoid over-engineering
- Clarity over cleverness

```python
# GOOD: Simple and clear
def clamp(value, min_val, max_val):
    return max(min_val, min(max_val, value))

# BAD: Over-engineered
def clamp(value, min_val, max_val):
    return sorted([min_val, value, max_val])[1]
```

---

## Common Patterns

### Model Sampling Adaptation
```python
# Get model's sampling configuration
model_sampling = model.model.model_sampling

# Access shift parameter
if hasattr(model_sampling, 'shift'):
    shift = model_sampling.shift
elif hasattr(model_sampling, 'sampling_settings'):
    shift = model_sampling.sampling_settings.get('shift', 1.0)

# Convert between sigma and timestep
sigma = model_sampling.sigma(timestep)
timestep = model_sampling.timestep(sigma)
```

### Resolution-Aware Scheduling
```python
def calculate_resolution_skew(width, height, base_res=1024):
    """Calculate skew adjustment based on image resolution"""
    actual_mp = (width * height) / 1e6
    base_mp = (base_res ** 2) / 1e6
    mp_ratio = actual_mp / base_mp
    
    # Logarithmic scaling for smooth adjustment
    skew = math.log2(mp_ratio) * 0.1
    return skew
```

### Tiled Sampling Overlap
```python
def calculate_tile_overlap(tile_size, overlap_percent=0.125):
    """Standard 12.5% overlap for smooth blending"""
    overlap = int(tile_size * overlap_percent)
    # Ensure even number for symmetric blending
    return overlap if overlap % 2 == 0 else overlap + 1
```

### Sigma Schedule Validation
```python
def validate_sigma_schedule(sigmas):
    """Ensure sigmas are monotonically decreasing"""
    if len(sigmas) < 2:
        raise ValueError("Schedule must have at least 2 sigmas")
    
    for i in range(len(sigmas) - 1):
        if sigmas[i] <= sigmas[i + 1]:
            raise ValueError(f"Sigmas not decreasing at index {i}")
    
    if sigmas[-1] != 0.0:
        logging.warning(f"Final sigma {sigmas[-1]} != 0, may cause artifacts")
```

---

## Naming Conventions

### Node Classes
- Prefix: `SMMD` (Stable Mega Mega Diffusion)
- Version suffix: `V9`, `V10`, etc.
- Example: `SMMDTileSamplerV9`, `SMMDSchedulerV10`

### Helper Functions
- Descriptive, verb-based names
- Include units in parameter names when relevant
```python
def generate_sigmas_flux(steps, shift=1.15, denoise_strength=1.0):
    """Generate sigma schedule for Flux models"""
    pass

def calculate_tile_coords_with_overlap(image_width, image_height, tile_size, overlap_pixels):
    """Calculate tile coordinates with specified overlap"""
    pass
```

### Constants
- UPPER_CASE for module-level constants
- Descriptive names, avoid magic numbers
```python
DEFAULT_FLUX_SHIFT = 1.15
DEFAULT_WAN_SHIFT = 8.0
DEFAULT_TILE_SIZE = 512
DEFAULT_OVERLAP_RATIO = 0.125
MIN_STEPS = 1
MAX_STEPS = 1000
```

---

## Documentation Requirements

### Node Docstrings
```python
class SMMDCustomNode:
    """
    Brief one-line description.
    
    This node performs [specific function] for [use case].
    Supports [key features].
    
    Inputs:
        model: Diffusion model (Flux/WAN/SDXL)
        steps: Number of sampling steps (1-1000)
        shift: Shift parameter (default varies by model)
    
    Outputs:
        latent: Processed latent tensor
        sigmas: Generated sigma schedule
    
    Notes:
        - Uses resolution-aware scheduling
        - Automatically detects model type
        - See Model_Sampling_Context.md for theory
    """
```

### Function Docstrings
```python
def flux_time_shift(mu: float, sigma_param: float, t):
    """
    Calculate Flux rectified flow timestep mapping.
    
    Args:
        mu: Shift parameter (typically 1.15 for Flux Dev)
        sigma_param: Sigma exponent (typically 1.0)
        t: Normalized timestep in [0, 1]
    
    Returns:
        Shifted sigma value
    
    Formula:
        sigma(t) = exp(μ) / (exp(μ) + (1/t - 1)^σ)
    
    Reference:
        https://arxiv.org/abs/2403.03206 (Flux paper)
    """
```

---

## Error Handling

### Input Validation
```python
def execute(self, model, latent, steps, cfg_scale):
    # Type validation
    if not isinstance(steps, int):
        raise TypeError(f"steps must be int, got {type(steps)}")
    
    # Range validation
    if not (1 <= steps <= 1000):
        raise ValueError(f"steps must be 1-1000, got {steps}")
    
    # Tensor validation
    if "samples" not in latent:
        raise KeyError("latent dict missing 'samples' key")
    
    samples = latent["samples"]
    if samples.dim() != 4:
        raise ValueError(f"latent samples must be 4D (BCHW), got {samples.dim()}D")
```

### Graceful Degradation
```python
def detect_model_type(model):
    """Detect model type with fallback to safe default"""
    try:
        if hasattr(model.model, 'model_sampling'):
            sampling = model.model.model_sampling
            if 'Flux' in sampling.__class__.__name__:
                return 'flux', 1.15
            elif 'DiscreteFlow' in sampling.__class__.__name__:
                return 'wan', 8.0
    except AttributeError as e:
        logging.warning(f"Could not detect model type: {e}, using SDXL default")
    
    return 'sdxl', 3.0  # Safe fallback
```

---

## Performance Considerations

### Memory Management
```python
import torch

def process_tiles(image, tile_size):
    """Process tiles with proper memory cleanup"""
    tiles = split_into_tiles(image, tile_size)
    results = []
    
    for tile in tiles:
        result = process_single_tile(tile)
        results.append(result)
        
        # Clear intermediate tensors
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    
    return merge_tiles(results)
```

### Device Handling
```python
def execute(self, model, latent, ...):
    # Get device from input tensors
    device = latent["samples"].device
    dtype = latent["samples"].dtype
    
    # Create new tensors on same device
    noise = torch.randn_like(latent["samples"], device=device, dtype=dtype)
    
    # Never hardcode device
    # BAD: tensor.to("cuda")
    # GOOD: tensor.to(device)
```

---

## Testing & Validation

### Smoke Tests
Create simple scripts in `scripts/` for quick validation:
```python
# scripts/smoke_import_my_node.py
import sys
sys.path.insert(0, "D:/pinokio/api/comfy.git/app")

try:
    from MigratedSLGLNMNodes.my_node import MyCustomNode
    print("IMPORT_OK")
    
    # Quick instantiation test
    node = MyCustomNode()
    print("INSTANTIATION_OK")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
```

### Unit Tests
```python
def test_calculate_skew():
    # Test base resolution
    assert calculate_skew_from_resolution(1024, 1024) == 0.0
    
    # Test 4x resolution (4MP vs 1MP)
    assert abs(calculate_skew_from_resolution(2048, 2048) - 0.2) < 0.01
    
    # Test rectangular images
    skew_rect = calculate_skew_from_resolution(2048, 1024)
    assert skew_rect == calculate_skew_from_resolution(1024, 2048)
```

---

## Key Files Reference

### Documentation
- `Docs/Model_Sampling_Context.md` - Comprehensive model sampling theory and practice
- `Docs/MODEL_DETECTION_v10_1.md` - Model type detection and compatibility
- `comfyui adv context/` - ComfyUI node development patterns

### Core Implementations
- `helpers.py` - Shared utility functions (flux_time_shift, time_snr_shift)
- `tile_sampler_v10.py` - Latest tiled sampling implementation
- `flux_scheduler_v5.py` - Flux-specific scheduler
- `sampling_helper_v2.py` - Sampling utilities and wrappers

### Node Versions
- V10: Current stable (tiled sampler)
- V9: Legacy support
- V8: Deprecated (reference only)

---

## Example Workflow

When implementing a new feature:

1. **Research** (if needed)
   - Search local ComfyUI source: `D:\pinokio\api\comfy.git\app`
   - Check existing patterns in this repo
   - Query Gemini for specific questions (SHORT, TARGETED)

2. **Design**
   - Apply 8 design principles
   - Define clear input/output contract
   - Identify reusable components

3. **Implement**
   - Follow node structure template
   - Use defensive validation
   - Write docstrings

4. **Test**
   - Create smoke test script
   - Test with actual ComfyUI workflow
   - Verify tensor shapes and devices

5. **Document**
   - Add docstrings to all public functions
   - Update relevant docs if theory changes
   - Add examples to `10_examples.md` if applicable

---

For detailed ComfyUI node patterns, see `comfyui adv context/00_index.md` and subsequent guides.
