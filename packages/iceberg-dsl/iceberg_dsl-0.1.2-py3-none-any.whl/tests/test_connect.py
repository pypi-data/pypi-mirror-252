import iceberg as ice
from .scene_tester import check_render
import os


def test_connect():
    # What font?
    _CIRCLE_WIDTH = 100
    _BORDER_THICKNESS = 8
    _CIRCLE_PAD = 20

    left_ellipse = ice.Ellipse(
        rectangle=ice.Bounds(size=(_CIRCLE_WIDTH, _CIRCLE_WIDTH)),
        border_color=ice.Color.from_hex("#d63031"),
        border_thickness=_BORDER_THICKNESS,
        fill_color=ice.Color.from_hex("#ff7675"),
    ).pad(_CIRCLE_PAD)

    right_ellipse = ice.Ellipse(
        rectangle=ice.Bounds(size=(_CIRCLE_WIDTH, _CIRCLE_WIDTH)),
        border_color=ice.Color.from_hex("#0984e3"),
        border_thickness=_BORDER_THICKNESS,
        fill_color=ice.Color.from_hex("#74b9ff"),
    ).pad(_CIRCLE_PAD)

    ellipses = ice.Arrange(
        [left_ellipse, right_ellipse],
        gap=500,
    )

    with ellipses:
        # Within this context, we can use `relative_bounds` to get the bounds of the
        # `left_ellipse` and `right_ellipse` relative to the `ellipses` object.
        arrow = ice.Arrow(
            left_ellipse.relative_bounds.corners[ice.Corner.MIDDLE_RIGHT],
            right_ellipse.relative_bounds.corners[ice.Corner.MIDDLE_LEFT],
            line_path_style=ice.PathStyle(
                color=ice.Colors.BLACK,
                thickness=3,
            ),
        )

    arrow_label = ice.MathTex("f(x) = x^2", svg_scale=4)
    arrow = ice.LabelArrow(
        arrow=arrow,
        child=arrow_label,
        child_corner=ice.Corner.BOTTOM_MIDDLE,
        distance=20,
    )
    connection = ice.Compose([ellipses, arrow])

    text_block = ice.Text(
        "This is some really long text, and it's going to wrap around at some point, because it's so long and I spent a lot of time.",
        font_style=ice.FontStyle(
            filename=os.path.join("tests", "testdata", "OpenSans-Regular.ttf"),
            size=28,
            color=ice.Colors.BLACK,
        ),
        width=connection.bounds.width,
    )

    scene = ice.Arrange(
        [connection, text_block],
        gap=10,
        arrange_direction=ice.Arrange.Direction.VERTICAL,
    )

    scene = scene.pad(20).scale(2)

    check_render(scene, "connect.png")
