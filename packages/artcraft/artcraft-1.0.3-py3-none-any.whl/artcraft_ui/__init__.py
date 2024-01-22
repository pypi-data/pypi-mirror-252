from .img2img import Image2ImageUI
from .text2img import Text2ImgUI
from .hub import HubUI
from .util import CombinedTabsLayoutUI
from .gradio import gradio as mgr
from .globals import CACHED_CONFIG, init_hubs, prepare


def launch():
    try:
        import matplotlib

        matplotlib.use("TkAgg")
    except:
        print("cannot load backend TkAgg")

    CACHED_HUBS = init_hubs(config=CACHED_CONFIG)

    with mgr.Blocks(title="ArtCraft", analytics_enabled=False) as demo:
        prepare(demo, __file__)

        tabs = CombinedTabsLayoutUI(blocks=[
            Text2ImgUI(name="text2image", hubs=CACHED_HUBS, config=CACHED_CONFIG),
            Image2ImageUI(name="image2image", hubs=CACHED_HUBS, config=CACHED_CONFIG),
            HubUI(name="hub", config=CACHED_CONFIG, hubs=CACHED_HUBS),
        ]).build().run()

    demo.queue(max_size=10).launch(show_error=True,
                                   show_api=False,
                                   server_name="0.0.0.0",
                                   server_port=6006)
