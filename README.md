# 3D Slicer Work Sample Portfolio

**3D Slicer** is a free, open-source platform for medical image informatics, visualization, and image-guided intervention research.  
It supports DICOM and many imaging workflows, including segmentation and 3D model generation.

## Quick project plan (dataset + approach)
For a reliable, no-download demo, I used **3D Slicer Sample Data -> MRHead** and built a simple **threshold-based segmentation** workflow.  
The script creates one segment from intensity thresholding, then exports a **3D model** and saves both the segmentation and model files locally.  
This keeps the sample beginner-friendly while showing practical Slicer automation.

## What I did
- Loaded MRHead from **Sample Data** (public, de-identified sample bundled via Slicer).
- Created a new segmentation node linked to the loaded volume.
- Applied a simple threshold effect to generate a segment.
- Converted/exported segmentation content to a 3D model.
- Saved outputs to a local folder for reproducibility.
- Documented manual steps, script execution, and troubleshooting.

## Datasets used
- **Primary (scripted):** Slicer Sample Data -> `MRHead` (required).
- **Optional manual walkthrough:** Slicer Sample Data -> `CTChest` (optional, not required for script).

> No PHI/PII is included in this repository. Use only public/de-identified sample data.

## Folder structure

```text
.
├── README.md
├── notes/
│   └── worklog.md
├── screenshots/
│   ├── 01-sample-data-mrhead.png
│   ├── 02-threshold-segmentation.png
│   ├── 03-3d-model-view.png
│   └── 04-saved-files.png
└── scripts/
    ├── mrhead_threshold_to_model.py
    └── RUN.md
```

## Reproduce the sample (manual click-by-click)

1. Open **3D Slicer**.
2. Go to **Sample Data** module.
3. Click **MRHead** to load the sample volume.
4. Open **Segment Editor**.
5. Click **Add** to create a new segment.
6. Select **Threshold** effect.
7. Adjust threshold range so major head structures are selected (example start: lower `500`, upper `2000`; tune visually).
8. Click **Apply**.
9. Click **Show 3D** to generate/display the 3D surface.
10. (Optional) Open **Segmentations** module and export segment(s) to model(s).
11. Save scene/data via **File -> Save**.

## Reproduce the sample (script)

1. Start 3D Slicer.
2. Open **View -> Python Interactor**.
3. Run:
   ```python
   exec(open(r"/absolute/path/to/scripts/mrhead_threshold_to_model.py", encoding="utf-8").read())
   ```
4. Check generated files in `outputs/mrhead_threshold_demo/`.

See `scripts/RUN.md` for details.

## Screenshots checklist
Place screenshots in `/screenshots` using these filenames:
- `01-sample-data-mrhead.png` — MRHead loaded in slice viewers.
- `02-threshold-segmentation.png` — Segment Editor threshold settings and result.
- `03-3d-model-view.png` — 3D view with segmentation/model visible.
- `04-saved-files.png` — File browser showing saved `.seg.nrrd` and `.stl` outputs.

## What I learned
- How to move from sample volume loading -> segmentation -> 3D model export in Slicer.
- Basic Slicer Python automation patterns (`SampleData`, `SegmentEditor`, save/export logic).

## Next steps
- Add multi-segment workflow (e.g., bone + soft tissue labels).
- Add quantitative metrics (segment volume/surface area).
- Expand optional CTChest manual walkthrough with comparison notes.
