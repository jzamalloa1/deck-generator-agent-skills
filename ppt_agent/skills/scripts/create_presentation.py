"""PowerPoint creation script - executed outside agent context.

This script contains the actual implementation logic for creating
PowerPoint presentations. It is called by the tool but its code
never enters the agent's context window (progressive disclosure).
"""

import os
from datetime import datetime
from pptx import Presentation
from pptx.util import Inches


def create_powerpoint(
    topic: str,
    num_slides: int = 5,
    include_title_slide: bool = True,
    output_dir: str = "./output",
) -> dict:
    """Create a PowerPoint presentation.

    This function is called by the tool wrapper but its implementation
    stays outside the agent's context.

    Args:
        topic: Main topic/subject of the presentation
        num_slides: Number of content slides (excluding title)
        include_title_slide: Whether to include a title slide
        output_dir: Directory to save the file

    Returns:
        Dictionary with success status, filepath, and message
    """
    try:
        # Validate inputs
        if num_slides < 1 or num_slides > 20:
            return {
                "success": False,
                "error": "num_slides must be between 1 and 20",
                "filepath": None,
            }

        if not topic or len(topic.strip()) == 0:
            return {
                "success": False,
                "error": "topic cannot be empty",
                "filepath": None,
            }

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Create presentation
        prs = Presentation()
        prs.slide_width = Inches(10)
        prs.slide_height = Inches(7.5)

        # Add title slide
        if include_title_slide:
            title_slide_layout = prs.slide_layouts[0]
            slide = prs.slides.add_slide(title_slide_layout)
            title = slide.shapes.title
            subtitle = slide.placeholders[1]

            title.text = topic
            subtitle.text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"

        # Add content slides
        bullet_slide_layout = prs.slide_layouts[1]

        for i in range(1, num_slides + 1):
            slide = prs.slides.add_slide(bullet_slide_layout)
            shapes = slide.shapes

            # Set title
            title_shape = shapes.title
            title_shape.text = f"{topic} - Point {i}"

            # Add content
            body_shape = shapes.placeholders[1]
            text_frame = body_shape.text_frame
            text_frame.text = f"Key concept {i} related to {topic}"

            # Add bullet points
            for j in range(3):
                p = text_frame.add_paragraph()
                p.text = f"Supporting detail {j + 1} for concept {i}"
                p.level = 1

        # Generate filename
        safe_topic = "".join(c if c.isalnum() or c.isspace() else "_" for c in topic)
        safe_topic = safe_topic.replace(" ", "_")[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_topic}_{timestamp}.pptx"
        filepath = os.path.join(output_dir, filename)

        # Save presentation
        prs.save(filepath)

        total_slides = num_slides + (1 if include_title_slide else 0)

        return {
            "success": True,
            "filepath": filepath,
            "total_slides": total_slides,
            "message": f"PowerPoint presentation created successfully: {filepath} (Total slides: {total_slides})",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "filepath": None,
            "message": f"Error creating PowerPoint presentation: {str(e)}",
        }
