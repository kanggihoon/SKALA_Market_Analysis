"""
Pipeline Visualization Tool
Generates flowchart diagrams showing the state, nodes, and edges of the SKALA Market Analysis pipeline.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path


def draw_node(ax, x, y, width, height, text, color='#667eea', text_color='white', fontsize=9):
    """Draw a rounded rectangle node"""
    box = FancyBboxPatch(
        (x - width/2, y - height/2), width, height,
        boxstyle="round,pad=0.05",
        facecolor=color,
        edgecolor='#333',
        linewidth=1.5
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, color=text_color, weight='bold',
            wrap=True)


def draw_arrow(ax, x1, y1, x2, y2, style='->', color='#333', linewidth=2):
    """Draw an arrow between two points"""
    arrow = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style,
        color=color,
        linewidth=linewidth,
        mutation_scale=20,
        zorder=0
    )
    ax.add_patch(arrow)


def visualize_state_schema(output_path: str):
    """
    Visualize the State schema and its relationships
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'SKALA Market Analysis - State Schema',
            ha='center', fontsize=18, weight='bold')

    # Central State node
    draw_node(ax, 5, 5, 1.5, 0.8, 'State\n(Pydantic)', color='#e74c3c', fontsize=11)

    # State fields arranged in a circle
    fields = [
        ('input_meta', 2, 8, '#3498db'),
        ('market_summary', 0.5, 6.5, '#2ecc71'),
        ('reg_compliance', 0.5, 4.5, '#f39c12'),
        ('competition', 0.5, 2.5, '#9b59b6'),
        ('gtm_high', 2, 1, '#1abc9c'),
        ('gtm_mid', 4, 0.5, '#1abc9c'),
        ('gtm_low', 6, 0.5, '#1abc9c'),
        ('gtm_merged', 8, 1, '#16a085'),
        ('partners', 9.5, 2.5, '#e67e22'),
        ('risks', 9.5, 4.5, '#c0392b'),
        ('decision', 9.5, 6.5, '#8e44ad'),
        ('artifacts', 8, 8, '#34495e'),
    ]

    for field_name, x, y, color in fields:
        draw_node(ax, x, y, 1.2, 0.6, field_name, color=color, fontsize=8)
        # Draw connection to central State
        draw_arrow(ax, x, y, 5, 5, style='-', color='#95a5a6', linewidth=1)

    # Add legends for field types
    legend_y = 9
    ax.text(0.3, legend_y, 'Field Types:', fontsize=10, weight='bold')
    ax.text(0.3, legend_y - 0.3, '• Input/Output metadata', fontsize=8, color='#3498db')
    ax.text(0.3, legend_y - 0.6, '• Analysis results', fontsize=8, color='#2ecc71')
    ax.text(0.3, legend_y - 0.9, '• Segment cards', fontsize=8, color='#1abc9c')
    ax.text(0.3, legend_y - 1.2, '• Decision data', fontsize=8, color='#8e44ad')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ State schema diagram saved: {output_path}")
    plt.close()


def visualize_phase1_pipeline(output_path: str):
    """
    Visualize Phase1 pipeline flow
    """
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Title
    ax.text(5, 9.5, 'Phase 1 Pipeline - Fast Analysis',
            ha='center', fontsize=18, weight='bold')
    ax.text(5, 9, 'Market Research → Regulation → Decision → Report',
            ha='center', fontsize=11, style='italic', color='#666')

    # Node positions
    nodes = [
        ('START', 5, 8.2, 1.2, 0.5, '#95a5a6'),
        ('Input\nValidation', 5, 7.2, 1.4, 0.6, '#3498db'),
        ('Market\nResearch', 5, 6, 1.4, 0.6, '#2ecc71'),
        ('Regulation\nCheck', 5, 4.8, 1.4, 0.6, '#f39c12'),
        ('Decision\nMaker', 5, 3.6, 1.4, 0.6, '#8e44ad'),
        ('Report\nWriter', 5, 2.4, 1.4, 0.6, '#e74c3c'),
        ('HTML\nReporter', 5, 1.2, 1.4, 0.6, '#d35400'),
        ('END', 5, 0.3, 1.2, 0.5, '#95a5a6'),
    ]

    # Draw nodes
    for i, (name, x, y, w, h, color) in enumerate(nodes):
        draw_node(ax, x, y, w, h, name, color=color)

        # Draw arrows between sequential nodes
        if i < len(nodes) - 1:
            next_y = nodes[i + 1][2]
            draw_arrow(ax, x, y - h/2, x, next_y + nodes[i + 1][4]/2)

    # Add state updates on the right
    state_updates = [
        (7.5, 7.2, 'input_meta'),
        (7.5, 6, 'market_summary'),
        (7.5, 4.8, 'reg_compliance'),
        (7.5, 3.6, 'decision'),
        (7.5, 2.4, 'artifacts'),
        (7.5, 1.2, 'artifacts'),
    ]

    ax.text(7.5, 8, 'State Updates', ha='center', fontsize=10, weight='bold', color='#333')
    for x, y, field in state_updates:
        ax.text(x, y, f'→ {field}', ha='left', fontsize=8,
                color='#666', style='italic')

    # Add timing info
    ax.text(2.5, 8, 'Timing:', fontsize=10, weight='bold')
    ax.text(2.5, 7.7, '~2-5 min', fontsize=9, color='#27ae60')
    ax.text(2.5, 7.4, 'for 3 companies', fontsize=8, color='#666')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Phase1 pipeline diagram saved: {output_path}")
    plt.close()


def visualize_full_pipeline(output_path: str):
    """
    Visualize Full pipeline flow with parallel GTM processing
    """
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 13)
    ax.axis('off')

    # Title
    ax.text(6, 12.5, 'Full Pipeline - Complete Analysis',
            ha='center', fontsize=18, weight='bold')
    ax.text(6, 12, 'All modules with parallel GTM segment processing',
            ha='center', fontsize=11, style='italic', color='#666')

    # Sequential nodes
    sequential = [
        ('START', 6, 11, 1.2, 0.5, '#95a5a6'),
        ('Input\nValidation', 6, 10, 1.4, 0.6, '#3498db'),
        ('Market\nResearch', 6, 9, 1.4, 0.6, '#2ecc71'),
        ('Regulation\nCheck', 6, 8, 1.4, 0.6, '#f39c12'),
        ('Competitor\nMapping', 6, 7, 1.4, 0.6, '#9b59b6'),
    ]

    for i, (name, x, y, w, h, color) in enumerate(sequential):
        draw_node(ax, x, y, w, h, name, color=color)
        if i < len(sequential) - 1:
            next_y = sequential[i + 1][2]
            draw_arrow(ax, x, y - h/2, x, next_y + sequential[i + 1][4]/2)

    # Parallel GTM nodes
    gtm_y = 5.5
    draw_node(ax, 3, gtm_y, 1.4, 0.6, 'GTM\nHigh', color='#1abc9c')
    draw_node(ax, 6, gtm_y, 1.4, 0.6, 'GTM\nMid', color='#1abc9c')
    draw_node(ax, 9, gtm_y, 1.4, 0.6, 'GTM\nLow', color='#1abc9c')

    # Arrows from competitor_mapping to parallel GTM
    draw_arrow(ax, 6, 7 - 0.3, 3, gtm_y + 0.3)
    draw_arrow(ax, 6, 7 - 0.3, 6, gtm_y + 0.3)
    draw_arrow(ax, 6, 7 - 0.3, 9, gtm_y + 0.3)

    # Add parallel indicator
    ax.text(6, 6.2, 'ThreadPoolExecutor', ha='center',
            fontsize=9, style='italic', color='#16a085', weight='bold')
    ax.text(6, 5.9, '(max_workers=3)', ha='center',
            fontsize=8, color='#666')

    # Merge and continue
    merge_y = 4.5
    draw_node(ax, 6, merge_y, 1.4, 0.6, 'GTM\nMerge', color='#16a085')

    # Arrows from parallel GTM to merge
    draw_arrow(ax, 3, gtm_y - 0.3, 6, merge_y + 0.3)
    draw_arrow(ax, 6, gtm_y - 0.3, 6, merge_y + 0.3)
    draw_arrow(ax, 9, gtm_y - 0.3, 6, merge_y + 0.3)

    # Continue sequential
    final_nodes = [
        ('Partner\nSourcing', 6, 3.5, 1.4, 0.6, '#e67e22'),
        ('Risk\nScenarios', 6, 2.5, 1.4, 0.6, '#c0392b'),
        ('Decision\nMaker', 6, 1.5, 1.4, 0.6, '#8e44ad'),
        ('Report\nWriter', 6, 0.8, 1.4, 0.6, '#e74c3c'),
        ('HTML\nReporter', 6, 0.3, 1.4, 0.6, '#d35400'),
    ]

    # Arrow from merge to partner sourcing
    draw_arrow(ax, 6, merge_y - 0.3, 6, final_nodes[0][2] + 0.3)

    for i, (name, x, y, w, h, color) in enumerate(final_nodes):
        draw_node(ax, x, y, w, h, name, color=color)
        if i < len(final_nodes) - 1:
            next_y = final_nodes[i + 1][2]
            draw_arrow(ax, x, y - h/2, x, next_y + final_nodes[i + 1][4]/2)

    # Final reporter (separate, runs after all cases)
    draw_node(ax, 10, 1, 1.4, 0.6, 'Final\nReporter', color='#2c3e50')
    ax.text(10, 0.5, '(All cases)', ha='center', fontsize=7,
            style='italic', color='#666')

    # State updates on the right
    state_updates = [
        (10, 10, 'input_meta', '#3498db'),
        (10, 9, 'market_summary', '#2ecc71'),
        (10, 8, 'reg_compliance', '#f39c12'),
        (10, 7, 'competition', '#9b59b6'),
        (10, 5.5, 'gtm_high/mid/low', '#1abc9c'),
        (10, 4.5, 'gtm_merged', '#16a085'),
        (10, 3.5, 'partners', '#e67e22'),
        (10, 2.5, 'risks', '#c0392b'),
        (10, 1.5, 'decision', '#8e44ad'),
        (10, 0.8, 'artifacts (MD)', '#e74c3c'),
        (10, 0.3, 'artifacts (HTML)', '#d35400'),
    ]

    ax.text(10, 11, 'State Updates', ha='center', fontsize=10,
            weight='bold', color='#333')
    for x, y, field, color in state_updates:
        ax.text(x, y, f'→ {field}', ha='left', fontsize=7,
                color=color, style='italic')

    # Add timing info
    ax.text(2, 11, 'Timing:', fontsize=10, weight='bold')
    ax.text(2, 10.7, '~5-10 min', fontsize=9, color='#27ae60')
    ax.text(2, 10.4, 'for 3 companies', fontsize=8, color='#666')

    # Add loop indicator
    ax.text(2, 9.5, 'Loop:', fontsize=10, weight='bold')
    ax.text(2, 9.2, 'Per company ×', fontsize=8, color='#666')
    ax.text(2, 8.9, 'target countries', fontsize=8, color='#666')

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Full pipeline diagram saved: {output_path}")
    plt.close()


def main():
    """Generate all pipeline visualizations"""
    # Create output directory
    output_dir = Path(__file__).parent.parent / "docs" / "diagrams"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("🎨 Generating pipeline visualizations...")

    # Generate diagrams
    visualize_state_schema(str(output_dir / "01_state_schema.png"))
    visualize_phase1_pipeline(str(output_dir / "02_phase1_pipeline.png"))
    visualize_full_pipeline(str(output_dir / "03_full_pipeline.png"))

    print("\n✅ All diagrams generated successfully!")
    print(f"📁 Output directory: {output_dir}")
    print("\nGenerated files:")
    print("  - 01_state_schema.png: State and field relationships")
    print("  - 02_phase1_pipeline.png: Fast analysis pipeline")
    print("  - 03_full_pipeline.png: Complete pipeline with parallel GTM")


if __name__ == "__main__":
    main()
