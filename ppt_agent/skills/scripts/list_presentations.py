"""Presentation listing script - executed outside agent context.

This script lists PowerPoint files. Its implementation stays outside
the agent's context window (progressive disclosure).
"""

import os


def list_presentations(output_dir: str = "./output") -> dict:
    """List all PowerPoint presentations in the output directory.

    This function is called by the tool wrapper but its implementation
    stays outside the agent's context.

    Args:
        output_dir: Directory to search for presentations

    Returns:
        Dictionary with success status and list of presentations
    """
    try:
        if not os.path.exists(output_dir):
            return {
                "success": False,
                "error": f"Output directory does not exist: {output_dir}",
                "presentations": [],
                "message": f"Output directory does not exist: {output_dir}",
            }

        pptx_files = [f for f in os.listdir(output_dir) if f.endswith(".pptx")]

        if not pptx_files:
            return {
                "success": True,
                "presentations": [],
                "message": f"No PowerPoint presentations found in {output_dir}",
            }

        presentations = []
        for filename in sorted(pptx_files):
            filepath = os.path.join(output_dir, filename)
            size_kb = os.path.getsize(filepath) / 1024
            presentations.append(
                {"filename": filename, "size_kb": round(size_kb, 1), "path": filepath}
            )

        result_message = f"Found {len(pptx_files)} presentation(s) in {output_dir}:\n"
        for i, pres in enumerate(presentations, 1):
            result_message += f"\n{i}. {pres['filename']} ({pres['size_kb']} KB)"

        return {
            "success": True,
            "presentations": presentations,
            "count": len(presentations),
            "message": result_message,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "presentations": [],
            "message": f"Error listing presentations: {str(e)}",
        }
