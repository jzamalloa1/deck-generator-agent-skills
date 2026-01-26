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
    research_data: str = None,
) -> dict:
    """Create a PowerPoint presentation with optional research-enriched content.

    This function is called by the tool wrapper but its implementation
    stays outside the agent's context.

    Args:
        topic: Main topic/subject of the presentation
        num_slides: Number of content slides (excluding title)
        include_title_slide: Whether to include a title slide
        output_dir: Directory to save the file
        research_data: Optional research findings to incorporate into slides

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
            subtitle_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
            if research_data:
                subtitle_text += " | Research-Enhanced Presentation"
            subtitle.text = subtitle_text

        # Add content slides
        bullet_slide_layout = prs.slide_layouts[1]

        # If research data is provided, add a research findings slide first
        if research_data:
            slide = prs.slides.add_slide(bullet_slide_layout)
            shapes = slide.shapes
            title_shape = shapes.title
            title_shape.text = "Key Research Findings"

            body_shape = shapes.placeholders[1]
            text_frame = body_shape.text_frame

            # Parse research data into bullet points
            # Simple parsing: split by newlines and filter
            research_lines = [line.strip() for line in research_data.split('\n') if line.strip() and not line.strip().startswith('#')]

            if research_lines:
                text_frame.text = research_lines[0]
                for line in research_lines[1:8]:  # Limit to 8 bullets to avoid overcrowding
                    if line and line != '**' and not line.startswith('**'):
                        p = text_frame.add_paragraph()
                        # Clean up markdown-style formatting
                        clean_line = line.replace('**', '').replace('- ', '').replace('* ', '')
                        p.text = clean_line
                        p.level = 0 if line.startswith('-') or line.startswith('*') else 1
            else:
                text_frame.text = "Research findings incorporated throughout presentation"

        # Parse research data into usable bullets for content slides
        research_bullets = []
        if research_data:
            # Extract all meaningful bullet points from research data
            # Split by lines and filter for actual content
            lines = research_data.split('\n')

            for line in lines:
                line = line.strip()

                # Skip empty lines, headers, and URLs
                if not line or line.startswith('#') or line.startswith('http'):
                    continue

                # Skip section markers
                if line.startswith('**') or line.endswith('**'):
                    continue

                # Clean up markdown bullet markers
                cleaned = line
                for marker in ['- ', '* ', '• ']:
                    if cleaned.startswith(marker):
                        cleaned = cleaned[len(marker):]

                cleaned = cleaned.strip()

                # Only keep substantial content (not section headers, not URLs)
                if (len(cleaned) > 15 and
                    not cleaned.lower().startswith(('key findings', 'visual suggestions', 'sources', 'key insight')) and
                    not cleaned.startswith('http') and
                    ':' not in cleaned[:30]):  # Likely a data point, not a header
                    research_bullets.append(cleaned)

        # Add regular content slides
        for i in range(1, num_slides + 1):
            slide = prs.slides.add_slide(bullet_slide_layout)
            shapes = slide.shapes

            # Set title
            title_shape = shapes.title
            title_shape.text = f"{topic} - Point {i}"

            # Add content
            body_shape = shapes.placeholders[1]
            text_frame = body_shape.text_frame

            if research_data and research_bullets:
                # Distribute research bullets across slides
                # Calculate which bullets go on this slide (distribute evenly)
                bullets_per_slide = max(3, len(research_bullets) // num_slides)
                start_idx = (i - 1) * bullets_per_slide
                end_idx = min(start_idx + bullets_per_slide, len(research_bullets))

                slide_bullets = research_bullets[start_idx:end_idx]

                if slide_bullets:
                    # Add first bullet as main text
                    text_frame.text = slide_bullets[0]
                    # Add remaining bullets as paragraphs
                    for bullet in slide_bullets[1:]:
                        p = text_frame.add_paragraph()
                        p.text = bullet
                        p.level = 0
                else:
                    # Fallback if no bullets for this slide
                    text_frame.text = f"Additional insights related to {topic}"
            else:
                # No research data - use generic content
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
