# Running the MRHead Threshold Script in 3D Slicer

## Where to run it
You can run `mrhead_threshold_to_model.py` in either:
1. **Python Interactor** (fastest for this sample), or
2. A custom **Scripted Module** environment if you are building a module.

For beginners, use **Python Interactor**.

## Python Interactor steps
1. Open 3D Slicer.
2. Go to **View → Python Interactor**.
3. Run:
   ```python
   exec(open(r"/absolute/path/to/scripts/mrhead_threshold_to_model.py", encoding="utf-8").read())
   ```
4. Watch the Python console for `[INFO]` logs.
5. Check outputs in:
   - `outputs/mrhead_threshold_demo/MRHeadSegmentation.seg.nrrd`
   - `outputs/mrhead_threshold_demo/MRHeadModel.stl`

## Expected outputs
- **Scene changes:**
  - Loaded `MRHead` volume.
  - New segmentation node: `MRHeadSegmentation`.
  - One threshold-generated segment.
  - Exported model node(s) visible in 3D view.
- **Saved files:**
  - `.seg.nrrd` segmentation file.
  - `.stl` model file.

## Troubleshooting
- **No visible segmentation/model:**
  - Threshold range may be too strict for your target anatomy; try lower minimum or higher maximum.
- **Script can’t find file path:**
  - Ensure the absolute path in `exec(open(...))` is correct.
- **Save failures:**
  - Confirm you have write permission to the repository folder.
- **Slow first run:**
  - Initial sample-data fetch and module initialization can take extra time.

## Optional parameter tweaks
Edit these values in `mrhead_threshold_to_model.py`:
- `LOWER_THRESHOLD`
- `UPPER_THRESHOLD`
- `SEGMENT_NAME`
- `OUTPUT_SUBFOLDER`
