import io

import numpy as np
from PIL import Image as PILImage

from iceberg import DrawableWithChild
from iceberg.primitives.image import Image
from iceberg.primitives.svg import SVG

_MATPLOTLIB_INSTALLED = False

# Check if matplotlib is installed.
try:
    import matplotlib

    _MATPLOTLIB_INSTALLED = True
except ImportError:
    pass


if _MATPLOTLIB_INSTALLED:
    import matplotlib.figure

    class MatplotlibFigure(DrawableWithChild):
        """Import a matplotlib figure as a drawable for iceberg.

        Note, if not using SVG mode, control the dpi of the figure using the
        matplotlib figure's dpi property.

        Args:
            figure: The matplotlib figure to import.
            use_svg: Whether to use svg or png as the intermediate format.
            transparent: Whether to use a transparent background.
        """

        figure: matplotlib.figure.Figure
        use_svg: bool = True
        transparent: bool = False
        filter_quality: Image.ImageFilterQuality = Image.ImageFilterQuality.HIGH

        def setup(self) -> None:
            buffer = io.BytesIO()
            self.figure.savefig(
                buffer,
                format="svg" if self.use_svg else "png",
                transparent=self.transparent,
            )
            buffer.seek(0)

            if self.use_svg:
                child = SVG(raw_svg=buffer.getvalue().decode("utf-8"))
            else:
                pil_image = PILImage.open(buffer)
                child = Image(
                    image=np.array(pil_image.convert("RGBA")),
                    filter_quality=self.filter_quality,
                )

            self.set_child(child)
