"""
mrhead_threshold_to_model.py

Beginner-friendly 3D Slicer script that:
1) Loads Sample Data (MRHead)
2) Creates a segmentation node
3) Applies threshold-based segmentation
4) Exports a 3D model from the segmentation
5) Saves segmentation + model outputs to a local folder

How to run (inside 3D Slicer):
- Open: View -> Python Interactor
- Run:
    exec(open(r"/absolute/path/to/scripts/mrhead_threshold_to_model.py", encoding="utf-8").read())

Notes:
- Uses only de-identified Slicer Sample Data.
- If threshold values do not produce a useful region, adjust LOWER_THRESHOLD/UPPER_THRESHOLD.
"""

import os

import SampleData
import slicer


# -----------------------------
# Configurable parameters
# -----------------------------
LOWER_THRESHOLD = 500
UPPER_THRESHOLD = 2000
SEGMENT_NAME = "MRHead_Threshold"
OUTPUT_SUBFOLDER = "mrhead_threshold_demo"


def ensure_output_dir():
    """Create output folder under this script's parent directory (/outputs/...)."""
    # When run via exec(open(...).read()), __file__ is not guaranteed.
    # Fallback to current working directory if __file__ is missing.
    script_path = os.path.abspath(__file__) if "__file__" in globals() else os.path.join(os.getcwd(), "scripts", "mrhead_threshold_to_model.py")
    repo_root = os.path.abspath(os.path.join(os.path.dirname(script_path), ".."))
    output_dir = os.path.join(repo_root, "outputs", OUTPUT_SUBFOLDER)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def load_mrhead_volume():
    """Load MRHead from Slicer Sample Data."""
    print("[INFO] Loading MRHead sample volume...")
    volume_node = SampleData.SampleDataLogic().downloadMRHead()
    if not volume_node:
        raise RuntimeError("Failed to load MRHead sample data.")
    print(f"[INFO] Loaded volume node: {volume_node.GetName()}")
    return volume_node


def create_threshold_segmentation(volume_node):
    """Create segmentation and apply threshold effect using Segment Editor."""
    print("[INFO] Creating segmentation node...")
    segmentation_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode", "MRHeadSegmentation")
    segmentation_node.CreateDefaultDisplayNodes()
    segmentation_node.SetReferenceImageGeometryParameterFromVolumeNode(volume_node)

    segment_editor_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
    segment_editor_widget = slicer.qMRMLSegmentEditorWidget()
    segment_editor_widget.setMRMLScene(slicer.mrmlScene)
    segment_editor_widget.setMRMLSegmentEditorNode(segment_editor_node)
    segment_editor_widget.setSegmentationNode(segmentation_node)
    segment_editor_widget.setSourceVolumeNode(volume_node)

    # Add a new segment
    added_segment_id = segmentation_node.GetSegmentation().AddEmptySegment(SEGMENT_NAME)
    segment_editor_node.SetSelectedSegmentID(added_segment_id)

    # Apply threshold effect
    print(f"[INFO] Applying threshold: {LOWER_THRESHOLD} to {UPPER_THRESHOLD}")
    segment_editor_widget.setActiveEffectByName("Threshold")
    effect = segment_editor_widget.activeEffect()
    effect.setParameter("MinimumThreshold", str(LOWER_THRESHOLD))
    effect.setParameter("MaximumThreshold", str(UPPER_THRESHOLD))
    effect.self().onApply()

    # Cleanup editor widget/node
    segment_editor_widget = None
    slicer.mrmlScene.RemoveNode(segment_editor_node)

    print("[INFO] Segmentation created successfully.")
    return segmentation_node


def export_model(segmentation_node):
    """Export all segments as models into a model hierarchy folder node."""
    print("[INFO] Exporting segmentation to model...")
    models_folder_node = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLFolderDisplayNode", "MRHeadModelsFolder")

    success = slicer.modules.segmentations.logic().ExportAllSegmentsToModels(segmentation_node, models_folder_node)
    if not success:
        raise RuntimeError("Failed to export segmentation to model.")

    model_nodes = slicer.util.getNodesByClass("vtkMRMLModelNode")
    if not model_nodes:
        raise RuntimeError("Model export reported success, but no model nodes were found.")

    print(f"[INFO] Exported {len(model_nodes)} model node(s).")
    return model_nodes


def save_outputs(segmentation_node, model_nodes, output_dir):
    """Save segmentation (.seg.nrrd) and first model (.stl)."""
    seg_path = os.path.join(output_dir, "MRHeadSegmentation.seg.nrrd")
    model_path = os.path.join(output_dir, "MRHeadModel.stl")

    print(f"[INFO] Saving segmentation to: {seg_path}")
    if not slicer.util.saveNode(segmentation_node, seg_path):
        raise RuntimeError(f"Failed to save segmentation: {seg_path}")

    print(f"[INFO] Saving model to: {model_path}")
    if not slicer.util.saveNode(model_nodes[0], model_path):
        raise RuntimeError(f"Failed to save model: {model_path}")

    print("[INFO] Saved outputs successfully.")
    print(f"[DONE] Output folder: {output_dir}")


def main():
    output_dir = ensure_output_dir()
    volume_node = load_mrhead_volume()
    segmentation_node = create_threshold_segmentation(volume_node)
    model_nodes = export_model(segmentation_node)
    save_outputs(segmentation_node, model_nodes, output_dir)


main()
