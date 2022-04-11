from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for
)

from bokeh.embed import components
from bokeh.layouts import gridplot
from bokeh.plotting import figure
from bokeh.resources import INLINE
#from bokeh.util.string import encode_utf8
import numpy as np
import scipy.special

from PIL import Image

from app.auth import login_required
from app.db import get_db, query_mongo

bp = Blueprint('viz', __name__)

def make_plot(title, hist, edges):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
        fill_color="navy", line_color="white", alpha=0.5)

    p.y_range.start = 0
    p.legend.location = "center_right"
    p.legend.background_fill_color = "#fefefe"
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color="white"

    return p

@bp.route('/bokehplot', methods=('GET', 'POST'))
def bokehplot():
    im_path = "/mnt/c/Users/samrk/work_files/c4_s13_box2_NF_short.tif"

    bins = np.linspace(0, 256, 50)
    hist = np.zeros(bins.shape[0] - 1)

    with Image.open(im_path) as im:
        im.seek(0)
        frame = 0
        imarray = np.array(im).flatten()

        hist += np.histogram(imarray, bins=bins)[0]

        try:
            while 1:
                im.seek(im.tell() + 1)
                frame = frame + 1

                if frame == 100:
                    im.save("/mnt/c/Users/samrk/work_files/test.png")
                #imarray = np.array(im).flatten()

                #hist += np.histogram(imarray, bins=bins)[0]
        except EOFError:
            pass
    
    p = make_plot("Normal Distribution(mu=0, sigma=0.5)", hist, bins)

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(p)
    html = render_template(
        'viz/bokehplot.html',
        plot_script=script,
        plot_div=div,
        js_resources=js_resources,
        css_resources=css_resources,
    )

    return html

@bp.route('/bokehimg', methods=('GET', 'POST'))
def bokehimg():
    return render_template('viz/bokehimg.html')

@bp.route('/webgl', methods=('GET', 'POST'))
def webgl():
    return render_template('viz/webgl.html')

