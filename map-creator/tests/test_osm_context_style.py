import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.transforms import Bbox

from guide_maps.rendering import osm_context_style as style
from guide_maps.rendering.osm_context_map_template import (
    LEGEND_WIDTH,
    MAP_WIDTH,
    ContextMapSpec,
    _create_context_axes,
    add_title as add_context_title,
)


def test_index_uses_square_text_boxes_not_colored_map_markers():
    fig, ax = plt.subplots(figsize=(4, 3))
    spots = [
        style.Spot("a", "A", 31.0, 121.0, "coffee", "addr A"),
        style.Spot("b", "B", 31.1, 121.1, "bar", "addr B"),
    ]

    style.add_index(ax, spots, fonts={})

    number_labels = [text for text in ax.texts if text.get_text() in {"01", "02"}]
    assert [text.get_text() for text in number_labels] == ["01", "02"]

    for label in number_labels:
        bbox = label.get_bbox_patch()
        assert bbox is not None
        assert "Square" in type(bbox.get_boxstyle()).__name__
        assert "Circle" not in type(bbox.get_boxstyle()).__name__
        assert mcolors.to_hex(bbox.get_facecolor()).lower() == style.THEME["panel"].lower()
        assert mcolors.to_hex(bbox.get_edgecolor()).lower() != style.CATEGORY_COLORS["coffee"].lower()
        assert mcolors.to_hex(bbox.get_edgecolor()).lower() != style.CATEGORY_COLORS["bar"].lower()

    first_number = next(text for text in ax.texts if text.get_text() == "01")
    first_name = next(text for text in ax.texts if text.get_text() == "A")
    first_note = next(text for text in ax.texts if text.get_text() == "addr A")
    second_number = next(text for text in ax.texts if text.get_text() == "02")
    second_name = next(text for text in ax.texts if text.get_text() == "B")
    second_note = next(text for text in ax.texts if text.get_text() == "addr B")

    marker_text_gap = first_name.get_position()[0] - first_number.get_position()[0]
    assert 0.037 <= marker_text_gap <= 0.041
    assert abs(first_name.get_position()[1] - first_number.get_position()[1]) <= 0.002
    name_note_gap = first_name.get_position()[1] - first_note.get_position()[1]
    assert 0.028 <= name_note_gap <= 0.034
    assert first_number.get_position()[1] - second_number.get_position()[1] >= 0.086

    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    first_number_box = first_number.get_bbox_patch().get_window_extent(renderer)
    first_item_box = Bbox.union(
        [
            first_number_box,
            first_name.get_window_extent(renderer),
            first_note.get_window_extent(renderer),
        ]
    )
    second_item_box = Bbox.union(
        [
            second_number.get_bbox_patch().get_window_extent(renderer),
            second_name.get_window_extent(renderer),
            second_note.get_window_extent(renderer),
        ]
    )
    first_name_box = first_name.get_window_extent(renderer)
    horizontal_px_gap = first_name_box.x0 - first_number_box.x1
    assert 1 <= horizontal_px_gap <= 6
    assert not first_number_box.overlaps(first_name_box)
    assert not first_number_box.overlaps(first_note.get_window_extent(renderer))
    assert not first_item_box.overlaps(second_item_box)

    plt.close(fig)


def test_context_map_title_does_not_render_subtitle():
    fig, ax = plt.subplots(figsize=(4, 3))
    spec = ContextMapSpec(
        title="Changning Industrial Memory Map",
        subtitle="This subtitle should not render",
        output_name="unused.png",
        spots=[],
        road_labels=[],
        area_labels=[],
    )

    add_context_title(ax, spec, fonts={})

    labels = [text.get_text() for text in ax.texts]
    assert any(label.replace("\n", "") == "Changning Industrial Memory Map" for label in labels)
    assert "This subtitle should not render" not in labels

    plt.close(fig)


def test_context_axes_reserve_left_legend_without_map_background():
    fig = plt.figure(figsize=(16, 9))

    legend_ax, map_ax = _create_context_axes(fig)

    assert legend_ax.get_position().bounds == (0.0, 0.0, LEGEND_WIDTH, 1.0)
    assert map_ax.get_position().bounds == (LEGEND_WIDTH, 0.0, MAP_WIDTH, 1.0)
    assert legend_ax.get_xlim() == (0.0, 1.0)
    assert legend_ax.get_ylim() == (0.0, 1.0)
    assert len(legend_ax.collections) == 0
    assert len(legend_ax.images) == 0

    plt.close(fig)
